import quandl
import matplotlib
import matplotlib.pyplot as plt
import logging

logger = logging.getLogger('quant')
matplotlib.style.use('ggplot')


class QuandlData(object):
    def __init__(self, ticker):
        self.ticker = ticker
        self.df = self.request_df()

    def request_df(self):
        try:
            return quandl.get(self.ticker)
        except Exception as e:
            logger.exception('Failed to download data')
            return None

    def plot(self):
        if self.df is not None:
            self.df.plot()
            plt.title(self.ticker)
        else:
            logger.error('No data available')

if __name__ == '__main__':
    tickers = [
        'CBOE/VIX',  # Volatility Index
        'CBOE/VXO',  # S&P 100 Volatility Index
        'CBOE/VXN',  # Nasdaq Volatility Index
        'CBOE/VXD',  # DJIA Volatility Index
    ]

    for ticker in tickers:
        quandl_data = QuandlData(ticker)
        quandl_data.plot()

    plt.show()
