### Project Goal:

  * Illustrate how a network of APIs can be used in unison for data collection to create a unified dataset with wide reaching and varied samples.

### API Network:

  1. 3geonames is called to generate a random geolocation on land.
  2. With the geolocation, every other API is called to collect information on that location.
  3. Every response is saved into json dictionaries, using the geo location as a key.
  4. Scripts can then build dataframes to specification with all available data from called geo locations. 

![Alt text](/flowchart.png?raw=true "API Network flowchart")

### APIs used:
  * https://api.3geonames.org/
  * https://nominatim.openstreetmap.org
  * https://api.foursquare.com
  * https://api.yelp.com
  * https://maps.googleapis.com

### Results:
      From 431 samples:
 
      Four Square:
      2765.0 venues across 52 countries
      
 
      Google:
      158.0 venues across 15 countries
      
 
      Yelp:
      283.0 venues across 11 countries
 
 ### Average results per request by company:
      
![Alt text](/four_square.png?raw=true "API Network flowchart")
  
![Alt text](/yelp.png?raw=true "API Network flowchart")
    
![Alt text](/google.png?raw=true "API Network flowchart")

 ### Comparison between companies, by total number of results: 
![Alt text](/comparison.png?raw=true "API Network flowchart")


 ### Notes
 - This is a very small dataset for such large comparisons, the intention is to show the concept not create actual meaningful comparisons.
 - Each API is returning different types of results that might not make sense to compare (ie. land marks vs. pubs).
 - Each API also has different radius from the given location.
 - Each API also has different caps on the maximum number of results it can reutrn.
 - Most random locations will be rural, which provide very different results from urban geo locations.

 ### Next Steps:
 - Create function for retrieving detailed information from different venues at given location.
