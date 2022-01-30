
import pandas as pd
import numpy as np
import json

from scripts.constants import *
from scripts.file_handler import get_all_geo_locations, get_response

def update():
    df = pd.read_csv(SAVE_DIR+RESULTS, index_col=0)
    for geo_location in get_all_geo_locations():
        if not geo_location in df.index:
            add_sample(geo_location)

def add_sample(geo_location):
    df = pd.read_csv(SAVE_DIR+RESULTS, index_col=0)
    
    entry = pd.Series(name = geo_location)
    entry['country'] = get_country(geo_location)
    entry['city'] = get_city(geo_location)
    entry['yelp'] = get_yelp(geo_location)
    entry['four_square'] = get_four_square(geo_location)
    entry['google'] = get_google(geo_location)
    
    if not entry.name in df.index:
        df = df.append(entry)
    else:
        for column in df.columns:
            if column in entry.index:
                if entry[column]:
                    df.at[entry.name,column] = entry[column]
                    
    df.to_csv(SAVE_DIR+RESULTS)



def get_country(geo_location):
    data = get_response(LOG_DIR+COUNTRIES, geo_location)
    if data: 
        if 'name' in data.keys():
            return data['name']

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
        

