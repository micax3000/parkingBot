import urllib.request
import requests
import json
import threading
import pprint as pp
import datetime as dt
import bs4 as bs
from typing import List
from api import distance_api as DISTANCE_API

parking_slots_state = {}

def refreshTable(f_stop):
    findSlots()
    if not f_stop.is_set():
        threading.Timer(30, refreshTable, [f_stop]).start()
def findSlots() -> List[str]:
    print(f'findSlots run at: {dt.datetime.now()}')
    source = urllib.request.urlopen(
        'https://www.parking-servis.co.rs/garaze-i-parkiralista#6-slobodna-parking-mesta').read()
    soup = bs.BeautifulSoup(source, 'lxml')
    slots = soup.find('ul', 'parking-count').find_all('li')
    for slot in slots:
        parking_slots_state[slot.a['href'].split('/')[-1]] = (slot.a.text, slot.span.text)
    print(pp.pprint(parking_slots_state))
    return [f'{item[1][0]}: {item[1][1]}' for item in parking_slots_state.items()]


async def calculateDistances(latitude, longitude):
    distance_values = []
    addresses = []
    data = {}
    dict_keys = [item[0] for item in list(parking_slots_state.items()) if int(item[1][1]) > 0]
    for i in range(0, len(parking_slots_state.items()), 25):
        destinations = ''
        for key in dict_keys[i:i+25]:
            key = key.split(',')
            destinations += key[0] + '%2C' + key[1] + '%7C'
        if destinations != '':
            url = f'https://maps.googleapis.com/maps/api/distancematrix/json?' \
                  f'origins={latitude}%2C{longitude}&destinations={destinations[:-3]}&key={DISTANCE_API}'
            response = requests.request("GET", url)
            data = dict(json.loads(response.text))
            distance_values.extend([x['duration']['value'] for x in data['rows'][0]['elements']])
            addresses.extend(data['destination_addresses'])
    min_index = distance_values.index(min(distance_values))
    closest_parking_lot = parking_slots_state[dict_keys[min_index]]
    return closest_parking_lot[0],addresses[min_index],closest_parking_lot[1],dict_keys[min_index]