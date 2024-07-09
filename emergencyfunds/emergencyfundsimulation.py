import pandas as pd
import data as data
from datetime import date, timedelta
import holidays


def adjust_for_holidays_and_weekends_backward(pay_date: date, us_holidays: holidays.HolidayBase) -> date:
    while pay_date in us_holidays or pay_date.weekday() >= 5:  # 5: Saturday, 6: Sunday
        pay_date -= timedelta(days=1)
    return pay_date

def generate_bi_monthly_paydates(inputDate: date):
    # List to store the pay dates
    paydates = []

    # start year / month
    start_year = inputDate.year
    start_month = inputDate.month

    # US holidays for the given year(s)
    us_holidays = holidays.US(years=range(start_year, start_year + (num_months // 12) + 1))

    # Start from the specified year and month
    current_year = start_year
    current_month = start_month

    for _ in range(num_months):
        # 1st of the month
        first_pay_date = adjust_for_holidays_and_weekends_backward(date(current_year, current_month, 1), us_holidays)
        paydates.append(first_pay_date)

        # 15th of the month
        fifteenth_pay_date = adjust_for_holidays_and_weekends_backward(date(current_year, current_month, 15),
                                                                       us_holidays)
        paydates.append(fifteenth_pay_date)

        # Move to the next month
        if current_month == 12:
            current_month = 1
            current_year += 1
        else:
            current_month += 1

    return paydates

# Example usage:
start_year = 2023  # Example start year
start_month = 1  # Example start month
num_months = 12  # Number of months to generate pay dates for
paydates = generate_bi_monthly_paydates(start_year, start_month, num_months)
for paydate in paydates:
    print(paydate)

raise ("no")

def calculate_total_returns(start_date, monthly_investment, dividend_tax_rate):
    # Fetch historical data
    hist = data.getStockData( 'SPY' )

    # Ensure 'Date' column is a datetime index
    hist.index = pd.to_datetime(hist.index, utc=True)
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
    pd_start = pd.to_datetime(start_date).tz_localize(None)
    last_month = None

    for date, row in hist.iterrows():
        date = date.tz_localize(None)
        if date < pd_start:
            continue

        if last_month is None or date.month != last_month:  # Assuming investments are made at the start of each month
            shares_bought = monthly_investment / row['Open']
            total_shares += shares_bought
            investments.at[date, 'Investment'] = monthly_investment
            investments.at[date, 'Shares'] = shares_bought
            last_month = date.month

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
start_date = '2006-01-01'
monthly_investment = 1000  # $1000 per month
dividend_tax_rate = 0.15  # 15% tax on dividends

# Calculate total returns for the SPY index
returns = calculate_total_returns(start_date, monthly_investment, dividend_tax_rate)
print(returns.tail())