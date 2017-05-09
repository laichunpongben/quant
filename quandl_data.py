import quandl
import matplotlib
import matplotlib.pyplot as plt
import logging

logger = logging.getLogger('quant')


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
            matplotlib.style.use('ggplot')
            self.df.plot()
            plt.title(self.ticker)
            plt.show()
        else:
            logger.error('No data available')

if __name__ == '__main__':
    ticker = 'CBOE/VIX'
    quandl_data = QuandlData(ticker)
    quandl_data.plot()
