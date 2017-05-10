#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import re
import json
import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('google_option_chain_quote')


class GoogleOptionChainQuote(object):
    URL_PREFIX = 'https://www.google.com/finance/option_chain?q='
    URL_SUFFIX = '&output=json'

    def __init__(self, ticker):
        self.ticker = ticker
        self.data_json = None

    def request(self):
        self.data_json = self.request_google_json()

    def request_google_json(self):
        quote_url = '{0}{1}{2}'.format(self.URL_PREFIX, self.ticker, self.URL_SUFFIX)
        try:
            response = requests.get(quote_url)
            return response.json()
        except ValueError:  # json.decoder.JSONDecodeError in Python3
            return self.add_quotation_mark_to_key(response.text)
        except Exception as e:
            logger.exception('Failed to download data')
            return None

    @staticmethod
    def add_quotation_mark_to_key(dirty_json_str):
        clean_json_str = re.sub("(\\w+)\\s*:", '"\\1":', dirty_json_str)
        try:
            return json.loads(clean_json_str)
        except ValueError:
            logger.error('Invalid json')
            return None
        except Exception as e:
            logger.exception('Unhandled error')
            return None

if __name__ == '__main__':
    logging.getLogger("requests").setLevel(logging.WARNING)

    ticker = 'AAPL'
    google_option_chain_quote = GoogleOptionChainQuote(ticker)
    google_option_chain_quote.request()
    print(google_option_chain_quote.data_json)
