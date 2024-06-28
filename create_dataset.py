from datetime import datetime, timedelta
import requests

'''
    This script will take data from the NASA Near Earth Object Web Service,
    convert the data into a pandas DataFrame, and save the data to a CSV file.
'''

base_url = 'https://api.nasa.gov/neo/rest/v1/feed'


def weekly_dates(start_date, num_weeks):
    dates = []
    current_date = start_date
    for _ in range(num_weeks + 1):  # +1 to include the start date
        dates.append(current_date.strftime("%Y-%m-%d"))
        current_date -= timedelta(days=7)
    return dates

# Set the start date
start_date = datetime(2024, 6, 1)

# Generate dates for 10 weeks (adjust as needed)
date_list = weekly_dates(start_date, 10)

# Print the dates
for date in date_list:
    print(date)