import os

### File structure
SAVE_DIRECTORY = './data'
LOG_DIRECTORY = SAVE_DIRECTORY+'/logs'

GEO_LOCATIONS = 'geo_locations.json'
FS_VENUES = 'foursquare_venue_search.json'
YELP_VENUES= 'yelp_venues_save.json'
COUNTRIES = 'countries.json'
GOOGLE_VENUES_ = 'google_venues_save.json'

### API Adresses
GEO_LOCATION_URL = 'https://api.3geonames.org/.json?randomland=yes'
FS_SEARCH_URL = "https://api.foursquare.com/v2/venues/search?"
YELP_SEARCH_URL = 'https://api.yelp.com/v3/businesses/search'
GOOGLE_PLACE_URL = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?'
NOMINATIM_URL = 'https://nominatim.openstreetmap.org/reverse?format=jsonv2&zoom=3&accept-language=en-us&'

### Authentication
FS_ID = os.environ["FOURSQUARE_CLIENT_ID"]
FS_PASS = os.environ["FOURSQUARE_CLIENT_SECRET"]
YELP_ID = os.environ["YELP_ID"]
YELP_PASS = os.environ["YELP_KEY"]
GOOGLE_KEY = os.environ["GOOGLE_PLACES_KEY"]

