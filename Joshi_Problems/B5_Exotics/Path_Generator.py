import numpy as np


class PathGenerator():
    """
    Generates Path for MC simulation using provided random generator
    """
    def __init__(self, spot, r, d, vol, times):
        self._spot = spot
        self._log_spot = np.log(self._spot)
        self._r = r
        self._d = d
        self._vol = vol  # annual volatility
        self._times = times  # averaging period
        self._times_num = len(self._times)
        self._generator = Generator(len(self._times))
        self._variance = self._vol ** 2

        # path set up:
        self.spot_values = np.zeros(self._times_num)

    def get_path(self):
        variates = self._generator.get_gaussians()

        current_log_spot = np.log(self._spot)  # initial value
        spot_values = np.zeros(self._times_num)
        # Initial Step:
        drift = self._r - self._d - 0.5 * self._vol ** 2
        dt = self._times[0]
        # log(s_0) + drift
        current_log_spot = self._log_spot + drift * dt + self._vol * np.sqrt(dt) * variates[0]
        spot_values[0] = np.exp(current_log_spot)
        # from 1 since we have original jump already.

        # slow part this loop can be re-written as Matrix manipulation to be faster
        # I have already array of variates so applying array x array to get individual path components will speed things up.
        for j in range(1, self._times_num):
            dt = self._times[j] - self._times[j - 1]
            current_log_spot += drift * dt + self._vol * np.sqrt(dt) * variates[j]
            spot_values[j] = np.exp(current_log_spot)
        self.spot_values = spot_values


class Generator:
    def __init__(self, length=1):
        self._length = length

    def get_gaussians(self):
        variates = np.random.normal(size=self._length)
        return variates
