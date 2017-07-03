from enum import Enum

import attr

# default tds
tds = list(range(7))

# bucket values
class Bucket(Enum):
    bad = 1
    meh = 2
    ok = 3
    good = 4
    great = 5


prior = {
    'bad': 0.03,
    'meh': 0.27,
    'ok': 0.43,
    'good': 0.22,
    'great': 0.04,
}


@attr.s
class Pdf(object):

    # dict of probabilities
    probs = attr.ib()

    def normalize(self):
        self.probs = {
            k: p / sum(self.probs.values())
            for k,p in self.probs.items()
        }


@attr.s
class DiscreteBayes(object):

    likelihoods = attr.ib()
    prior = attr.ib()

    def update_prior(self, event):
        for k,p in self.prior.probs.items():
            prob_event = self.likelihoods[k].probs[event]
            self.prior.probs[k] *= prob_event
        self.prior.normalize()


    def posterior_predictive(self):

        pp = Pdf({i: 0 for i in list(self.likelihoods.values())[0].probs.keys()})

        for i in pp.probs.keys():
            # i = 0
            pp.probs[i] = sum(
                p.probs[i]*self.prior.probs[k]
                for k,p in self.likelihoods.items()
            )

        pp.normalize()
        return pp
