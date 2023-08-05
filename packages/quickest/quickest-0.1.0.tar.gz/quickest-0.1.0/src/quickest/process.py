import logging

import numpy as np

from .dynamics import DynamicsFactory
from .sensor import GaussianSensorMixin
from .cost import CostFactory


class Process(DynamicsFactory, GaussianSensorMixin, CostFactory):
    """A change process class. 
    A change process is a controlled process whose hidden state includes information 
    about when a change point occurred.
    This class should be initialised from a dictionary (keyword arguments) containing configuration for:
    1. a process,
    2. a sensor, and 
    3. a cost function.
    """

    def __init__(
        self,
        pre_change_states=[0],
        post_change_states=[1],
        process_duration=200,
        **kwargs
    ):
        """Change process constructor. 
        The additional keyword arguments must contain configuration for a process, a sensor, and a cost function.

        Args:
            pre_change_states (list, optional): The 0-indexed states that occur before the change. Defaults to [0].
            post_change_states (list, optional): The 0-indexed states that occur after the change. Defaults to [1].
            process_duration (int, optional): The runtime of a process in steps if it is not interrupted. Defaults to 200.
        """

        self._logger = logging.getLogger(__name__)
        logging.basicConfig(level="DEBUG")

        self._process_duration = process_duration
        self._pre_change_states = pre_change_states
        self._post_change_states = post_change_states
        self._dynamics = self._init_dynamics(**kwargs["dynamics"])
        self._sensor = self._init_sensor(**kwargs["sensor"])
        self._cost_function = self._init_cost_function(**kwargs["cost_function"])

        self.reset()

    def __call__(self, control_input):

        old_state = self._hidden_state
        new_state = self._dynamics(old_state, control_input, self._simulation_time)

        if (np.isnan(self._change_time)) and not (new_state in self._pre_change_states):

            self._logger.debug(
                "Change point at k={}, new state: {}".format(
                    self._simulation_time, new_state
                )
            )
            self._change_time = self._simulation_time

        measurement = self._sensor(new_state)

        cost = self._cost_function(
            new_state,
            control_input,
            self._process_duration,
            self._simulation_time,
            self._change_time,
        )

        if (not np.isclose(cost, 0)) and (
            not np.isclose(cost, self._cost_function.false_alarm_cost)
        ):
            self._logger.debug("Cost from delay: {}".format(cost))

        self._history[self._simulation_time] = new_state
        self._hidden_state = new_state

        self._simulation_time = self._simulation_time + 1

        return measurement, cost

    def __iter__(self):
        yield ("process_duration", self._process_duration)
        yield ("pre_change_states", self._pre_change_states)
        yield ("post_change_states", self._post_change_states)
        yield ("dynamics", dict(self._dynamics))
        yield ("cost_function", dict(self._cost_function))
        yield ("sensor", dict(self._sensor))

    def __repr__(self):
        repstr = "Change process with \nDynamics: {}\nSensor: {}\nCost function: {}".format(
            self._dynamics, self._sensor, self._cost_function
        )
        return repstr

    def sample_initial_belief(self):
        return self._dynamics.initial_distribution

    def reset(self):

        self._history = np.zeros(self._process_duration, dtype=np.uint8)
        self._simulation_time = 0
        self._hidden_state = self._dynamics.reset()
        self._change_time = np.nan

    @property
    def num_states(self):
        return len(self._post_change_states) + len(self._pre_change_states)

    @property
    def pre_change_states(self):
        return self._pre_change_states

    @property
    def post_change_states(self):
        return self._post_change_states

    @property
    def history(self):
        return np.array([state + 1 for state in self._history])

    @property
    def change_time(self):
        return self._change_time

    @property
    def hidden_state(self):
        return self._hidden_state

    @property
    def maximum_duration(self):
        return self._process_duration

    @property
    def simulation_clock(self):
        return self._simulation_time

    @property
    def transition_matrix(self):
        return self._dynamics.transition_matrix

    @property
    def observation_pdfs(self):
        return self._sensor.observation_pdfs

