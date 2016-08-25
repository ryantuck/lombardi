from jinja2 import Template
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.stats

import data as ld
import stats


def fit_demo(data, x_max=None, bin_size=20, chart_title='Metric', normalize=True):

    # dynamically determine x_max
    if x_max is None:
        x_max = round(max(data), -2) + 100

    # get some necessary x values
    x = np.linspace(0, x_max, 1000)

    # fit to kde
    x, y1 = stats.fit_kde(x, data, normalize)

    # fit to normal distribution
    x, y2 = stats.fit_normal(x, data, normalize)

    # fit to gamma dist
    x, y3 = stats.fit_gamma(x, data, normalize)

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
        bins=stats.num_bins(data, bin_size),
        label='hist',
        alpha=0.5,
        width=float(bin_size)/2,
        align='mid',
    )
    plt.legend()


def add_gamma_dist(data, x, label=None, normalize=True):

    # fit to kde
    x, y_gamma = stats.fit_gamma(x, data, normalize)
    plt.plot(x, y_gamma, label=label)


def add_kde(data, x, label=None, normalize=True):

    x, y_kde = stats.fit_gamma(x, data, normalize)
    plt.plot(x, y_kde, label=label)


def plot_players(players, metric, min_year=None, max_year=None):

    x = np.linspace(0, ld.metric_range(metric), 1000)
    plot = plt.figure(figsize=(20,10))

    for player in players:

        player_data = ld.player_metric(
            player=player,
            metric=metric,
            min_year=2014,
        )

        add_gamma_dist(player_data, x, label=player)

    plt.legend()


def plot_player_years(player, metric, min_year=2009, max_year=2015):

    x = np.linspace(0, ld.metric_range(metric), 1000)
    plot = plt.figure(figsize=(20,10))

    for year in range(min_year, max_year+1):

        player_data = ld.player_metric(
            player=player,
            metric=metric,
            min_year=year,
            max_year=year,
        )

        if len(player_data) > 0:
            add_gamma_dist(player_data, x, label=year)

    plt.legend()



if __name__ == '__main__':
    pass
