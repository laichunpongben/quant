#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, division
import math
from scipy.stats import norm
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('european_option')


class EuropeanOption(object):
    def __init__(self, price, s, k, r, t, option_type):
        self.price = price
        self.s = s
        self.k = k
        self.r = r
        self.t = t
        self.option_type = option_type
        self.implied_volatility = self.estimate_implied_volatility_closed_form()

    def d1(self, sigma):
        return (math.log(self.s / self.k) + (self.r + sigma**2 / 2) * self.t) / sigma / math.sqrt(self.t)

    def d2(self, sigma):
        return (math.log(self.s / self.k) + (self.r - sigma**2 / 2) * self.t) / sigma / math.sqrt(self.t)

    def calc_black_scholes_call_price(self, sigma):
        return self.s * norm.cdf(self.d1(sigma)) - self.k * math.exp(-self.r * self.t) * norm.cdf(self.d2(sigma))

    def calc_black_scholes_put_price(self, sigma):
        return self.k * math.exp(-self.r * self.t) * norm.cdf(-self.d2(sigma)) - self.s * norm.cdf(-self.d1(sigma))

    @staticmethod
    def calc_normal_first_derivative(x):
        return 1 / math.sqrt(2 * math.pi) * math.exp(-x**2 / 2)

    def calc_vega(self, sigma):
        return self.s * math.sqrt(self.t) * self.calc_normal_first_derivative(self.d1(sigma))

    def estimate_implied_volatility_closed_form(self):
        return math.sqrt(2 * math.pi / self.t) * self.price / self.s

    def estimate_implied_volatility_iteratively(self):
        for _ in range(100):
            vega = self.calc_vega(self.implied_volatility)
            if abs(vega) < 0.0001:
                break

            if self.option_type == 'call':
                price = self.calc_black_scholes_call_price(self.implied_volatility)
            else:
                price = self.calc_black_scholes_put_price(self.implied_volatility)

            if self.implied_volatility - (price - self.price) / vega > 0:
                self.implied_volatility += -(price - self.price) / vega
            else:
                break

if __name__ == '__main__':
    test_cases = [
        (14.00, 153.96, 140.0, 0.005, 37/252, 'call'),
        (9.30, 153.96, 145.0, 0.005, 37/252, 'call'),
        (5.31, 153.96, 150.0, 0.005, 37/252, 'call'),
        (2.55, 153.96, 155.0, 0.005, 37/252, 'call'),
        (1.06, 153.96, 160.0, 0.005, 37/252, 'call'),
        (0.43, 153.96, 165.0, 0.005, 37/252, 'call'),
        (1.80, 153.96, 150.0, 0.005, 37/252, 'put'),
        (4.05, 153.96, 155.0, 0.005, 37/252, 'put'),
        (7.75, 153.96, 160.0, 0.005, 37/252, 'put'),
        (11.56, 153.96, 165.0, 0.005, 37/252, 'put'),
    ]

    for test_case in test_cases:
        european_option = EuropeanOption(*test_case)
        logger.info('{0} k={1} price={2}'.format(european_option.option_type, european_option.k, european_option.price))
        european_option.estimate_implied_volatility_iteratively()
        logger.info('implied_volatility={0}'.format(european_option.implied_volatility))
