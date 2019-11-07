# IMPORTS
import pandas as pd
import math
import os.path
import time
from binance.client import Client
from datetime import timedelta, datetime
from dateutil import parser
from tqdm import tqdm_notebook #(Optional, used for progress-bars)
from dotenv import load_dotenv

### API
load_dotenv()
binance_api_key = os.getenv("BINANCE_API_KEY")
binance_api_secret = os.getenv("BINANCE_API_SECRET")

### CONSTANTS
binsizes = {"1m": 1, "5m": 5, "1h": 60, "4h": 240, "1d": 1440}
batch_size = 750
binance_client = Client(api_key=binance_api_key, api_secret=binance_api_secret)

### FUNCTIONS
def minutes_of_new_data(symbol, kline_size, data, source):
    old = datetime.strptime('1 Jan 2017', '%d %b %Y')
    new = pd.to_datetime(binance_client.get_klines(symbol=symbol, interval=kline_size)[-1][0], unit='ms')
    return old, new

def get_all_binance(symbol, kline_size, save = False):

    data_df = pd.DataFrame()

    oldest_point, newest_point = minutes_of_new_data(symbol, kline_size, data_df, source = "binance")
    delta_min = (newest_point - oldest_point).total_seconds()/60
    available_data = math.ceil(delta_min/binsizes[kline_size])

    print('Downloading all available %s data for %s. Be patient..!' % (kline_size, symbol))
    
    klines = binance_client.get_historical_klines(symbol, kline_size, oldest_point.strftime("%d %b %Y %H:%M:%S"), newest_point.strftime("%d %b %Y %H:%M:%S"))

    parsedSymbol = symbol[0:-3]+ "_"+ symbol[-3:]
    filename = './binance/%s-%s.json' % (parsedSymbol, kline_size)
    
    with open(filename, 'w') as f:
        f.write("[")

        print("Total number of candles: {}".format(len(klines)))
       
        for i, item in enumerate(klines):
            item = item[0:6]
            item[1] = float(item[1])
            item[2] = float(item[2])
            item[3] = float(item[3])
            item[4] = float(item[4])
            item[5] = float(item[5])
             
            if i != len(klines)-1:
                f.write("%s," % item)
            else:
                f.write("%s" % item)

        f.write("]")
        

# For Binance
binance_symbols = [
            "LTCBTC",
            "ETCBTC",
            "DASHBTC",
            "ZECBTC",
            "XLMBTC",
            "XMRBTC",
            "XRPBTC",
            "BNBBTC",
            "LINKBTC",
            "EOSBTC",
            "TRXBTC",
            "ADABTC",
            "IOTABTC",
            "XEMBTC"
]

for symbol in binance_symbols:
    get_all_binance(symbol, '4h', save = True)
