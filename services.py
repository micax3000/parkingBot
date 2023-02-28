import bs4 as bs
import urllib.request
import requests
import json
import numpy as np
from typing import List
from api import distance_api as DISTANCE_API

parking_slots_state = {}
def findSlots() -> List[str]:
    source = urllib.request.urlopen(
        'https://www.parking-servis.co.rs/garaze-i-parkiralista#6-slobodna-parking-mesta').read()
    soup = bs.BeautifulSoup(source, 'lxml')
    slots = soup.find('ul','parking-count').find_all('li')
    for slot in slots:
        parking_slots_state[slot.a.text] = (slot.a['href'].split('/')[-1],slot.span.text)
    print(parking_slots_state)
    return [f'{key}: {value[1]}' for key,value in zip(parking_slots_state.keys(), parking_slots_state.values())]

async def calculateDistances(latitude, longitude):
    #TODO: TESTIRAM SA MANJE DESTINACIJA, KAKO BIH USTEDEO NA POSLATIM REQUESTOVIMA. PROMENITI KADA ZAVRSIM
    dict_keys = list(parking_slots_state.values())[:-1]
    destinations = ''
    for key in dict_keys:
        if int(key[1]) > 0:
            key = key[0].split(',')
            destinations += key[0] + '%2C' + key[1] + '%7C'

    url = f'https://maps.googleapis.com/maps/api/distancematrix/json?' \
          f'origins={latitude}%2C{longitude}&destinations={destinations[:-3]}&key={DISTANCE_API}'
    response = requests.request("GET", url)
    data = dict(json.loads(response.text))
    distance_values = [x['duration']['value'] for x in data['rows'][0]['elements']]
    min_index = np.argmin(distance_values)

    print("Index of destination address with minimum distance:", min_index)
    print("Minimum distance:", distance_values[min_index])
    print("Destination address with minimum distance:", data['destination_addresses'][min_index])

    closest_parking_lot = list(parking_slots_state.keys())[min_index]
    print(parking_slots_state[closest_parking_lot][0])
    return closest_parking_lot, distance_values[min_index], parking_slots_state[closest_parking_lot][1], parking_slots_state[closest_parking_lot][0]