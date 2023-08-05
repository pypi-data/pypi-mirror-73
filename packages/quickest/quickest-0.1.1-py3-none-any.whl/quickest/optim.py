import logging
import numpy as np


class LearningRateScheduler:
    # TODO CONVERT TO ABC WITH ENFORCED PROPERTIES
    pass


class ExponentialDecay(LearningRateScheduler):
    """The learning rate L at training step k out of N total training steps with initial rate L0 and decay parameter d:

    L = L0 * exp(-d*k/K)

    The decay parameter defaults to 1, which corresponds to a final learning rate LN at time step k=N:

    LN ~ 0.37*L0

    """

    def __init__(self, initial_learning_rate, decay_constant=1, **kwargs):
        self._initial_learning_rate = initial_learning_rate
        self._decay_constant = np.float64(decay_constant)

    def __call__(self, current_step, maximum_steps):
        """
        Returns:
            np float64: A scalar in [0,1]
        """
        K = np.float64(maximum_steps)  # np.float64(0.3) * np.float64(maximum_steps)
        k = np.float64(current_step)
        d = self._decay_constant
        learning_rate = self._initial_learning_rate * np.exp(-(k * d / K))
        return learning_rate

    def __repr__(self):
        return "Exponentially decaying learning rate scheduler with initial value {} and decay constant {}".format(
            self._initial_learning_rate, self._decay_constant
        )

    # TODO move THIS TO ABC WITH ENFORCED PROPERTIES
    def __iter__(self):
        yield ("type", "exponential_decay")
        yield ("initial_learning_rate", self._initial_learning_rate)
        yield ("decay_constant", float(self._decay_constant))


class LinearDecay(LearningRateScheduler):
    pass


class ConstantRate(LearningRateScheduler):
    pass


class LearningRateFactory:
    def _get_lr_scheduler(
        self,
        initial_learning_rate=0.001,
        type="exponential_decay",
        decay_constant=1,
        **kwargs
    ):
        if type == "exponential_decay":
            return ExponentialDecay(
                initial_learning_rate, decay_constant=decay_constant
            )
        elif type == "linear_decay":
            return LinearDecay(initial_learning_rate)
        elif type == "constant":
            return ConstantRate(initial_learning_rate)


class Solver(LearningRateFactory):
    def __init__(
        self,
        process,
        estimator,
        policy,
        maximum_steps,
        initial_learning_rate,
        learning_rate_type="exponential_decay",
        **kwargs
    ):

        self._logger = logging.getLogger(__name__)
        logging.basicConfig(level="DEBUG")
        self._process = process
        self._estimator = estimator
        self._policy = policy
        self._step = 0
        self._maximum_steps = maximum_steps

        self._logger.debug(
            "Maximum steps: {}, initial_learning_rate: {}, learning_rate_type: {}".format(
                maximum_steps, initial_learning_rate, learning_rate_type
            )
        )
        self._learning_rate_scheduler = self._get_lr_scheduler(
            initial_learning_rate=initial_learning_rate,
            learning_rate_type=learning_rate_type,
            **kwargs
        )

        self._logger.debug(
            "Got learning rate scheduler {}, requested {}".format(
                self._learning_rate_scheduler, learning_rate_type
            )
        )

    def step(self, *args, **kwargs):
        raise NotImplementedError

    def _compute_gradient(self, *args, **kwargs):
        raise NotImplementedError

    def _backprop_gradients(self, *args, **kwargs):
        raise NotImplementedError


class StochasticPerturbation(Solver):
    """TODO MAKE THIS WORK FOR ANY SIZED PARAMETER VECTOR

    Spall, J. C. (1992). Multivariate stochastic approximation using a simultaneous perturbation gradient approximation. 
    IEEE transactions on automatic control, 37(3), 332-341.
    """

    def __init__(
        self,
        process,
        estimator,
        policy,
        maximum_steps=100,
        initial_learning_rate=1,
        learning_rate_type="exponential_decay",
        loss_samples_per_step=10,
        **kwargs
    ):

        super().__init__(
            process,
            estimator,
            policy,
            maximum_steps,
            initial_learning_rate,
            learning_rate_type,
            **kwargs
        )

        self._loss_samples_per_step = loss_samples_per_step

    def step(self):

        old_params = self._policy.params
        gradient = self._compute_gradient(old_params)
        new_params = self._backprop_gradients(old_params, gradient)
        self._logger.debug("New params: {}".format(new_params))
        self._policy.params = new_params

        self._step = self._step + 1

        return new_params

    def __iter__(self):

        yield ("solver_type", "stochastic_perturbation")
        yield ("learning_rate", dict(self._learning_rate_scheduler))
        yield ("loss_samples_per_training_step", self._loss_samples_per_step)

    def __repr__(self):
        return "Stochastic perturbation solver with maximum steps: {}, initial learning rate scheduler: {}".format(
            self._maximum_steps, self._learning_rate_scheduler
        )

    def _compute_gradient(self, old_params):

        dimensions = len(old_params)

        perturbation_vector = np.random.binomial(1, 0.5, dimensions).astype(np.float64)
        perturbation_vector[np.isclose(perturbation_vector, 0)] = -1

        self._logger.debug("Perturbation: {}".format(perturbation_vector))

        param1 = old_params + perturbation_vector
        param2 = old_params - perturbation_vector
        self._logger.debug("Parameters under test: {} - {}".format(param1, param2))

        self._policy.params = param1
        self._logger.debug("Begin evaluation step 1")

        loss_accumulator = np.float64(0)
        for i in range(self._loss_samples_per_step):
            self._logger.debug("Evaluation step 1, iteration {}".format(i))
            loss_accumulator = loss_accumulator + self._policy.evaluate(
                self._process, self._estimator
            )
        self._logger.debug("End evaluation step 1")
        expected_loss_param_1 = loss_accumulator / np.float64(
            self._loss_samples_per_step
        )

        loss_accumulator = np.float64(0)
        self._policy.params = param2
        self._logger.debug("Begin evaluation step 2")
        for i in range(self._loss_samples_per_step):
            self._logger.debug("Evaluation step 2, iteration {}".format(i))
            loss_accumulator = loss_accumulator + self._policy.evaluate(
                self._process, self._estimator
            )
        self._logger.debug("End evaluation step 2")
        expected_loss_param_2 = loss_accumulator / np.float64(
            self._loss_samples_per_step
        )

        self._logger.debug(
            "Losses 1, 2: {}, {}".format(expected_loss_param_1, expected_loss_param_2)
        )

        gradient = np.zeros(dimensions, dtype=np.float64)

        for i, _ in enumerate(gradient):
            gradient[i] = (expected_loss_param_1 - expected_loss_param_2) / (
                2 * perturbation_vector[i]
            )

        self._logger.debug("Gradient: {}".format(gradient))

        return gradient

    def _backprop_gradients(self, old_params, gradient):
        """

        Returns:
            (numpy ndarray float64): [description]
        """

        learning_rate = self._learning_rate_scheduler(self._step, self._maximum_steps)
        self._logger.debug("Learning rate: {}".format(learning_rate))
        new_params = old_params - learning_rate * gradient
        return new_params


class SolverFactory:
    def _get_solver(
        self,
        process,
        estimator,
        policy,
        maximum_steps=100,
        initial_learning_rate=1,
        solver_type="stochastic_perturbation",
        **kwargs
    ):

        if solver_type == "stochastic_perturbation":
            return StochasticPerturbation(
                process,
                estimator,
                policy,
                maximum_steps,
                initial_learning_rate,
                **kwargs
            )

