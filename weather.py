#Testing OpenWeather API

import requests
# from pyowm import OWM
# from pyowm.utils import timestamps
from PIL import Image
import schedule
import time
import json
from io import BytesIO
import random
degree_sign = u'\N{DEGREE SIGN}'

def weather_update():
    api_key = "API KEY"
    lat = 12345
    lon = 12345
    url = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&appid=%s&units=metric" % (lat, lon, api_key)
    response = requests.get(url)
    data = json.loads(response.text)
    hourly = data["hourly"]
    global weather_data
    weather_data = []
    for i in range(10):
        temp = str(round(int(hourly[i]["temp"]))) + " " + degree_sign + "C"
        # weather = entry["weather"][0]['main']
        icon = hourly[i]["weather"][0]["icon"]
        image_url = "http://openweathermap.org/img/wn/" +  icon + "@2x.png"
        image_response = requests.get(image_url)
        img = Image.open(BytesIO(image_response.content))
        weather_data.append([temp,image_url])


weather_update()
schedule.every().hour.do(weather_update)
while True:
    schedule.run_pending()
    time.sleep(0.5) #this might need to change