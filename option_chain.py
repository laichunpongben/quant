#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, division
import math
import datetime
import matplotlib
import matplotlib.pyplot as plt
from european_option import EuropeanOption
from quote.google_option_chain_quote import GoogleOptionChainQuote

matplotlib.style.use('ggplot')


class OptionChain(object):
    def __init__(self, ticker, quote_class, equity_price, risk_free_rate=0.0):
        self.quote = quote_class(ticker)
        self.calls = []
        self.puts = []
        self.equity_price = equity_price
        self.risk_free_rate = risk_free_rate

    def request(self):
        self.quote.request()
        self.make_calls()
        self.make_puts()

    def make_calls(self):
        for c in self.quote.data_json['calls']:
            price = float(c['a'])
            s = self.equity_price
            k = float(c['strike'])
            r = self.risk_free_rate
            t = 37/252
            option_type = 'call'

            call = EuropeanOption(price, s, k, r, t, option_type)
            call.estimate_implied_volatility()
            self.calls.append(call)

    def make_puts(self):
        for p in self.quote.data_json['puts']:
            price = float(p['a'])
            s = self.equity_price
            k = float(p['strike'])
            r = self.risk_free_rate
            t = 37/252
            option_type = 'put'

            put = EuropeanOption(price, s, k, r, t, option_type)
            put.estimate_implied_volatility()
            self.puts.append(put)

    def plot_volatility_smile(self):
        option_dict = {'calls': self.calls, 'puts': self.puts}
        plt.title('Volatility Smile')
        plt.xlabel('Strike')
        plt.ylabel('Volatility')

        for k, v in option_dict.items():
            implied_volatilities = [option.implied_volatility for option in v]
            strikes = [option.k for option in v]
            plt.plot(strikes, implied_volatilities, label=k)

if __name__ == '__main__':
    ticker = 'AAPL'
    quote_class = GoogleOptionChainQuote
    equity_price = 153.96
    risk_free_rate = 0.0

    option_chain = OptionChain(ticker, quote_class, equity_price, risk_free_rate)
    option_chain.request()
    option_chain.plot_volatility_smile()

    plt.show()
