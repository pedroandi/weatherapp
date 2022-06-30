'''
libs usadas:
Nominatim - api de mapa para geolocalização
'''

from geopy.geocoders import Nominatim

def getcoord(x): #função pra obter as coordenadas passando o endereço
    coordenadas = Nominatim(user_agent="Weather") #chama a api do google e retorna abaixo
    return coordenadas.geocode(f"{x}").raw