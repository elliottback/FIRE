import pandas as pd
import data as data

def calculate_total_returns(start_date, monthly_investment, dividend_tax_rate):
    # Fetch historical data
    hist = data.getStockData( 'SPY' )

    # Ensure 'Date' column is a datetime index
    hist.index = pd.to_datetime(hist.index).tz_localize(None)

    print(hist.tail())

    # Prepare DataFrame to store investment history
    investments = pd.DataFrame(index=hist.index)
    investments['Investment'] = 0.0
    investments['Shares'] = 0.0
    investments['Total Shares'] = 0.0
    investments['Dividends'] = 0.0
    investments['Total Value'] = 0.0

    # Simulate the monthly investments
    total_shares = 0.0
    pd_start = pd.to_datetime(start_date)

    for date, row in hist.iterrows():
        if date < pd_start:
            continue

        if date.day == 1:  # Assuming investments are made at the start of each month
            shares_bought = monthly_investment / row['Open']
            total_shares += shares_bought
            investments.at[date, 'Investment'] = monthly_investment
            investments.at[date, 'Shares'] = shares_bought

        investments.at[date, 'Total Shares'] = total_shares

        # Calculate dividends and reinvest after tax
        if row['Dividends'] > 0:
            dividends_received = total_shares * row['Dividends']
            dividends_after_tax = dividends_received * (1 - dividend_tax_rate)
            shares_from_dividends = dividends_after_tax / row['Open']
            total_shares += shares_from_dividends
            investments.at[date, 'Dividends'] = dividends_after_tax
            investments.at[date, 'Total Shares'] = total_shares

        # Calculate total value of the portfolio
        investments.at[date, 'Total Value'] = total_shares * row['Close']

    return investments


# Example usage
start_date = '2020-01-01'
end_date = '2023-01-01'
monthly_investment = 1000  # $1000 per month
dividend_tax_rate = 0.15  # 15% tax on dividends

# Calculate total returns for the SPY index
returns = calculate_total_returns(start_date, monthly_investment, dividend_tax_rate)
print(returns.tail())
