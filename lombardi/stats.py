import numpy as np
import scipy.stats

def get_stats(x_data, y_data):

    probs = {
        0.05: None,
        0.25: None,
        0.5: None,
        0.75: None,
        0.95: None,
    }

    for p in probs.keys():
        tot = 0
        for x,y in zip(x_data, y_data):
            tot += y
            if tot > p:
                probs[p] = int(round(x))
                break

    return probs


def num_bins(data, bin_size):

    # find max/min values
    d_min = min(data)
    d_max = max(data)
    bins = int((d_max-d_min)/bin_size)
    return bins


def fit_kde(x, data, normalize=False):

    kde = scipy.stats.gaussian_kde(data)
    y_kde = kde(x)
    if normalize: y_kde = [a/sum(y_kde) for a in y_kde]

    return x, y_kde


def fit_normal(x, data, normalize=False):

    mu, std = scipy.stats.norm.fit(data)
    y_normal = scipy.stats.norm.pdf(x, mu, std)
    if normalize: y_normal = [a/sum(y_normal) for a in y_normal]

    return x, y_normal


def fit_gamma(x, data, normalize=False):

    x, y_kde = fit_kde(x, data, normalize=True)

    c = scipy.stats.rv_discrete(name='custom', values=(x,y_kde))
    data_kde = c.rvs(size=len(x))
    a,l,b = scipy.stats.gamma.fit(data_kde)
    rv = scipy.stats.gamma(a,l,b)
    y_gamma = rv.pdf(x)
    if normalize: y_gamma = [a/sum(y_gamma) for a in y_gamma]

    return x, y_gamma


def cdf(x, data):

    x, y_kde = fit_kde(x, data, normalize=True)

    c = scipy.stats.rv_discrete(name='custom', values=(x,y_kde))
    data_kde = c.rvs(size=len(x))
    a,l,b = scipy.stats.gamma.fit(data_kde)
    rv = scipy.stats.gamma(a,l,b)
    y_cdf = rv.cdf(x)

    return x, y_cdf




