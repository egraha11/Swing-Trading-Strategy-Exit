import yfinance as yf
import numpy as numpy
import pandas as pd
import datetime as dt
from dateutil.relativedelta import relativedelta
from matplotlib import pyplot as plt
import numpy as np
import pandas_ta as ta
from Send_Email import SendText




class Exit_Strategy():

    def __init__(self):

        self.current_tickers=pd.read_csv("current_positions.csv")
        self.action = {"Symbol":self.current_tickers["Symbol"].values.tolist(), "Entry Price":[], "Current Price":[], "Signal":[], "TI":[]}

        self.current_tickers["Date"] = pd.to_datetime(self.current_tickers["Date"])

        self.fibb_level = .618


    def fibbanacci_exit(self, df, entry_date, entry_price):

        fibb_value = entry_price + ((df.loc[entry_date:, "Adj Close"].max() - entry_price) * self.fibb_level)

        if df.iloc[-1, 4] < fibb_value:
            return True
        else:
            return False
        

    def strategy(self):
        
        for index, row in self.current_tickers.iterrows():

            df = yf.download(row["Symbol"], start=row["Date"] - relativedelta(months=1), end=dt.datetime.now(), progress=False)
            #df = yf.download(row["Symbol"], start=row["Date"] - relativedelta(months=1), end=dt.datetime(2024,1,31), progress=False)

            #step one look at fibbinacci retracement of 61.8%
            fibb_action = self.fibbanacci_exit(df, row["Date"], row["Entry Price"])
            #last step if current price is lower than entry price 
            loss_action = True if df.iloc[-1, 4] < row["Entry Price"] else False

            if fibb_action or loss_action:
                self.action["Signal"].append("Sell")

                if loss_action:
                    self.action["TI"].append("loss")
                else:
                    self.action["TI"].append("Fibb")
            else:
                self.action["Signal"].append("Hold")
                self.action["TI"].append("Na")

            self.action["Entry Price"].append(row["Entry Price"])
            self.action["Current Price"].append(df.iloc[-1, 4])

        #print(self.action)

    #consolidate statistics and send email
    #def email(self):

        #df = pd.DataFrame.from_dict(self.action)

        #df = df.sort_values("Signal", ascending=False)

        #df["Entry Price"] = df["Entry Price"].round(2)
        #df["Current Price"] = df["Current Price"].round(2)

        #df["text data"] = df["Symbol"].str.cat(df[["Entry Price", "Current Price", "Signal", "TI", "metric", "obv flag"]].astype(str), sep=", ")
        
        #print(df["text data"])

        #email = SendText()
        #email.send_text(df["text data"].values)
          


exit_strategy = Exit_Strategy()
exit_strategy.strategy()
exit_strategy.email()