from datetime import datetime, timedelta
from dotenv import load_dotenv
import csv
import json
import time
import requests
import os

'''
    This script will take data from the NASA Near Earth Object Web Service,
    convert the data into a JSON file that can loaded into a pandas DataFrame.
    - NEO or neo referes to Near Earth Object.

    Process:
    - Query the NASA API for a week's worth of NEO data (1 week period is
      defined by the API).
    - This initial query will provide a link to the previous week's data, and
      the script can continue to query the API for more data.
    - For each date within the 7 day period, the script will parse the NEO data
      and format it into a dictionary. These dictionaries will be the rows of
      the pandas DataFrame.
'''

# Load environment variables from .env file, and get the NASA API Key
load_dotenv()
api_key = os.getenv("NASA_API_KEY")

def parse_individual_neo(neo_data):
    '''
    This function will take data about a single NEO from the NASA API and return
    a formatted dictionary suitable for a pandas DataFrame.
    '''
    estimated_diameter_km = neo_data['estimated_diameter']['kilometers']
    close_approach_data = neo_data['close_approach_data'][0]
    relative_velocity = close_approach_data['relative_velocity']['kilometers_per_hour']
    miss_distance = close_approach_data['miss_distance']['kilometers']

    # 1: included in Sentry collision monitoring system, 0: not included
    sentry_object = 1 if neo_data['is_sentry_object'] == True else 0

    # 1: potentially hazardous, 0: not potentially hazardous
    hazardous = 1 if neo_data['is_potentially_hazardous_asteroid'] == True else 0

    formatted_dict = {
        'id':neo_data['id'],
        'name':neo_data['name'],
        'absolute_magnitude_h':neo_data['absolute_magnitude_h'], # intrinsic luminosity of the NEO
        'est_diameter_min':estimated_diameter_km['estimated_diameter_min'],
        'est_diameter_max':estimated_diameter_km['estimated_diameter_max'],
        'relative_velocity':relative_velocity, # relative velocity of the NEO to Earth in km/h
        'miss_distance':miss_distance, # in km
        'orbiting_body':"Earth", # planet or moon that the NEO orbits
        'sentry_object':sentry_object, 
        'is_potentially_hazardous':hazardous,

    }
    return formatted_dict

def parse_neo_results_dict(neo_dict):
    '''
    This function will take a dictionary of NEO data from the NASA API and return
    a list of formatted dictionaries.
        - The input dictionary has dates as keys, and a list of NEOs as values.
        - The output list will contain a formatted dictionary for each NEO.
    '''
    results = []
    for date in neo_dict.keys():
        for neo in neo_dict[date]:
            try:
                formatted_neo = parse_individual_neo(neo)
                if formatted_neo and formatted_neo not in results:
                    results.append(formatted_neo)
            except Exception as e:
                print(f"Error: {e}")
                print(f"Error parsing NEO: {neo['id']}")
                print(neo)
    return results

def retrieve_neo_data(nasa_url):
    '''
    NEO data will be found at the nasa_url, which will be a link to a chunk of
    data. This function will retrieve the data from the link and return the
    results and the link to the next chunk of data.
    '''
    request = requests.get(nasa_url)
    if request.status_code == requests.codes.ok:
        json_data = request.json()
        near_earth_objects = json_data['near_earth_objects']
        link = json_data['links']['previous']
        results = parse_neo_results_dict(near_earth_objects)
    else:
        results = []
        link = None
        print(f"Error: Unable to retrieve data from {nasa_url}.")
        
    return {'results':results, 'link':link}

def execute_data_retrieval(start_date_string="2024-06-01", attempts_count=52):
    '''
    Create the first request to the NASA API. The result will include a link
    to the next chunk of results, which can be used to retrieve more data.
    All results will be added to a list.
    '''
    nasa_url = 'https://api.nasa.gov/neo/rest/v1/feed'

    # Get the start and end dates
    start_date = datetime.strptime(start_date_string, "%Y-%m-%d")
    end_date = start_date - timedelta(days=7)
    request_kwargs = {
                        'api_key': api_key,
                        'start_date':start_date.strftime("%Y-%m-%d"),
                        'end_date': end_date.strftime("%Y-%m-%d"),
                    }

    request = requests.get(nasa_url, params=request_kwargs)

    if request.status_code == requests.codes.ok:
        total_results = []
        json_data = request.json()
        # use the previous link since we are going backwards in time from
        # June 1st, 2024
        previous_link = json_data['links']['previous']
        near_earth_objects = json_data['near_earth_objects']
        total_results += parse_neo_results_dict(near_earth_objects)
        # Do this same process over the last 52 weeks
        attempts = 0
        while attempts < attempts_count and previous_link is not None:
            print(f"attempt {attempts + 1}...")
            total_results += retrieve_neo_data(previous_link)['results']
            previous_link = retrieve_neo_data(previous_link)['link']
            attempts += 1
            time.sleep(1)
    else:
        total_results = []
        print("Error: Unable to retrieve data from the NASA API.")

    return total_results

def export_to_local_json_file(data, filename):
    '''
    This function will export a list of dictionaries to a JSON file for 
    convenient usage in creating pandas DataFrames.
    '''
    # Export without indentation to make the file more compact and faster
    # to read/write later.
    with open(filename, 'w') as f:
        json.dump(data, f)

def export_to_local_csv_file(data, filename):
    '''
    This function will export a list of dictionaries to a CSV file for 
    convenient usage in creating pandas DataFrames.
    '''
    # Open the file in write mode
    with open(filename, 'w', newline='') as f:
        # If data is not empty, proceed
        if data:
            # Use the keys of the first dictionary as fieldnames (column headers)
            fieldnames = data[0].keys()
            # Create a DictWriter object with the fieldnames
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            
            # Write the header (column names)
            writer.writeheader()
            
            # Write each dictionary as a row in the CSV
            for row in data:
                writer.writerow(row)


def main():
    '''
      Uncomment and execute if you need to create a local JSON file of NEO data.
      Alternatively, these functions can be called from another script.
    '''
    # print("...initiating data retrieval...")
    # date_string = '2023-05-01'
    # data = execute_data_retrieval(date_string, 150)
    # print("...data retrieval completed...")
    # print(f"Total NEOs retrieved: {len(data)}")
    # print("...exporting data to JSON file...")
    # file_path = 'resources/additional_neo_data.json'
    # export_to_local_json_file(data, file_path)


if __name__ == "__main__":
    main()