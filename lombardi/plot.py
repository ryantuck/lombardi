import nfldb
from jinja2 import Template
import pandas as pd
import scipy.stats
import matplotlib.pyplot as plt
import numpy as np


db = nfldb.connect()
conn = 'postgres://nfldb:nfldb@localhost:5432/nfldb'


def num_bins(data, bin_size):

    # find max/min values
    d_min = min(data)
    d_max = max(data)
    bins = int((d_max-d_min)/bin_size)
    return bins


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


def fit_demo(data, x_max=None, chart_title='Metric'):

    bin_size = 20

    # dynamically determine x_max
    if x_max is None:
        x_max = round(max(data), -2) + 100

    # get some necessary x values
    x = np.linspace(0, x_max, 1000)

    # fit to kde
    kde = scipy.stats.gaussian_kde(data)
    y1 = kde(x)
    tot = sum(y1)
    y1 = [a/tot for a in y1]

    # fit to normal distribution
    mu, std = scipy.stats.norm.fit(data)
    y2 = scipy.stats.norm.pdf(x, mu, std)
    tot = sum(y2)
    y2 = [a/tot for a in y2]

    # fit to gamma dist
    c = scipy.stats.rv_discrete(name='custom', values=(x,y1))
    data_kde = c.rvs(size=len(x))
    print len(data_kde)
    a,l,b = scipy.stats.gamma.fit(data_kde)
    rv = scipy.stats.gamma(a,l,b)
    y3 = rv.pdf(x)
    tot = sum(y3)
    y3 = [a/tot for a in y3]

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


def add_gamma_dist(data, x, label=None):

    # fit to kde
    kde = scipy.stats.gaussian_kde(data)
    y_kde = kde(x)
    y_kde = [a/sum(y_kde) for a in y_kde]

    # get sample data from kde dist for better fitting
    c = scipy.stats.rv_discrete(name='custom', values=(x,y_kde))
    data_kde = c.rvs(size=len(x))

    # fit to gamma dist
    a,l,b = scipy.stats.gamma.fit(data_kde)
    rv = scipy.stats.gamma(a,l,b)
    y_gamma = rv.pdf(x)
    y_gamma = [a/sum(y_gamma) for a in y_gamma]

    plt.plot(x, y_gamma, label=label)




if __name__ == '__main__':
    pass
