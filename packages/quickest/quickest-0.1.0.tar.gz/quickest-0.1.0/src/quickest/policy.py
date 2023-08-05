import logging, os
import math
import numpy as np
from scipy.special import logit, expit as logistic

from .optim import SolverFactory
from .util import print_progress_bar


def get_policy(type="single_threshold_detector", **kwargs):
    """Returns a policy object.

    Args:
        type (str, optional): The type of policy to return. Options:
        
        "single_threshold_detector"
        
        Defaults to "single_threshold_detector".

    Returns:
        Subclass of change.policy.StoppingPolicy: A stopping policy object
    """

    if type == "single_threshold_detector":
        return ChangePointDetector(**kwargs)

    # TODO CHANGE POINT ISOLATOR, HYPERPLANE...


class StoppingPolicy:
    """Abstract base class for a parameterised function that maps a belief state to an action
    """

    def __init__(self, pre_change_states, post_change_states, *args, **kwargs):

        self._logger = logging.getLogger(__name__)
        logging.basicConfig(level="DEBUG")

        self._action_space = self._define_action_space(**kwargs)

        self._logger.debug("Kwargs: {}".format(kwargs))
        self._params = self._init_params(*args, **kwargs)

        self._pre_change_states = pre_change_states
        self._post_change_states = post_change_states

        self._solver = None

    def __call__(self, belief):

        belief_ = np.array(belief)
        action = self._map_belief_to_action(belief_)
        return action

    def __repr__(self):

        repstr = "Policy with possible actions: \n"

        for action in self._action_space:
            repstr = repstr + str(action) + "\n"

        return repstr

    def evaluate(self, process, estimator):
        """Run a sample realisation of the process using this policy as the controller. 
        Returns when a change is declared resulting in a final cost, or maximum steps are reached.

        Args:
            process (ChangeProcess): The process whose dynamics will be used to test the controller
            estimator (Sensor): The filter used to obtain belief estimates from the process measurements.

        Returns:
            float64: Cost incurred
        """
        process.reset()

        control_input = 0
        measurement, cost = process(control_input)
        belief = process.sample_initial_belief()

        k = 1
        while cost == 0 and k < process.maximum_duration:

            belief = estimator(measurement, belief)

            control_input = self._map_belief_to_action(belief)

            measurement, cost = process(control_input)

            k = k + 1

        if np.isnan(cost):
            raise Exception("Policy evaluation returned NaN cost!")

        self._logger.debug("Evaluation cost: {}".format(cost))
        return np.float64(cost)

    def fit(self, process, estimator, *args, **kwargs):
        raise NotImplementedError

    def _marginalise_belief(self, belief):
        """Marginalises a belief state over all pre- and post-change states.

        Args:
            belief (change.types.Belief): A belief regarding the state of a process

        Returns:
            Belief: A 2-dimensional belief, where the 0th element is the belief that the process 
            is in pre-change state and the 1st element is the belief that the process is in the post-change state.
        """

        marginalised_belief = np.ndarray(2, dtype=np.float64)
        marginalised_belief[0] = np.sum(belief[self._pre_change_states])
        marginalised_belief[1] = np.sum(belief[self._post_change_states])

        return marginalised_belief

    def _define_action_space(self, *args, **kwargs):
        raise NotImplementedError

    def _init_params(self, *args, **kwargs):
        """How to initialise the policy
        """
        raise NotImplementedError

    def _map_belief_to_action(self, belief):
        raise NotImplementedError


class ChangePointDetector(StoppingPolicy, SolverFactory):
    """A change detection policy that returns either 0 (continue) or 1 (stop).
    If there are multiple pre- and post- change states, the state estimate will be 
    marginalised before applying the decision rule.

    """

    def __init__(self, pre_change_states=[0], post_change_states=[1], *args, **kwargs):

        super().__init__(pre_change_states, post_change_states, *args, **kwargs)

    def __repr__(self):
        return "1D change point detector with threshold {}".format(self.threshold)

    def __iter__(self):
        yield ("Type", "single_threshold_detector")
        yield ("decision_boundary", float(self._reparameterise(self._params[0])))
        yield ("pre_change_states", self._pre_change_states)
        yield ("post_change_states", self._post_change_states)
        yield ("solver", dict(self._solver))

    # TODO is this general enough to be in the base policy class?
    def fit(
        self,
        process,
        estimator,
        solver_iterations=100,
        initial_learning_rate=1,
        **kwargs
    ):

        self._logger.info("Optimising for {} steps".format(solver_iterations))

        self._solver = self._get_solver(
            process, estimator, self, solver_iterations, initial_learning_rate, **kwargs
        )

        self._logger.debug("Got solver {}".format(self._solver))

        threshold_history = np.zeros(solver_iterations)

        for k in range(solver_iterations):
            self._logger.debug("{}[{}/{}]".format("-" * 60, k, solver_iterations))
            param_k = self._solver.step()
            self._logger.debug("Got param in training loop: {}".format(param_k))
            threshold_k = self._reparameterise(param_k)
            self._logger.debug("Reparameterised to threshold: {}".format(threshold_k))
            threshold_history[k] = threshold_k
            print_progress_bar(k, solver_iterations)

        process.reset()

        return threshold_history[-1], threshold_history

    @property
    def threshold(self):
        return self._reparameterise(self._params)

    @property
    def params(self):
        return self._params

    @params.setter
    def params(self, param_vector):
        """Setter for the policy's free parameter vector.

        Args:
            param_vector (array-like): The new parameters

        """

        var = param_vector[0]

        if np.isnan(var):
            raise AttributeError("Policy received NaN parameter")

        if len(param_vector) is not 1:
            raise AttributeError("Parameter vector for detector should be length 1")

        self._params = np.array(param_vector, dtype=np.float64)

    def _define_action_space(self, *args, **kwargs):
        return [0, 1]

    def _map_belief_to_action(self, belief):

        marginalised_belief = self._marginalise_belief(belief)

        decision_threshold = self._reparameterise(self._params[0])

        action = 0
        if marginalised_belief[1] > decision_threshold:
            action = 1

        return action

    def _init_params(self, decision_boundary=0.5, **kwargs):
        """A simple detector only requires a single parameter.

        Args:
            param (float, optional): The free optimisation parameter.

        Returns:
            [np.array float64] A one-dimensional array of type float64 containing the parameter.
        """

        self._logger.debug(
            "Request for initial threshold: {}".format(decision_boundary)
        )
        param = logit(decision_boundary)
        self._logger.debug("Set to param: {}".format(param))

        return np.array([param], dtype=np.float64)

    def _reparameterise(self, params):
        """Turns the free optimisation parameter into a decision threshold

        Args:
            params (numpy float64): [description]

        Returns:
            numpy float64: Decision threshold in [0,1]
        """
        return np.float64(logistic(params))


