import nfldb
from jinja2 import Template
import pandas as pd
import scipy.stats
import matplotlib.pyplot as plt
import numpy as np


db = nfldb.connect()
conn = 'postgres://nfldb:nfldb@localhost:5432/nfldb'


def top_5_rushers():
    q = nfldb.Query(db)
    q.game(season_year=2015, season_type='Regular')
    for pp in q.sort('rushing_yds').limit(5).as_aggregate():
        print pp.player, pp.rushing_yds


def passing_yds_by_week():
    for wk in range(1, 17):
        q_brady = nfldb.Query(db)
        q_brady.game(season_year=2015, season_type='Regular', week=wk)
        q_brady.player(full_name='Tom Brady')
        for pp in q_brady.as_aggregate():
            print pp.player, pp.passing_yds


def query_from_template():
    with open('sql/passing_yds_per_game.sql.j2') as f:
        template = Template(f.read())
    query = template.render(year=2015, full_name='Tom Brady')
    print query
    results = pd.read_sql(query, conn)
    print results


def generate_histogram():
    with open('sql/brady_test.sql') as f:
        template = Template(f.read())

    players = [
        'Tom Brady',
        'Aaron Rodgers',
        'Peyton Manning',
    ]

    for p in players:

        q = template.render(full_name=p)
        results = pd.read_sql(q, conn)
        fit_histogram(list(results['yards']), 25)


def num_bins(data, bin_size):

    # find max/min values
    d_min = min(data)
    d_max = max(data)
    bins = int((d_max-d_min)/bin_size)
    return bins


def print_brady_by_game():
    q_brady = nfldb.Query(db)
    q_brady.game(season_year=2015, season_type='Regular', week=1)
    q_brady.player(full_name='Tom Brady')
    for pp in q_brady.as_play_players():
        print pp.player, pp.passing_yds

    print sum([x.passing_yds for x in q_brady.as_play_players()])


def plot_player(player, metric, min_year=None, max_year=None, x_max=None):

    data = player_metric(player, metric, min_year=None, max_year=None)
    plot_stuff(data, x_max, chart_title)


def player_metric(player, metric, min_year=None, max_year=None):

    # retrieve data
    with open('sql/by_game_template.sql') as f:
        template = Template(f.read())

    query = template.render(
        player=player,
        metric=metric,
        min_year=min_year,
        max_year=max_year,
    )

    results = pd.read_sql(query,conn)
    return list(results[metric])


def plot_stuff(data, x_max=None, chart_title='Metric'):

    bin_size = 20

    # dynamically determine x_max
    if x_max is None:
        x_max = round(max(data), -2) + 100

    # get some necessary x values
    x = np.linspace(0, x_max, 1000)

    # fit to kde
    kde = scipy.stats.gaussian_kde(data)
    y1 = kde(x)

    # fit to normal distribution
    mu, std = scipy.stats.norm.fit(data)
    y2 = scipy.stats.norm.pdf(x, mu, std)

    # fit to gamma dist
    a,l,b = scipy.stats.gamma.fit(data)
    rv = scipy.stats.gamma(a,l,b)
    y3 = rv.pdf(x)

    # plot everything plus histogram
    fig = plt.figure(figsize=(20,10))
    fig.suptitle(chart_title, fontsize=20)
    axes = plt.gca()
    axes.set_xlim([0, x_max])
    plt.plot(x, y1, label='kde', lw=2)
    plt.plot(x, y2, label='normal', lw=2)
    plt.plot(x, y3, label='gamma', lw=2)
    plt.hist(
        [j - bin_size/2 for j in data],
        normed=True,
        bins=num_bins(data, bin_size),
        label='hist',
        alpha=0.5,
        width=10,
        align='mid',
    )
    plt.legend()





if __name__ == '__main__':
#    passing_yds_by_week()
#    query_from_template()
#    generate_histogram()
    print_brady_by_game()

