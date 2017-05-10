#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, division
import math
import matplotlib
import matplotlib.pyplot as plt
from quote.google_option_chain_quote import GoogleOptionChainQuote


class OptionChain(object):
    def __init__(self, ticker, quote_class):
        self.quote = quote_class(ticker)
        self.options = []

    def request(self):
        pass

    def plot_volatility_smile(self):
        pass


if __name__ == '__main__':
    ticker = 'AAPL'
    quote_class = GoogleOptionChainQuote

    option_chain = OptionChain(ticker, quote_class)
    option_chain.plot_volatility_smile()
