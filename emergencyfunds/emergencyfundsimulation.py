import pandas as pd
import data as data

spy = data.getStockData( 'SPY' )

print(spy.tail())