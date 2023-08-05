from scipy.stats import norm


class GaussianSensor:
    def __init__(self, observation_pdfs):

        self._params = observation_pdfs

    def __call__(self, state):
        observation = self._sense(state)
        return observation

    def __repr__(self):
        return "Sensor with additive white Gaussian noise. Observed distributions for each state: {}".format(
            self._params
        )

    def __iter__(self):

        yield("sensor_type", "Noisy Gaussian sensor")
        yield("observation_pdfs", self._params)

    def _sense(self, state):

        params = self._params[state]

        return norm.rvs(params["mu"], params["std"])

    @property 
    def observation_pdfs(self):
        return self._params



class GaussianSensorMixin:
    def _init_sensor(self, *args, **kwargs):

        return GaussianSensor(kwargs["observation_pdfs"])
