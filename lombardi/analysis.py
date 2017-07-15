# stuff we need
import math
import matplotlib.pyplot as plt
import petl
import psycopg2

from . import bayes


# big inline graphs by default
plt.rcParams['figure.figsize'] = (20.0, 10.0)

# suppress bullshit scipy warnings
import warnings
warnings.filterwarnings(action="ignore", module="scipy", message="^internal gelsd")

# global connection for db
conn = psycopg2.connect('dbname=nfldb')


def season_buckets(season_param, season_bins):

    # extract data
    full_seasons = petl.fromdb(conn, 'select * from lombardi.qb_aggs').selecteq('num_games', 16)

    vals = [float(y) for y in full_seasons[season_param]]

    # calculate params for our model
    min_v = min(vals)
    max_v = max(vals)
    bin_size = (max_v-min_v)/season_bins

    def rebucket(v):
        if v == season_bins:
            return v-1
        return v

    # bucket vals
    seasons = (
        full_seasons
        .addfield('normed_v', lambda r: float(r[season_param]) - min_v)
        .addfield('bucket', lambda r: int(r['normed_v'] // bin_size))
        .convert(season_param, float)
        # gnarly hack to account for bin logic weirdness on last value
        .convert('bucket', rebucket)
        .cut(('year', 'name', season_param, 'bucket'))
    )

    return seasons


def game_buckets(game_param, game_bins):

    # extract data
    qb_games = petl.fromdb(conn, 'select * from lombardi.qb_stats')

    vals = [float(y) for y in qb_games[game_param]]

    # calculate params for our model
    min_v = min(vals)
    max_v = max(vals)
    bin_size = (max_v-min_v)/game_bins

    def rebucket(v):
        if v == game_bins:
            return v-1
        return v

    # bucket vals
    games = (
        qb_games
        .addfield('normed_v', lambda r: float(r[game_param]) - min_v)
        .addfield('bucket', lambda r: int(r['normed_v'] // bin_size))
        .convert(game_param, float)
        # gnarly hack to account for bin logic weirdness on last value
        .convert('bucket', rebucket)
        .cut(('year', 'name', 'week', game_param, 'bucket'))
    )

    return games


def season_game_bucket_combo_probs(sbs, gbs):

    # join bucketed season performance to bucketed game performance
    sg = sbs.join(gbs, key=('year', 'name'), lprefix='s_', rprefix='g_')

    # get all possible season/game bucket combos as our master list
    all_bucket_combos = petl.fromdicts([
        {'s_bucket': s, 'g_bucket': g}
        for s in set(sg['s_bucket'])
        for g in set(sg['g_bucket'])
    ])

    # get counts of all existing season/game bucket combos
    game_bucket_counts = sg.aggregate(('s_bucket', 'g_bucket'), len)

    # generate counts for all season/game bucket combos and fill in
    # any missing values with 0
    all_game_bucket_counts = (
        all_bucket_combos
        .leftjoin(
            game_bucket_counts,
            key=('s_bucket', 'g_bucket'),
            missing=0,
        )
        .rename({'value': 'g_count'})
    )

    # calculate season bucket counts
    s_bucket_game_counts = (
        all_game_bucket_counts
        .aggregate('s_bucket', sum, 'g_count')
        .rename({'value': 's_count'})
    )

    # get probs for each season-game turnout
    g_bucket_probs = (
        all_game_bucket_counts
        .join(s_bucket_game_counts, key=('s_bucket'))
        .addfield('prob', lambda r: r['g_count'] / r['s_count'])
        .cut(('s_bucket', 'g_bucket', 'g_count', 's_count', 'prob'))
    )

    return g_bucket_probs


def data_dicts(sbs, gbs):

    season_dicts = petl.dicts(sbs)
    game_dicts = petl.dicts(gbs)

    data = []

    for s in season_dicts:
        gd = [
            {
                k:v for k,v in x.items()
                if k in ['yards', 'week', 'bucket']
            }
            for x in game_dicts
            if x['year'] == s['year']
            and x['name'] == s['name']
        ]

        data.append(dict(
            season=s,
            games=sorted(gd, key=lambda r: r['week']),
        ))

    return data

def bucket_dist(table):
    # get explicit probability distributions
    agg = table.aggregate('bucket', len)
    tot = sum(agg['value'])
    probs = agg.addfield('prob', lambda r: r['value'] / tot)
    return probs


def conduct_runs(data, likelihoods, prior):

    runs = []

    for d in data:

        #print(d['season']['year'], d['season']['name'])

        # list of actual values
        bucket_vals = [g['bucket'] for g in d['games']]

        dist = bayes.DiscreteBayes(
            prior=bayes.Pdf(dict(prior)),
            likelihoods=dict(likelihoods),
        )

        initial_posterior_predictive = dist.posterior_predictive()

        results = []

        # pre-season
        results.append({
            'prior': dict(dist.prior.probs),
            'posterior_predictive': list(dist.posterior_predictive().probs.values()),
        })

        # track bayesian results week by week
        for val in bucket_vals:

            # given game performance this week, update our prior
            dist.update_prior(val)

            # store results
            results.append(dict(
                prior=dict(dist.prior.probs),
                posterior_predictive=list(dist.posterior_predictive().probs.values()),
            ))

        # calculate statistics
        expected_vals = expected_values(results)
        rmse_run = rmse(expected_vals, bucket_vals)

        initial_expected_val = sum(
            k*v for k,v in initial_posterior_predictive.probs.items()
        )

        rmse_avg = rmse([initial_expected_val]*17, bucket_vals)

        runs.append(dict(
            data=d,
            bucket_vals=bucket_vals,
            expected_vals=expected_vals,
            initial_posterior_predictive=initial_posterior_predictive.probs,
            rmse_avg=rmse_avg,
            rmse_run=rmse_run,
            results=results,
        ))

    return runs


def expected_value(pp):
    """
    Extract expected value given a posterior predictive distribution.
    """
    return sum(i*x for i,x in enumerate(pp))


def expected_values(results):
    """
    Generate a list of expected values from a list of posterior predictive
    distributions in `results`.
    """
    return [
        expected_value(r['posterior_predictive'])
        for r in results
    ]

def rmse(expected, actual):
    """
    Calculate RMSE between a list of expected values and
    a list of actual values.
    """
    deltas = [e-a for e, a in zip(expected, actual)]
    sq_deltas = [pow(d,2) for d in deltas]
    avg_delta = sum(sq_deltas) / len(sq_deltas)
    rmse = math.sqrt(avg_delta)
    return rmse


def rmse_analysis(runs):
    rmse_runs = [r['rmse_run'] for r in runs]
    rmse_avgs = [r['rmse_avg'] for r in runs]
    ratios = [r/a for r,a in zip(rmse_runs, rmse_avgs)]

    total_rmse_ratio = sum(rmse_runs) / sum(rmse_avgs)
    avg_ratio = sum(ratios) / len(ratios)

    return dict(
        rmse_runs=rmse_runs,
        rmse_avgs=rmse_avgs,
        ratios=ratios,
        avg_ratio=avg_ratio,
    )


def analyze(season_bins, game_bins):

    # extract bucketed season / game performance
    gbs = game_buckets('yards', game_bins)
    sbs = season_buckets('avg_yds', season_bins)

    # create probability distribution tables for seasons / games
    s_bucket_probs = bucket_dist(sbs)
    sg_bucket_probs = season_game_bucket_combo_probs(sbs, gbs)

    # generate likelihoods and prior
    s_bucket_dicts = list(petl.dicts(s_bucket_probs))
    sg_bucket_dicts = list(petl.dicts(sg_bucket_probs))
    s_buckets = sorted(set(s['bucket'] for s in s_bucket_dicts))

    likelihoods = {
        sb: bayes.Pdf({
            gb['g_bucket']: gb['prob']
            for gb in sg_bucket_dicts
            if gb['s_bucket'] == sb
        })
        for sb in s_buckets
    }

    prior = {s['bucket']: s['prob'] for s in s_bucket_dicts}

    # get appropriately-formed data
    data = data_dicts(sbs, gbs)

    # run analysis on data
    runs = conduct_runs(data, likelihoods, prior)

    # conduct rmse analysis overall and by bucket
    rmse_results = dict(
        overall=rmse_analysis(runs),
        by_bucket=dict(),
    )

    for sb in range(season_bins):
        tmp_runs = [r for r in runs if r['data']['season']['bucket'] == sb]
        rmse_results['by_bucket'][sb] = rmse_analysis(tmp_runs)

    # return all data!
    return dict(
        runs=runs,
        likelihoods={k:v.probs for k,v in likelihoods.items()},
        prior=prior,
        rmse_analysis=rmse_results,
    )


def rmse_scatter(results):
    for k,v in results['rmse_analysis']['by_bucket'].items():
        plt.scatter(v['rmse_runs'], v['rmse_avgs'], label=k)

    overall = results['rmse_analysis']['overall']['rmse_runs']
    lims = [min(overall), max(overall)]
    plt.plot(lims, lims)

    plt.xlabel('RMSE Run')
    plt.ylabel('RMSE Avg')

    plt.legend()


def sorted_rmse_ratio_scatter(results):
    bucketed_ratios = []
    for k,v in results['rmse_analysis']['by_bucket'].items():
        for r,a in zip(v['rmse_runs'], v['rmse_avgs']):
            bucketed_ratios.append(dict(
                bucket=k,
                rmse_run=r,
                rmse_avg=a,
                ratio=r/a,
            ))
            
    sorted_br = sorted(bucketed_ratios, key=lambda x: x['ratio'])

    tuples = {b: [] for b in results['rmse_analysis']['by_bucket'].keys()}

    for idx,x in enumerate(sorted_br):
        tuples[x['bucket']].append((idx, x['ratio']))

    for b, vals in tuples.items():
        x = [v[0] for v in vals]
        y = [v[1] for v in vals]
        plt.scatter(x, y, label=b)

    # plot lines for reference
    ratios = results['rmse_analysis']['overall']['ratios']
    avg_ratio = sum(ratios) / len(ratios)
    plt.plot(range(len(ratios)), [1]*len(ratios), label=1, color='black')
    plt.plot(range(len(ratios)), [avg_ratio]*len(ratios), label='avg', color='r')

    plt.ylabel('RMSE Run / RMSE Avg')

    plt.legend()










