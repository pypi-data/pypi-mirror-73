import logging

from scipy import stats
import numpy as np

from .types import Belief, TransitionMatrix


class Filter:
    """Abstract base class for a filter that returns an estimate of a state given a measurement
    and possibly other inputs.
    """

    def __init__(self):
        self._logger = logging.getLogger(__name__)

    def __call__(self, measurement, *args, **kwargs):

        state_estimate = self._estimate(measurement, *args, **kwargs)
        return state_estimate

    def _estimate(self, measurement, *args, **kwargs):
        raise NotImplementedError


class HMMFilter(Filter):
    """The optimal bayesian filter for a hidden markov model. 
    This filter does not take inputs to the system into account.
    The dynamics are assumed to be static, and so the filter stores a copy of the markov model parameters.
    """

    def __init__(
        self,
        transition_matrix=[[0.99, 0.01], [0, 1]],
        observation_pdfs=[[0, 1], [0.5, 1]],
        **kwargs
    ):

        super().__init__()

        self.__transition__matrix = TransitionMatrix(transition_matrix)

        if isinstance(observation_pdfs[0], list) or isinstance(
            observation_pdfs[0], tuple
        ):
            observation_pdfs_ = [
                {"mu": dist[0], "std": dist[1]} for dist in observation_pdfs
            ]
        else:
            observation_pdfs_ = observation_pdfs

        self._observation_pdfs = observation_pdfs_

        self._observation_distributions = []

        for param in self._observation_pdfs:
            self._observation_distributions.append(
                stats.norm(param["mu"], param["std"])
            )

    def __repr__(self):
        reprstr = "Bayesian filter"

        return reprstr

    def __iter__(self):
        yield ("type", "forward_bayesian_filter")
        yield ("transition_matrix", self.__transition__matrix.tolist())
        yield ("observation_pdfs", self._observation_pdfs)

    def _estimate(self, measurement, previous_belief):

        likelihood_matrix = self._likelihood_matrix_from_measurement(measurement)

        unnormalised_estimate = np.matmul(
            np.matmul(likelihood_matrix, np.transpose(self.__transition__matrix)),
            previous_belief,
        )

        estimate = Belief(unnormalised_estimate)

        return estimate

    def _likelihood_matrix_from_measurement(self, measurement):
        """Return a diagonal matrix containing the likelihoods of observing the measurement
        for each possible observation distribution

        Args:
            measurement (double): a measurement of the system
        """

        likelihoods = np.zeros_like(self._observation_distributions)

        for i, param in enumerate(self._observation_distributions):
            likelihood = self._observation_distributions[i].pdf(measurement)
            likelihoods[i] = likelihood

        N = len(likelihoods)
        likelihood_matrix = np.zeros((N, N), dtype=np.float64)

        for i in range(N):
            likelihood_matrix[i, i] = likelihoods[i]

        return likelihood_matrix

