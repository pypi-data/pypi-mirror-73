import logging

import numpy as np


class CostFunction:
    """Abstract base class for a cost function for a change process.
    """
    def __init__(self, *args, **kwargs):
        self._logger = logging.getLogger(__name__)
        logging.basicConfig(level="DEBUG")

    def __call__(self, *args, **kwargs):
        cost = self._evaluate(*args, **kwargs)
        return cost

    def _evaluate(
        self,
        hidden_state,
        control_input,
        process_duration,
        simulation_time,
        change_time,
    ):
        raise NotImplementedError


class DetectionCost(CostFunction):
    """The simplest type of stopping cost that allocates either
    1. a false alarm cost or 
    2. cost per time step delay when the change is declared.
    This detector only accepts two types of actions/ state: 0 (no change) or 1 (change)
    """

    def __init__(self, false_alarm_cost, delay_cost):

        super().__init__()

        self._false_alarm_cost = false_alarm_cost
        self._delay_cost = delay_cost

    def __repr__(self):
        repstr = "Simple detection cost function with {} cost per time step delay and {} for false alarms".format(
            self._delay_cost, self._false_alarm_cost
        )
        return repstr

    def __iter__(self):
        yield ("cost_function_type", "simple_detection_cost")
        yield ("false_alarm_cost", self._false_alarm_cost)
        yield ("delay_cost", self._delay_cost)

    @property
    def false_alarm_cost(self):
        return self._false_alarm_cost

    def _evaluate(
        self,
        hidden_state,
        control_input,
        process_duration,
        simulation_time,
        change_time,
    ):
        """The class-specific implementation of __call__

        Args:
            old_state (int): 
            new_state (int): 
            control_input (int): 0 (continue) or 1 (stop)
            process_duration (int): The maximum number of steps the process may run for
            simulation_time (int, optional): [description]. Defaults to 0.
            change_time (int or numpy.nan): If a change has occured, change_time is the time step that the change occurred. 
            If no change occured, it is numpy.nan.

        Returns:
            numpy float64: cost incurred for the most recent action
        """

        # TODO REMOVE HIDDEN STATE, SIMPLE DETECTOR DOESN'T CARE

        cost = 0

        if control_input == 1:

            if not np.isnan(change_time):
                time_since_change = simulation_time - change_time
                cost = np.float64(self._delay_cost) * np.float64(time_since_change)

            else:
                cost = self._false_alarm_cost

        elif simulation_time == process_duration:

            if not np.isnan(change_time):
                time_since_change = simulation_time - change_time
                cost = self._delay_cost * time_since_change

        cost_ = np.float64(cost)

        if np.isnan(cost_):
            raise Exception(
                "Cost function computed nan cost. Control input: {}, hidden state: {}, simulation time: {}, change time: {}".format(
                    control_input, hidden_state, simulation_time, change_time
                )
            )

        return cost_


class IsolationCost(CostFunction):
    """The isolation cost must consider multiple possible outcomes of a change detection.
    1. Delay cost and correct detection
    2. Delay cost and incorrect detection
    3. False alarm
    """

    def __init__(self, false_alarm_costs=[0], delay_costs=[0], **kwargs):
        """[summary]

        Args:
            false_alarm_costs (list): A vector of size N-1 where N is the number of possible states. 
            Contains the cost for declaring a false alarm of each type.
            delay_costs (list): A vector of size N-1 where N is the number of possible states. 
            Contains the per time unit delay for failing to detect each type of anomaly.
        """
        self.__false__alarm__costs = false_alarm_costs
        self.__delay__costs = delay_costs

    def _evaluate(self, hidden_state, control_input, simulation_time=0, change_time=0):

        cost = 0

        if control_input > 0:

            if control_input == hidden_state:

                time_since_change = simulation_time - change_time
                cost = self.__delay__costs[hidden_state - 1] * time_since_change

            else:
                cost = self.__false__alarm__costs[control_input - 1]

        return cost

    def __repr__(self):

        zipped_costs = zip(self.__delay__costs, self.__false__alarm__costs)

        reprstr = "Isolation cost function with (delay, false alarm) costs: "

        for i, state in zipped_costs:
            reprstr = reprstr + "\nState {}: {}".format(i, state)

        return reprstr


class CostFactory:
    """A mixin that other classes can inherit from in order to obtain different types of cost functions"""

    def _init_cost_function(self, cost_type="simple_detection_cost", **kwargs):

        if cost_type == "simple_detection_cost":
            cost_function = DetectionCost(
                kwargs["false_alarm_cost"], kwargs["delay_cost"]
            )

        # TODO OTHER TYPES OF COST eg ISOLATION ERROR

        return cost_function
