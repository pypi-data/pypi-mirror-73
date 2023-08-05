import os

class Company(object):


    def __init__(self,  ticker,
                 u      = None,
                 header = True):

        # Stores cik internally
        self.ticker = ticker

        # Get data and library directories.
        self.LIBDIR  = os.path.dirname(os.path.realpath(__file__))
        self.DATADIR = os.path.join(self.LIBDIR,'..','..','..','data','yahoo')

    def get_ts_price_df(self,u):
        return u.map['ts_price'][self.ticker]['prices']

    def get_ts_dividend_df(self,u):
        return u.map['ts_price'][self.ticker]['dividends']

    def get_ts_split_df(self,u):
        return u.map['ts_price'][self.ticker]['splits']

    def prices(self,u):
        return self.get_ts_price_df(u)
    
    def dividends(self,u):
        return self.get_ts_dividend_df(u)

    def to_csv(self,u,res):

        # Resolver cik ticker transform 
        cik = res.resolve(self.ticker,'ticker','cik')

        out_path = os.path.join(self.DATADIR,'..','clean',str(cik))
        # TS Price: prices
        self.get_ts_price_df(u).to_csv(os.path.join(out_path,'prices.csv'))

        # TS Price: dividends 
        self.get_ts_dividend_df(u).to_csv(os.path.join(out_path,'dividends.csv'))

    def plot(self,u,show = False):

        ax_map = {}

        ts_price_df = self.get_ts_price_df(u)
        ax_map['prices'] = ts_price_df.plot(kind = 'line',figsize = (20,10))

        ts_dividend_df = self.get_ts_dividend_df(u)
        ax_map['dividends'] = ts_dividend_df.plot(kind = 'bar',figsize = (20,10))

        return ax_map