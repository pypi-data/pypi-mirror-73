import logging

from numpy import ndarray
from scipy.stats import rv_discrete
import numpy as np

from .types import TransitionMatrix, Belief


class Dynamics:
    """The abstract base class for a parameterised system that evolves as a function of time,
    control inputs, and its internal dynamics.
    """

    def __call__(self, old_state, control_input, simulation_time):
        raise NotImplementedError

    def reset(self):
        initial_state = self._sample_initial_state()
        return initial_state

    def _step(self, *args, **kwargs):
        raise NotImplementedError

    def _sample_initial_state(self, *args, **kwargs):
        raise NotImplementedError


class MarkovChain(Dynamics):
    """A stochastic model that evolves according to a transition matrix and no external inputs.
    """

    def __init__(
        self, transition_matrix=[[0.99, 0.01], [0.01, 0.99]], initial_distribution=None
    ):

        self._transition_matrix = TransitionMatrix(transition_matrix)
        self._state_space = np.arange(self._transition_matrix.shape[0])
        self._initial_distribution = self._init_starting_distribution(
            initial_distribution
        )

        self._transition_distributions = self._get_transition_distributions()

        self.reset()

    def __call__(self, old_state, *args, **kwargs):
        new_state = self._step(old_state)
        return new_state

    def __repr__(self):
        return "Markov chain with transition matrix\n{}\nand initial distribution\n{}".format(
            self._transition_matrix, self._initial_distribution
        )

    @property
    def initial_distribution(self):
        return self._initial_distribution

    @property
    def transition_matrix(self):
        return self._transition_matrix

    def _step(self, old_state):

        new_state = self._transition_distributions[old_state].rvs()

        return new_state

    def _init_starting_distribution(self, initial_distribution):

        if initial_distribution is not None:

            initial_distribution_ = Belief(initial_distribution)

        else:

            initial_distribution_ = np.array(
                [1] + (self._transition_matrix.shape[0] - 1) * [0]
            )

        return initial_distribution_

    def _get_transition_distributions(self):
        """Creates an array of transition distributions from the transition matrix.
        The transition matrix self._transition_matrix must already be initialised.

        Returns:
            [List of scipy distributions]: The discrete distribution of a transition from each possible state.
             The state indexes the distributions.
        """

        transition_distributions = []

        for state in self._state_space:
            probabilities = self._transition_matrix.transition_probabilities(state)

            transition_distributions.append(
                rv_discrete(
                    name="trans_dist", values=(self._state_space, probabilities)
                )
            )

        return transition_distributions

    def _sample_initial_state(self):

        initial_distribution = rv_discrete(
            name="initial_distribution",
            values=(self._state_space, tuple(self._initial_distribution)),
        )

        return initial_distribution.rvs()


class AugmentedMarkovChain(MarkovChain):
    def __init__(
        self,
        geometric_prior_matrix,
        pre_change_matrix,
        change_matrix,
        post_change_matrix,
        initial_distribution=None,
    ):

        self._geometric_prior = TransitionMatrix(geometric_prior_matrix)
        self._pre_change_matrix = TransitionMatrix(pre_change_matrix)
        self._change_matrix = np.array(change_matrix)
        self._post_change_matrix = TransitionMatrix(post_change_matrix)

        dim = self._pre_change_matrix.shape[0] + self._post_change_matrix.shape[0]
        matrix = np.zeros((dim, dim), dtype=np.float64)

        matrix[
            : self._pre_change_matrix.shape[0], : self._pre_change_matrix.shape[1]
        ] = (self._geometric_prior[0, 0] * self._pre_change_matrix)

        matrix[: self._change_matrix.shape[0], self._pre_change_matrix.shape[1] :] = (
            self._geometric_prior[0, 1] * self._change_matrix
        )

        matrix[
            self._pre_change_matrix.shape[0] :, self._pre_change_matrix.shape[1] :
        ] = (self._geometric_prior[1, 1] * self._post_change_matrix)

        # TODO ADD CASE WHERE CHANGE CAN SWITCH OFF

        logging.debug("Creating transition matrix {}".format(matrix))
        self._transition_matrix = TransitionMatrix(matrix)
        self._state_space = np.arange(self._transition_matrix.shape[0])
        self._transition_distributions = self._get_transition_distributions()
        self._initial_distribution = self._init_starting_distribution(
            initial_distribution
        )

        self.reset()

    def __iter__(self):
        yield ("model_type", "augmented_markov")
        yield ("initial_distribution", self._initial_distribution.tolist())
        yield ("geometric_prior_matrix", self._geometric_prior.tolist())
        yield ("pre_change_matrix", self._pre_change_matrix.tolist())
        yield ("change_matrix", self._change_matrix.tolist())
        yield ("post_change_matrix", self._post_change_matrix.tolist())


class DynamicsFactory:
    """A mixin that allows an object to instantiate a dynamics object from a dictionary of keys eg. a config file
    """

    def _init_dynamics(self, model_type="markov_chain", **kwargs):

        if "initial_distribution" in kwargs.keys():
            initial_distribution = kwargs["initial_distribution"]
        else:
            initial_distribution = None

        if model_type == "markov_chain":
            dynamics_model = MarkovChain(
                kwargs["transition_matrix"], initial_distribution=initial_distribution
            )
        elif model_type == "augmented_markov":
            dynamics_model = AugmentedMarkovChain(
                kwargs["geometric_prior_matrix"],
                kwargs["pre_change_matrix"],
                kwargs["change_matrix"],
                kwargs["post_change_matrix"],
                initial_distribution,
            )

        return dynamics_model

