# product spec
# Payoff to define calls/puts etc
import numpy as np


class Payoff:
    def __init__(self, strike):
        self._strike = strike


class PayoffCall(Payoff):
    def __init__(self, strike):
        self._strike = strike

    def get_payoff(self, spot):
        return max(spot - self._strike, 0)


class PayoffPut(Payoff):
    def __init__(self, strike):
        self._strike = strike

    def get_payoff(self, spot):
        return max(self._strike - spot, 0)


class Product:
    "Product base for handling cashflows for different types of options "

    def __init__(self):
        pass

    def cash_flow(spot_values):
        pass


class AsianOption(Product):
    def __init__(self, expiry, strike, payoff):
        # super.__init__()
        self.strike = strike
        self.expiry = expiry
        self.payoff = payoff

    def get_cashflow(self, spot_values):
        spot_sum = np.sum(spot_values)  # Sum j=1...n over setting dates
        spot_mean = spot_sum / len(spot_values)  # take a avg
        cashflow = self.payoff.get_payoff(spot_mean)
        return cashflow


class BarrierDownOut(Product):
    def __init__(self, expiry, strike, barrier, payoff):
        self.strike = strike
        self.expiry = expiry
        self.barrier = barrier
        self.payoff = payoff

    def get_cashflow(self, spot_values):
        # check for barrier in whole path for knock out part
        for val in spot_values:
            if (val <= self.barrier):
                return 0
        # did not hit barrier do payout:
        final_spot = spot_values[-1]
        cashflow = self.payoff.get_payoff(final_spot)
        return cashflow


class BarrierDownIn(Product):
    def __init__(self, expiry, strike, barrier, payoff):
        self.strike = strike
        self.expiry = expiry
        self.barrier = barrier
        self.payoff = payoff

    def get_cashflow(self, spot_values):
        # check for barrier in whole path and enable it

        for val in spot_values:
            # enabled check for price:
            if (val <= self.barrier):
                final_spot = spot_values[-1]
                cashflow = self.payoff.get_payoff(final_spot)
                return cashflow
        return 0
