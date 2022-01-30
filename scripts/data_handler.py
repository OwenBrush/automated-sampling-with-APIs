
import pandas as pd
import numpy as np
import json

from scripts.constants import *
from scripts.file_handler import *

def update():
    pass

def add_sample(geo_location):
    # df = pd.read_csv(SAVE_DIR+RESULTS)
    entry = pd.Series()
    entry['geo_location'] = geo_location
    entry['country'] = get_country(geo_location)
    entry['city'] = get_city(geo_location)
    entry['yelp'] = get_yelp(geo_location)
    entry['four_square'] = get_four_square(geo_location)
    entry['google'] = get_google(geo_location)
    
    return entry

def get_country(geo_location):
    data = get_response(LOG_DIR+COUNTRIES, geo_location)
    if data: 
        return data['name']
    else:
        return np.nan
    
def get_city(geo_location):
    data = get_response(LOG_DIR+GEO_LOCATIONS, geo_location)
    if data: 
        return data['nearest']['city']
    else:
        return np.nan  
    
def get_yelp(geo_location):
    data = get_response(LOG_DIR+YELP, geo_location)
    if data: 
        return data['total']   
    else:
        return np.nan
    
def get_four_square(geo_location):    
    data = get_response(LOG_DIR+FOUR_SQUARE, geo_location)
    if data: 
        return len(data['response']['venues'])
    else:
        return np.nan 
    
def get_google(geo_location):
    data = get_response(LOG_DIR+GOOGLE, geo_location)
    if data: 
        value = 0
        for venue in data['results']:
            if 'business_status' in venue.keys():
                value += 1  
        return value
    else:
        return np.nan
        

