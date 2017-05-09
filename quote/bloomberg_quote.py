#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import json
import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('bloomberg_quote')


class BloombergQuote(object):
    URL = 'http://www.bloomberg.com/markets/api/quote-page/'
    # Alternative API: http://www.bloomberg.com/markets/chart/data/1D/

    def __init__(self, ticker, security_type):
        self.ticker = ticker
        self.security_type = security_type
        self.data_json = None
        self.security_name = ''
        self.last_price = 0.0

    def request(self):
        self.data_json = self.request_bloomberg_json()
        self.security_name = self.get_security_name()
        self.last_price = self.get_last_price()

    def request_bloomberg_json(self):
        quote_url = '{0}{1}:{2}'.format(self.URL, self.ticker, self.security_type)
        try:
            response = requests.get(quote_url)
            return response.json()
        except Exception as e:
            logger.exception('Failed to download data')
            return None

    def get_last_price(self):
        if self.data_json:
            try:
                return self.data_json['priceTimeSeries'][-1]['lastPrice']
            except KeyError, TypeError:
                logger.exception('Invalid json')
                return self.get_prev_close()
        else:
            logger.error('No data json')
            raise NoBloombergDataException

    def get_prev_close(self):
        if self.data_json:
            try:
                return self.data_json['priceTimeSeries'][-1]['previousClosingPriceOneTradingDayAgo']
            except KeyError, TypeError:
                logger.exception('Invalid json')
                raise NoBloombergDataException
        else:
            logger.error('No data json')
            raise NoBloombergDataException

    def get_security_name(self):
        if self.data_json:
            try:
                return self.data_json['basicQuote']['name']
            except KeyError, TypeError:
                logger.exception('Invalid json')
                return ''
        else:
            logger.error('No data json')
            raise NoBloombergDataException


class NoBloombergDataException(Exception):
    pass

if __name__ == '__main__':
    logging.getLogger("requests").setLevel(logging.WARNING)

    ticker_types = [
        ('5', 'HK'),
        ('2388', 'HK'),
        ('1299', 'HK'),
        ('AAPL', 'US'),
        ('HSI', 'IND'),
        ('HSCEI', 'IND'),
        ('USDHKD', 'CUR'),
        ('HKDUSD', 'CUR'),
        ('SGDHKD', 'CUR'),
        ('JPYHKD', 'CUR'),
        ('GC1', 'COM')
    ]
    for item in ticker_types:
        try:
            bloomberg_quote = BloombergQuote(*item)
            logger.info('{0}:{1}'.format(bloomberg_quote.ticker, bloomberg_quote.security_type))
            bloomberg_quote.request()
            logger.info(bloomberg_quote.last_price)
        except NoBloombergDataException:
            logger.error('No Bloomberg data')
        except Exception as e:
            logger.exception('Unhandled exception')
