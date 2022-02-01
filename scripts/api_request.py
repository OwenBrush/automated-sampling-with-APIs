from urllib import response
import requests
import time
import json
import pandas as pd
import numpy as np

from scripts.constants import *
from scripts import file_handler
from scripts import dataframe_builder


### Automated Data Collection

def collect_random_samples(number:int):
    """Calls APIs and populates the results.csv with new entries, saving all response to log files
    """
    for i in range(number):
        geo_location = request_random_geo_location()
        if geo_location:
            request_foursquare_venues(geo_location)
            request_yelp_venues(geo_location)
            request_country_from_nominatim(geo_location)
            requset_places_from_google(geo_location)
            dataframe_builder.add_sample(geo_location)
        else:
            print(f"Ending sample collection after {i} samples collection: Geo location not recieved")
            break
        time.sleep(DELAY_BETWEEN_CALLS)
        
def request_missing_information():
    df = pd.read_csv(SAVE_DIR+RESULTS, index_col=0)
    for geo_location in df[df.isna().any(axis=1)].index:
        sample = df.loc[geo_location]
        nan_values = sample[sample.isna()].index
        if 'country' in nan_values:
            request_country_from_nominatim(geo_location)
        if 'yelp' in nan_values:
            request_yelp_venues(geo_location)     
        if 'four_square' in nan_values:
            request_foursquare_venues(geo_location)     
        if 'google' in nan_values:
            requset_places_from_google(geo_location)    
 
        
def handle_response(geo_location:str, response:response, log_file:str):
    """saves API response to file, if response failed saves as a False boolean
    """
    if response:
        data = json.loads(response.text)
    else:
        data = False
        print(f"{log_file} Request Failed: {response.status_code}")
        print(response.text)
    
    file_handler.save_response_to_file(  key= geo_location,
                            response= data,
                            file= log_file)
    return data


### API request functions

def request_random_geo_location():
    response = requests.get(GEO_LOCATION_URL)
    if response:
        jres = json.loads(response.text)
        if 'nearest' in jres.keys():
            geo_location = jres['nearest']['latt']+", "+jres['nearest']['longt']
            if file_handler.key_exists(geo_location,LOG_DIR+GEO_LOCATIONS):
                print('geo location already exists')
                return False
            
            file_handler.save_response_to_file(key= geo_location,
                                  response= jres,
                                  file= LOG_DIR+GEO_LOCATIONS)
            return geo_location       
            
    print(f"3geonames Request Failed: {response.status_code}")
    print(response.text)
    return False




def request_foursquare_venues(geo_location:str): 
    # if file_handler.key_exists(geo_location, LOG_DIR+FOUR_SQUARE):
    #     print('four square response for geo location already exists')
    #     return
    
    response = requests.get(f'{FS_SEARCH_URL}ll={geo_location}&client_id={FS_ID}&client_secret={FS_PASS}&v=20201010')
    
    return handle_response(geo_location, response, LOG_DIR+FOUR_SQUARE)


def request_yelp_venues(geo_location:str):
    # if file_handler.key_exists(geo_location, LOG_DIR+YELP):
    #     print('yelp response for geo location already exists')
    #     return
    
    cordinates=geo_location.split(', ')
    headers = {'Authorization': 'Bearer {}'.format(YELP_PASS)}
    params = {'latitude': cordinates[0], 'longitude': cordinates[1]}
    
    response = requests.get(YELP_SEARCH_URL, headers=headers, params=params, timeout=5)

    return handle_response(geo_location, response, LOG_DIR+YELP)


def request_country_from_nominatim(geo_location:str):
    # if file_handler.key_exists(geo_location, LOG_DIR+COUNTRIES):
    #     print('nominatim response for geo location already exists')
    #     return
    
    cordinates=geo_location.split(', ')
    
    response = requests.get(f'{NOMINATIM_URL}lat={cordinates[0]}&lon={cordinates[1]}')

    return handle_response(geo_location, response, LOG_DIR+COUNTRIES)
        
def requset_places_from_google(geo_location:str):
    # if file_handler.key_exists(geo_location, LOG_DIR+GOOGLE):
    #     print('google response for geo location already exists')
    #     return
    
    response = requests.get(f'{GOOGLE_PLACE_URL}location={geo_location}&radius=5000&key={GOOGLE_KEY}')

    return handle_response(geo_location, response, LOG_DIR+GOOGLE)
