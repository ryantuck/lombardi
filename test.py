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


def fit_histogram(data, bin_size):

    # find max/min values
    d_min = min(data)
    d_max = max(data)
    bins = int((d_max-d_min)/bin_size)

    # generate normalized histogram of relative frequencies
    y, x = np.histogram(data, bins=bins, normed=True)

    # generate fit function
    z = scipy.stats.gaussian_kde(data)

    # get a bunch of x data
    x = np.linspace(0,600,1000)

    # fit y coordinates to x data
    y = z(x)

    # normalize y so sum = 1
    y_norm = [i/sum(y) for i in y]

    return (x,y, bins)
    # plot curve and histogram to show hope dope the pairing is
    plt.plot(x,y,c='r')
    plt.hist([j - 0.5 for j in data], normed=True, bins=(d_max-d_min))
    plt.savefig('x.png')


if __name__ == '__main__':
    passing_yds_by_week()
    query_from_template()
    generate_histogram()