class ChangePointIsolator(StoppingPolicy):
    """A change detection policy that also isolates individual anomalies. 
    The dimensions in the belief state index the change that is to be declared, 
    TODO FIX CASE WITH MULTIPLE PRE- AND POST CHANGE DISTRIBUTIOSN
    """

    def __init__(self, anomaly_count=1, **kwargs):
        # TODO INITIALISE WITH PRE- AND POST- CHNAGE DISTRIBUTIONS
        super().__init__(anomaly_count=anomaly_count)

    def __call__(self, belief):
        return super().__call__(belief)

    def _define_action_space(self, anomaly_count=1, **kwargs):

        action_space = []

        for action in range(anomaly_count + 1):
            action_space.append(action)

        return action_space


class LinearHyperplaneThreshold(ChangePointIsolator):
    def __init__(self, anomaly_count, params=None):

        super().__init__(anomaly_count=anomaly_count)
        self._action_space = self._define_action_space(anomaly_count=anomaly_count)

    def __call__(self, belief):
        return super().__call__(belief)

    def _map_belief_to_action(self, belief):

        actions = []

        for (i, param) in enumerate(self._params):

            hyperplane = self.__hyperplane__from__parameters(param)
            crossed_threshold = self.__detect__threshold__crossing(hyperplane, belief)

            if crossed_threshold == True:

                action = self._action_space[i + 1]
                actions.append(action)

        if len(actions) == 0:
            return 0

        # elif len(actions) > 1:
        #     msg = "Invalid stopping policy. State {} returned multiple valid actions: {}. Using first action {}".format(
        #         belief, actions, actions[0]
        #     )

        return actions[0]

    def _init_params(self, *args, **kwargs):
        """The parameters for this policy are free parameters that undergo a reparameterisation 
        in order to define a valid hyperplane decision boundary.

        Returns:
            NxN array of float64: The first dimension indexes each change type, and the second dimension indexes the ith parameter
        """

        num_params = len(self._action_space) - 1
        param_dimension = len(self._action_space) - 1

        params = np.zeros((num_params, param_dimension), dtype=np.float64)

        for i in range(num_params):

            valid_params = False

            while not valid_params:

                candidate_params = np.random.uniform(
                    -param_dimension, param_dimension, param_dimension
                ).astype(np.float64)

                associated_belief = np.zeros(len(self._action_space), dtype=np.float64)
                associated_belief[i + 1] = 1.0

                candidate_hyperplane = self.__hyperplane__from__parameters(
                    candidate_params
                )

                crossing_detected = self.__detect__threshold__crossing(
                    candidate_hyperplane, associated_belief
                )

                if crossing_detected:

                    params[i, :] = candidate_params
                    valid_params = True

        return params

    def __hyperplane__from__parameters(self, params):
        """Converts free parameters (suitable as inputs to an unconstrained optimisation problem) 
        into the hyperplane parameters used by the linear threshold rule.

        Args:
            params (numpy array of float64): policy parameters for a single decision threshold
        """

        param_dimension = len(self._action_space) - 1
        hyperplane_params = np.zeros(param_dimension, dtype=np.float64)

        for i, phi in enumerate(params):

            if i == len(params) - 1:
                theta = np.power(phi, 2)

            elif i == len(params) - 2:
                theta = 1 + np.power(phi, 2)

            else:
                theta = (1 + np.power(params[-2], 2)) * np.power(math.sin(phi), 2)

            hyperplane_params[i] = theta

        return hyperplane_params

    def __detect__threshold__crossing(self, hyperplane, belief):
        """Detect whether a belief state has crossed a decision boundary.

        Args:
            hyperplane (array): A set of parameters representing a subspace of the belief space.
            belief (array): A point in the belief space
        """

        vec1 = np.zeros(hyperplane.shape[0] + 2)
        vec1[0] = 0
        vec1[1] = 1
        vec1[2:] = hyperplane

        vec2 = np.zeros(len(self._action_space) + 1)
        vec2[0:-1] = belief
        vec2[-1] = -1

        crossing_statistic = np.inner(vec1, vec2)

        threshold_crossed = crossing_statistic < 0

        return threshold_crossed

    def __repr__(self):

        return super().__repr__() + "\nParams: {}".format(self._params)

