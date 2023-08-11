#import folium
import requests, time, json
#from bs4 import BeautifulSoup
from keys import shipID

url = 'https://www.marinetraffic.com/map/getvesseljson/shipid:' + shipID


#url = 'https://www.marinetraffic.com/en/ais/details/ships/shipid:1192924/mmsi:368958000/imo:0/vessel:US_GOV_VESSEL'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Referer': 'https://www.marinetraffic.com/en/ais/home/centerx:-76.3/centery:37.0/zoom:10'

}

r = requests.get(url, headers=headers)

 # this if statement checks status of request
if r.status_code != 200:
    while True:
        print(str(r))
        time.sleep(15)
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            break

shipJson = r.json()
