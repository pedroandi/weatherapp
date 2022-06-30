'''
libs usadas:
json - tratamento do json retornado
requests - tratamento de chamadas de APIs
'''

import json
import requests

#token de chamada da API
token = 'e4720729770650b1e075619623c3ffb7'

#função usa as coordenadas de lat e lon obtidas pelo nominatim, retorna entao todos os dados referentes à clima etc para as coordenadas
def weather(x,y):
    weather = requests.get(f'https://api.openweathermap.org/data/3.0/onecall?lat={x}&lon={y}&exclude=minutely,hourly&appid={token}&units=metric&lang=pt_br')
    weatheraw = json.loads(weather.content)
    return weatheraw