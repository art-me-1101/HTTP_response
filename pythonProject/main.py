import sys
from io import BytesIO
from geopy.distance import geodesic as gd

import requests
from PIL import Image


toponym_to_find = " ".join(sys.argv[1:])

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
    "type": "biz",
    'results': '1'
}

response = requests.get(search_api_server, params=search_params)
if not response:
    ...

json_response = response.json()
toponym = json_response["features"][0]
print(f"адрес: {toponym['properties']['CompanyMetaData']['address']}\n"
      f"Название: {toponym['properties']['CompanyMetaData']['name']}\n"
      f"Время работы: {toponym['properties']['CompanyMetaData']['Hours']['text']}\n"
      f"Расстояние от заданной точки: {gd(tuple(address_ll.split(',')), (toponym_coodrinates,)).meters} метров")
toponym_coodrinates = list(map(str, toponym['geometry']['coordinates']))

toponym_coord = ','.join(toponym_coodrinates)
map_params = {
    "l": "map",
    'pt': address_ll + ',pm2al~' + toponym_coord + ',pm2bl'
}

map_api_server = "http://static-maps.yandex.ru/1.x/"
response = requests.get(map_api_server, params=map_params)

Image.open(BytesIO(
    response.content)).show()
