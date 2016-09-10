import numpy as np
import scipy.stats
from scipy.optimize import minimize
from scipy.misc import factorial

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


def weight_data(data, weights):
    data_w = [a*b for a,b in zip(data, weights)]
    return [
        int(x * float(sum(data))/sum(data_w))
        for x in data_w
    ]


def fit_kde(x, data, normalize=False):

    data_pos = [a for a in data if a > 0]

    kde = scipy.stats.gaussian_kde(data_pos)
    y_kde = kde(x)

    if normalize: y_kde = [a/sum(y_kde) for a in y_kde]

    return x, y_kde


def fit_normal(x, data, normalize=False):

    mu, std = scipy.stats.norm.fit(data)
    y_normal = scipy.stats.norm.pdf(x, mu, std)
    if normalize: y_normal = [a/sum(y_normal) for a in y_normal]

    return x, y_normal


def fit_gamma(x, data, normalize=False):

    data_pos = [a for a in data if a > 0]

    # get kde first (bc gamma shits the bed sometimes :shrug:)
    x, y_kde = fit_kde(x, data_pos, normalize=True)
    c = scipy.stats.rv_discrete(name='custom', values=(x,y_kde))
    data_kde = c.rvs(size=len(x))
    data_kde_pos = [a for a in data_kde if a > 0]

    # fit to gamma
    a,l,b = scipy.stats.gamma.fit(data_kde_pos, floc=0)
    rv = scipy.stats.gamma(a,l,b)
    y_gamma = rv.pdf(x)

    if normalize: y_gamma = [a/sum(y_gamma) for a in y_gamma]

    return x, y_gamma


def poisson(k, lamb):
    """poisson pdf, parameter lamb is the fit parameter"""
    return (lamb**k/factorial(k)) * np.exp(-lamb)


def fit_poisson(x, data, bin_size=25, normalize=False):

    param = poisson_params(x, data, bin_size)
    x_max = round(max(data), -2) + 100
    x = np.linspace(0, x_max, 1000)
    x_plot = np.linspace(0, x_max/bin_size, 1000)

    # normalize poisson distribution

    y_poisson = poisson(x_plot, param)

    if normalize:
        y_poisson = [a/sum(y_poisson) for a in y_poisson]

    return x, y_poisson


def gamma_params(x, data):

    data_pos = [a for a in data if a > 0]

    # get kde first (bc gamma shits the bed sometimes :shrug:)
    x, y_kde = fit_kde(x, data_pos, normalize=True)
    c = scipy.stats.rv_discrete(name='custom', values=(x,y_kde))
    data_kde = c.rvs(size=len(x))
    data_kde_pos = [a for a in data_kde if a > 0]

    # fit to gamma
    a,l,b = scipy.stats.gamma.fit(data_kde_pos, floc=0)
    return a,b


def poisson_params(x, data, bin_size=25, x_max=300):

    # get kde first (bc gamma shits the bed sometimes :shrug:)
    data_pos = [a for a in data if a > 0]
    x, y_kde = fit_kde(x, data_pos, normalize=True)
    c = scipy.stats.rv_discrete(name='custom', values=(x,y_kde))
    data_kde = c.rvs(size=len(x))
    data_kde_pos = [a for a in data_kde if a > 0]

    def negLogLikelihood(params, data):
        """ the negative log-Likelohood-Function"""
        lnl = - np.sum(np.log(poisson(data, params[0])))
        return lnl

    def bin_data(x_sample, bin_size):
        return (x_sample - x_sample % bin_size) / bin_size

    #x_max = round(max(data), -2) + 100

    x = np.linspace(0, x_max, 1000)

    binned = [bin_data(a, bin_size) for a in data_kde_pos]

    binned_pos = [a for a in binned if a > 0]

    # minimize the negative log-Likelihood
    result = minimize(negLogLikelihood,  # function to minimize
                      x0=np.ones(1),     # start value
                      args=(binned_pos,),      # additional arguments for function
                      method='Powell',   # minimization method, see docs
                      )

    print x_max, float(result.x)
    return float(result.x)


def cdf(x, data):

    x, y_kde = fit_kde(x, data, normalize=True)

    c = scipy.stats.rv_discrete(name='custom', values=(x,y_kde))
    data_kde = c.rvs(size=len(x))
    a,l,b = scipy.stats.gamma.fit(data_kde)
    rv = scipy.stats.gamma(a,l,b)
    y_cdf = rv.cdf(x)

    return x, y_cdf


def probability_bucket(x, cdf, y1, y2):

    def idx(yds):
        return int(float(yds) * (len(x)-1)/max(x))

    return cdf[idx(y2)] - cdf[idx(y1)]




