from datetime import datetime, timedelta
from dotenv import load_dotenv
import json
import time
import requests
import os

'''
    This script will take data from the NASA Near Earth Object Web Service,
    convert the data into a JSON file that can loaded into a pandas DataFrame.
'''

# Load environment variables from .env file, and get the NASA API Key
load_dotenv()
api_key = os.getenv("NASA_API_KEY")

# Get the start and end dates
start_date = datetime(2024, 6, 1)
end_date = start_date - timedelta(days=7)

def parse_individual_neo(neo_data):
    '''
    This function will take a JSON object from the NASA NEO API and return a
    formatted dictionary suitable for a pandas DataFrame.
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
    results = []
    # NEO data is stored in a dictionary with dates as keys
    # iterate through each date, then parse each NEO into a formatted dictionary
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
    This function will retrieve data from the NASA NEO API and return a list of
    formatted dictionaries.
    '''
    request = requests.get(nasa_url)
    if request.status_code == requests.codes.ok:
        json_data = request.json()
        near_earth_objects = json_data['near_earth_objects']
        results = parse_neo_results_dict(near_earth_objects)
    else:
        results = []
        print(f"Error: Unable to retrieve data from {nasa_url}.")
        
    return {'results':results, 'link':json_data['links']['previous']}

def execute_data_retrieval():
    '''
    Create the first request to the NASA API. The result will include a link
    to the next chunk of results, which can be used to retrieve more data.
    All results will be added to a list.
    '''
    nasa_url = 'https://api.nasa.gov/neo/rest/v1/feed'
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
        while attempts < 52:
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
    This function will export a list of dictionaries to a JSON file.
    '''
    # Export without indentation to make the file more compact and faster
    # to read/write later.
    with open(filename, 'w') as f:
        json.dump(data, f)


def main():
    print("...initiating data retrieval...")
    data = execute_data_retrieval()
    print("...data retrieval completed...")
    print(f"Total NEOs retrieved: {len(data)}")
    print("...exporting data to JSON file...")
    file_path = 'resources/neo_data.json'
    export_to_local_json_file(data, file_path)


if __name__ == "__main__":
    main()