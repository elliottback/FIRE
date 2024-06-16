import datetime
import yfinance as yf
import pandas as pd
import os
import re

cache_dir = '../data/'

def strip_non_alpha(input_string):
    # Use regular expression to remove non-alphabetic characters
    return re.sub(r'[^a-zA-Z]', '', input_string)

def delete_file_if_old(file_path):
    # Get current date and time
    current_time = datetime.datetime.now()

    # Check if the file exists
    if os.path.exists(file_path):
        # Get file's modification time
        file_stat = os.stat(file_path)
        file_mtime = datetime.datetime.fromtimestamp(file_stat.st_mtime)

        # Calculate the difference between current time and file modification time
        time_diff = current_time - file_mtime

        # Check if file is older than 30 days
        if time_diff.days > 30:
            # Delete the file
            os.remove(file_path)
            print(f"Deleted old file: {file_path}")
        else:
            print(f"File {file_path} is not older than 30 days, not deleted.")
    else:
        print(f"File {file_path} does not exist.")

def getStockData(ticker = '^GSPC'):
    file_path = cache_dir + strip_non_alpha(ticker)

    delete_file_if_old(file_path)

    if os.path.exists(file_path):
        print(f"DataFrame read from {file_path}")
        return pd.read_csv(file_path)
    else:
        dataframe = getStockDataFromYFinance(ticker)
        dataframe.to_csv(file_path, index=False)
        print(f"DataFrame cached as {file_path}")
        return dataframe

def getStockDataFromYFinance( ticker ): # ^GSPC is the ticker symbol for S&P 500
    ticker = yf.Ticker(ticker)
    return ticker.history(period="max", auto_adjust=True, rounding=True)
