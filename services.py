import logging
import os
import urllib.request
import requests
import json
import threading
import bs4 as bs
from dotenv import load_dotenv

load_dotenv()
distance_api = os.getenv("DISTANCE_API")

parking_slots_state = {}


def refreshTable(f_stop):
    findSlots()
    if not f_stop.is_set():
        threading.Timer(30, refreshTable, [f_stop]).start()


def findSlots():
    logging.info('findSlots run')
    source = urllib.request.urlopen(
        'https://www.parking-servis.co.rs/garaze-i-parkiralista#6-slobodna-parking-mesta').read()
    slots = bs.BeautifulSoup(source, 'lxml').find('ul', 'parking-count').find_all('li')
    global parking_slots_state
    parking_slots_state = {slot.a['href'].split('/')[-1]: (slot.a.text, slot.span.text) for slot in slots}


async def calculateDistances(latitude, longitude):
    distance_values = []
    addresses = []
    data = {}
    dict_keys = [coordinates for coordinates, info in list(parking_slots_state.items()) if int(info[1]) > 0]
    for i in range(0, len(dict_keys), 25):
        destinations = '|'.join(map(lambda key: ','.join(key.split(',')), dict_keys[i:i + 25]))
        if destinations != '':
            destinations = destinations.replace(',', '%2C').replace('|', '%7C')
            url = f'https://maps.googleapis.com/maps/api/distancematrix/json?' \
                  f'origins={latitude}%2C{longitude}&destinations={destinations}&key={distance_api}'
            response = requests.request("GET", url)
            if response.status_code == 200:
                data = dict(json.loads(response.text))
                distance_values.extend([x['duration']['value'] for x in data['rows'][0]['elements']])
                addresses.extend(data['destination_addresses'])
            else:
                return None
    min_index = distance_values.index(min(distance_values))
    address, free_spaces = parking_slots_state[dict_keys[min_index]]
    return address, addresses[min_index], free_spaces, dict_keys[min_index]
