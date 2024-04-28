import sys
from io import BytesIO

import requests
from PIL import Image

toponym_to_find = 'Россия Иваново ул. 30 м-н 33'
print(toponym_to_find)
geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

geocoder_params = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "geocode": toponym_to_find,
    "format": "json"}

response = requests.get(geocoder_api_server, params=geocoder_params)

if not response:
    pass

json_response = response.json()
toponym = json_response["response"]["GeoObjectCollection"][
    "featureMember"][0]["GeoObject"]
toponym_coodrinates = ','.join(toponym["Point"]["pos"].split())

search_api_server = "https://search-maps.yandex.ru/v1/"
api_key = "65fde4fd-24f6-49cd-aa40-34c4dc166d7f"

address_ll = toponym_coodrinates
search_params = {
    "apikey": api_key,
    "text": "аптека",
    "lang": "ru_RU",
    "ll": address_ll,
    "type": "biz"
}

response = requests.get(search_api_server, params=search_params)
if not response:
    ...

json_response = response.json()
apteki = []
for i in range(10):
    toponym = json_response["features"][i]
    toponym_coodrinates = list(map(str, toponym['geometry']['coordinates']))
    toponym_coord = ','.join(toponym_coodrinates)
    if 'Hours' in toponym['properties']['CompanyMetaData']:
        try:
            if toponym['properties']['CompanyMetaData']['Hours']['Availabilities'][0]['TwentyFourHours']:
                apteki.append((toponym_coord, 2))
            else:
                apteki.append((toponym_coord, 1))
        except Exception:
            apteki.append((toponym_coord, 1))
    else:
        apteki.append((toponym_coord, 0))

map_params = {
    "l": "map",
    'pt': '~'.join([i[0] + [',pmgrm', ',pmblm', ',pmgnm'][i[1]] for i in apteki])
}
map_api_server = "http://static-maps.yandex.ru/1.x/"
response = requests.get(map_api_server, params=map_params)

Image.open(BytesIO(
    response.content)).show()
