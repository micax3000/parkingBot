import bs4 as bs
import urllib.request
from typing import List


def findSlots() -> List[str]:
    source = urllib.request.urlopen(
        'https://www.parking-servis.co.rs/garaze-i-parkiralista#6-slobodna-parking-mesta').read()
    soup = bs.BeautifulSoup(source, 'lxml')
    slots = soup.find('ul','parking-count').find_all('li')
    return [f'{slot.a.text}:{slot.span.text}' for slot in slots]
