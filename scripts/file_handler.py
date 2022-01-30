import json

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


def get_response(file_name, geo_location):
    with open(file_name, 'r') as r_file:
        data = dict(json.load(r_file))
        if geo_location in data.keys():
            return data[geo_location]
    return False


def get_all_geo_locations():
    with open(LOG_DIR+GEO_LOCATIONS, 'r') as r_file:
        data = dict(json.load(r_file))
        return data.keys()