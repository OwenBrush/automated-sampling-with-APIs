import requests
import time
import json
import os
import time

from requests.models import Response


GEO_LOCATION_SAVE = './data/geo_locations.json'
FS_VENUES_SAVE = './data/foursquare_venue_search.json'
YELP_VENUES_SAVE = './data/yelp_venues_save.json'
COUNTRY_SAVE = './data/countries.json'
GOOGLE_VENUES_SAVE = './data/google_venues_save.json'

GEO_LOCATION_URL = 'https://api.3geonames.org/.json?randomland=yes'

FS_SEARCH_URL = "https://api.foursquare.com/v2/venues/search?"
FS_ID = os.environ["FOURSQUARE_CLIENT_ID"]
FS_PASS = os.environ["FOURSQUARE_CLIENT_SECRET"]

YELP_SEARCH_URL = 'https://api.yelp.com/v3/businesses/search'
YELP_ID = os.environ["YELP_ID"]
YELP_PASS = os.environ["YELP_KEY"]

GOOGLE_PLACE_URL = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?'
GOOGLE_KEY = os.environ["GOOGLE_PLACES_KEY"]

NOMINATIM_URL = 'https://nominatim.openstreetmap.org/reverse?format=jsonv2&zoom=3&accept-language=en-us&'

### File handling

def save_response_to_file(entry, file):
    with open(file, 'r') as r_file:
        data = json.load(r_file)
        data.append(entry)
        with open(file, 'w') as w_file:
            json.dump(data,w_file)


def entry_exists(cords, file):
    return cords in [x['geo_location'] for x in json.load(open(file))]


### Automated Data Collection

def collect_random_samples(number):
    for i in range(number):
        cords = request_random_geo_location()
        if cords:
            request_foursquare_venues(cords)
            request_yelp_venues(cords)
            request_country_from_nominatim(cords)
            requset_places_from_google(cords)
        else:
            Print(f"Ending sample collection after {i} samples collection: Geo location not recieved")
            break
        time.sleep(1.5)

### API request functions

def request_random_geo_location():
    response = requests.get(GEO_LOCATION_URL)
    if response:
        jres = json.loads(response.text)
        if 'nearest' in jres.keys():
            geo_location = jres['nearest']['latt']+", "+jres['nearest']['longt']
            if entry_exists(geo_location,GEO_LOCATION_SAVE):
                print('duplicate geo_location reject')
                return False
            
            parsed_response = {'geo_location': geo_location, 'geo_data' : jres}
            save_response_to_file(parsed_response, GEO_LOCATION_SAVE)
            return geo_location       
            
    print("3geonames Request Failed: {}".format(response.status_code))
    print(response.text)
    return False


def request_foursquare_venues(cords): 
    if entry_exists(cords, FS_VENUES_SAVE):
        return

    parsed_response = {'geo_location': cords, 'four_square_venues': None}
    response = requests.get(f'{FS_SEARCH_URL}ll={cords}&client_id={FS_ID}&client_secret={FS_PASS}&v=20201010')
    if response:
        jres = json.loads(response.text)
        if 'response' in jres.keys() and 'venues' in jres['response'].keys():
            parsed_response['four_square_venues'] = []
            for venue in jres['response']['venues']:
                parsed_response['four_square_venues'].append(venue)
        save_response_to_file(parsed_response, FS_VENUES_SAVE)
        return parsed_response
        
    print("FourSquare Request Failed: {}".format(response.status_code))
    print(response.text)
    return

def request_yelp_venues(cords):
    if entry_exists(cords, YELP_VENUES_SAVE):
        return
    parsed_response = {'geo_location': cords, 'yelp_venues': None}
    
    cords=cords.split(', ')
    headers = {'Authorization': 'Bearer {}'.format(YELP_PASS)}
    params = {'latitude': cords[0], 'longitude': cords[1]}
    
    response = requests.get(YELP_SEARCH_URL, headers=headers, params=params, timeout=5)
    if response:
        jres = json.loads(response.text)
        if 'businesses' in jres.keys():
            parsed_response['yelp_venues'] = jres
            save_response_to_file(parsed_response, YELP_VENUES_SAVE)
        return parsed_response

    print("Yelp Request Failed: {}".format(response.status_code))
    print(response.text)


def request_country_from_nominatim(cords):
    if entry_exists(cords, COUNTRY_SAVE):
        return
    parsed_response = {'geo_location': cords, 'country': None}      
        
    cords=cords.split(', ')
    response = requests.get(f'{NOMINATIM_URL}lat={cords[0]}&lon={cords[1]}')
    if response:
        response = json.loads(response.text)
        if 'name' in response.keys():
            parsed_response['country'] = response['name']        
        save_response_to_file(parsed_response, COUNTRY_SAVE)
        return parsed_response
        
    print("Nominatim Request Failed: {}".format(response.status_code))
    print(response.text)
        
def requset_places_from_google(cords):
    if entry_exists(cords, GOOGLE_VENUES_SAVE):
        return
    
    parsed_response = {'geo_location': cords, 'google_places': None}  
    response = requests.get('{}location={}&radius=5000&key={}'.format(GOOGLE_PLACE_URL,cords,GOOGLE_KEY))
    if response:
        jres = json.loads(response.text)
        if jres['status'] == 'OK':
            parsed_response['google_places'] = jres['results']
        save_response_to_file(parsed_response, GOOGLE_VENUES_SAVE)
        return jres
    
    print("Google Request Failed: {}".format(response.status_code))
    print(response.text)
    return response
