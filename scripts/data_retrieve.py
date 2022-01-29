
import pandas as pd
import os
import json

from pandas.core.frame import DataFrame

from scripts.api_request import GOOGLE_VENUES_SAVE

GEO_LOCATION_SAVE = './data/geo_locations.json'
FS_VENUES_SAVE = './data/foursquare_venue_search.json'
YELP_VENUES_SAVE = './data/yelp_venues_save.json'
COUNTRY_SAVE = './data/countries.json'
GOOGLE_VENUES_SAVE = './data/google_venues_save.json'


def get_geo_data():
    geo_data = json.load(open(GEO_LOCATION_SAVE))
    table = []
    for location in geo_data:
        entry= {'geo_location': location['geo_location'], 'city':location['geo_data']['nearest']['city']}
        table.append(entry)
    df = pd.DataFrame(table)
    return df

def get_four_square_data():
    fs_data = json.load(open(FS_VENUES_SAVE))
    df = pd.json_normalize(fs_data)
    df['four_square_venues'] = df['four_square_venues'].apply(len)
    return df
    
def get_yelp_data():
    ####! BUILD ENTRY LIKE GEO DATA
    yelp_data = json.load(open(YELP_VENUES_SAVE))
    table = []
    # return yelp_data
    for location in yelp_data:
        entry = {'geo_location': location['geo_location'], 'yelp_venues': location['yelp_venues']['total']}
        table.append(entry)
    return pd.DataFrame(table)


def get_google_data():
    google_data = json.load(open(GOOGLE_VENUES_SAVE))
    # return google_data
    table = []
    for location in google_data:
        venues = 0
        if location['google_places']:
            for place in location['google_places']:
                if 'business_status' in place.keys():
                    venues += 1  
        entry = {'geo_location': location['geo_location'], 'google_venues': venues}
        table.append(entry)
    return pd.DataFrame(table)

def get_nominatim_data():
    nominatim_data = json.load(open(COUNTRY_SAVE))
    return pd.DataFrame(nominatim_data)