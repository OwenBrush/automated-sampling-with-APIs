import requests
import time
import json
import time

from scripts.constants import *


### File handling

def save_response_to_file(key:str, response:str, file:str): 
    """
    Args:
        key: geo-location associated with response
        response: response recieved from API in text format
        file: file location of save file containing json dictionary
    """   
    with open(file, 'r') as r_file:
        data = json.load(r_file)
        data[key] = response
        with open(file, 'w') as w_file:
            json.dump(data,w_file, indent=4)


def key_exists(key:str, file:str)->bool:
    """
    Checks if key is present in saved json dictionary
    """
    with open(file, 'r') as r_file:
        data = dict(json.load(r_file))
        return key in data.keys()



### Automated Data Collection

def collect_random_samples(number:int):
    for i in range(number):
        geo_location = request_random_geo_location()
        if geo_location:
            request_foursquare_venues(geo_location)
            request_yelp_venues(geo_location)
            request_country_from_nominatim(geo_location)
            requset_places_from_google(geo_location)
        else:
            print(f"Ending sample collection after {i} samples collection: Geo location not recieved")
            break
        time.sleep(DELAY_BETWEEN_CALLS)

### API request functions

def request_random_geo_location():
    response = requests.get(GEO_LOCATION_URL)
    if response:
        jres = json.loads(response.text)
        if 'nearest' in jres.keys():
            geo_location = jres['nearest']['latt']+", "+jres['nearest']['longt']
            if key_exists(geo_location,LOG_DIR+GEO_LOCATIONS):
                print('geo location already exists')
                return False
            
            # parsed_response = {'geo_location': geo_location, 'geo_data' : jres}
            save_response_to_file(key= geo_location,
                                  response= jres,
                                  file= LOG_DIR+GEO_LOCATIONS)
            return geo_location       
            
    print(f"3geonames Request Failed: {response.status_code}")
    print(response.text)
    return False


def request_foursquare_venues(geo_location:str): 
    if key_exists(geo_location, LOG_DIR+FOUR_SQUARE):
        print('four square response for geo location already exists')
        return

    # parsed_response = {'geo_location': cords, 'four_square_venues': None}
    response = requests.get(f'{FS_SEARCH_URL}ll={geo_location}&client_id={FS_ID}&client_secret={FS_PASS}&v=20201010')
    if response:
        jres = json.loads(response.text)
        # if 'response' in jres.keys() and 'venues' in jres['response'].keys():
        #     parsed_response['four_square_venues'] = []
        #     for venue in jres['response']['venues']:
        #         parsed_response['four_square_venues'].append(venue)
        save_response_to_file(  key= geo_location,
                                response= jres,
                                file= LOG_DIR+FOUR_SQUARE)
        return jres
        
    print(f"FourSquare Request Failed: {response.status_code}")
    print(response.text)
    return

def request_yelp_venues(geo_location:str):
    if key_exists(geo_location, LOG_DIR+YELP):
        print('four square response for geo location already exists')
        return
    
    # parsed_response = {'geo_location': cords, 'yelp_venues': None}
    cordinates=geo_location.split(', ')
    headers = {'Authorization': 'Bearer {}'.format(YELP_PASS)}
    params = {'latitude': cordinates[0], 'longitude': cordinates[1]}
    response = requests.get(YELP_SEARCH_URL, headers=headers, params=params, timeout=5)
    
    if response:
        jres = json.loads(response.text)
        # if 'businesses' in jres.keys():
            # parsed_response['yelp_venues'] = jres
        save_response_to_file(  key= geo_location,
                                response= jres,
                                file= LOG_DIR+YELP)
        return jres

    print(f"Yelp Request Failed: {response.status_code}")
    print(response.text)


def request_country_from_nominatim(geo_location:str):
    if key_exists(geo_location, LOG_DIR+COUNTRIES):
        print('nominatim response for geo location already exists')
        return
    # parsed_response = {'geo_location': cords, 'country': None}      
        
    cordinates=geo_location.split(', ')
    response = requests.get(f'{NOMINATIM_URL}lat={cordinates[0]}&lon={cordinates[1]}')
    if response:
        jres = json.loads(response.text)
        # if 'name' in response.keys():
        #     parsed_response['country'] = response['name']        
        save_response_to_file(  key= geo_location,
                                response= jres,
                                file= LOG_DIR+COUNTRIES)
        return jres
        
    print(f"Nominatim Request Failed: {response.status_code}")
    print(response.text)
        
def requset_places_from_google(geo_location:str):
    if key_exists(geo_location, LOG_DIR+GOOGLE):
        print('nominatim response for geo location already exists')
        return
    
    # parsed_response = {'geo_location': cords, 'google_places': None}  
    response = requests.get(f'{GOOGLE_PLACE_URL}location={geo_location}&radius=5000&key={GOOGLE_KEY}')
    if response:
        jres = json.loads(response.text)
        # if jres['status'] == 'OK':
        #     parsed_response['google_places'] = jres['results']
        save_response_to_file(  key= geo_location,
                                response= jres,
                                file= LOG_DIR+GOOGLE)
        return jres
    
    print("Google Request Failed: {}".format(response.status_code))
    print(response.text)
    return response
