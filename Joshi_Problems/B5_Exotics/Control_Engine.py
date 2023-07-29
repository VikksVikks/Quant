import numpy as np

class ControlEngine():
    """
    calls path generator
    calls product definition
    discounts cash flow back to time zero
    averages result of all sims
    """
    def __init__(self, vol, d, r, spot, product, generator):
        self._vol = vol
        self._d = d
        self._r = r
        self._spot = spot
        self._product = product
        self._T = product.expiry

        self._generator = generator  # PathGenerator(spot, r, d , vol, times)
        # self._times = product.times

        # self._number_of_times = len(times)
        self._discount = np.exp(-self._r + self._d) * product.expiry  # only one discount - European !!!

        self._price_list = []
        self.cum_avg_list = []
        self.sqrt_err = 0
        self.option_price = 0
        self.last_path = 0

    def run_simulation(self, n_sims):
        self.price_list = []
        self.cum_avg_list = []
        for j in range(0, n_sims):
            # generate path calls gen
            self._generator.get_path()
            self.last_path = self._generator.spot_values
            # create cashflow
            cashflow = self._product.get_cashflow(self._generator.spot_values)
            # discount cashflow
            price = cashflow * self._discount
            # we wish to return inter averages as well:
            self.price_list.append(price)  # price of individual sim results

            self.cum_avg_list.append(np.mean(self.price_list))  # running average

        self.option_price = (np.mean(self.price_list))

        variance = (1 / (len(self.price_list) - 1)) * np.sum((self.price_list - self.option_price) ** 2)
        self.sqrt_err = np.sqrt(variance) / len(self.price_list)

        return self.option_price