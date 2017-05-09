import quandl
import matplotlib
import matplotlib.pyplot as plt


class QuandlData(object):
    def __init__(self, ticker):
        self.ticker = ticker
        self.df = self.get_df()

    def get_df(self):
        try:
            return quandl.get(self.ticker)
        except Exception as e:
            print(e)
            return None

    def plot(self):
        matplotlib.style.use('ggplot')
        self.df.plot()
        plt.title(self.ticker)
        plt.show()


if __name__ == '__main__':
    ticker = 'CBOE/VIX'
    quandl_data = QuandlData(ticker)
    quandl_data.plot()
