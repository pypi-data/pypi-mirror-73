import numpy as np
from numpy import ndarray


class Belief(ndarray):
    def __new__(cls, array):
        array_ = np.array(array, dtype=np.float64)

        if not len(array_.shape) == 1:
            msg = "A belief state must be a vector"
            raise Exception(msg)

        array_sum = np.sum(array_)

        if not np.isclose(array_sum, 1):
            array_ = array_ / array_sum

        obj = array_.view(cls)
        return obj


class TransitionMatrix(ndarray):
    """Wraps a numpy array that must satisfy the following conditions:

        1. The sum of each row is numerically close to 1
        2. Matrix is square 
        3. Array is immutable
    """

    def __new__(cls, array):
        """Overloaded allocator

        Args:
            array (list or array): The values of the transition matrix
        """

        if isinstance(array, list):
            array_ = np.array(array, dtype=np.float64)
        elif isinstance(array, np.ndarray):
            array_ = array.astype(np.float64)
        else:
            msg = "Matrix must be a list or numpy array"
            raise TypeError(msg)

        if not len(array_.shape) == 2:
            msg = "Matrix array must be two-dimensional"
            raise Exception(msg)

        if not array_.shape[0] == array_.shape[1]:
            msg = "Matrix array must be square"
            raise Exception(msg)

        for i in range(array_.shape[0]):
            i_dist = array_[i, :]
            if not np.isclose(np.sum(i_dist), 1, rtol=1e-04):
                msg = "Row {} of transition matrix does not sum to 1".format(i + 1)
                raise Exception(msg)

        obj = array_.view(cls)
        return obj

    def __setitem__(self, key, value):
        msg = "A TransitionMatrix is immutable"
        raise Exception(msg)

    def transition_probabilities(self, i):
        """Returns the Markov Chain's transition probabilities for state i

        args:
            i [integer]: The state, 0 to N-1 if N is the number of states

        Returns:
            [tuple]: The transition probabilities for state i
        """

        return tuple(self[i, :])
