#Clock and Telegram integration where the trigger text will activate the secondary screen overlaying the clock

#!/usr/bin/python
# -*- coding: UTF-8 -*-
#import chardet
from email.mime import image
import os
import sys 
import time
import datetime
import pytz
import requests, json
import schedule
from io import BytesIO
import logging
import spidev as SPI
sys.path.append("..")
from lib import LCD_2inch4
from PIL import Image,ImageDraw,ImageFont
import http.client as httplib
# import httplib
import asyncio
from telethon import TelegramClient, events
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.messages import (GetHistoryRequest)
from telethon.tl.types import (
    PeerChannel
)

# Raspberry Pi pin configuration:
RST = 27
DC = 25
BL = 18
bus = 0 
device = 0 
degree_sign = u'\N{DEGREE SIGN}'

#=====================================
#openweather API
api_key = "API KEY"
lat = 12345
lon = 12345
url = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&appid=%s&units=metric" % (lat, lon, api_key)
local_tz = pytz.timezone('INSERT LOCATION')
def time_update(hour_now):
    midnight = False
    hour_list = []
    for i in range(4):
        if midnight:
            next_hour = str(int(next_hour) + 1)
        elif int(hour_now) + i + 1 >= 24:
            next_hour = "00"
            midnight = True
        else:
            next_hour = str(int(hour_now) + i + 1)
        
        if len(next_hour) == 1: #if it's AM's add a 0 to the front 
            next_hour = "0" + next_hour
        hour_list.append(next_hour)
    return hour_list

def weather_update():
    global weather_update_hour 
    global weather_data
    global have_internet

    if wifi_connected():
        have_internet = True
    else:
        have_internet = False
        # weather_update_hour = curr_hour
        return have_internet
    now = datetime.datetime.now()
    weather_update_hour = now.astimezone(local_tz).strftime("%H")
    response = requests.get(url)
    data = json.loads(response.text)
    hourly = data["hourly"]
    weather_data = []
    for i in range(10):
        temp = str(round(int(hourly[i]["temp"]))) + " " + degree_sign + "C"
        icon = hourly[i]["weather"][0]["icon"]
        # print(hourly[i]["weather"][0]["description"])
        # image_url = "http://openweathermap.org/img/wn/" +  icon + "@2x.png"
        weather_data.append([temp,icon])


def wifi_connected():
    conn = httplib.HTTPSConnection("8.8.8.8", timeout=5)
    try:
        conn.request("HEAD", "/")
        return True
    except Exception:
        return False
    finally:
        conn.close()

#=====================================
#telegram API
api_id = "INSERT API ID"
api_hash = "INSERT API HASH"

# use full phone number including + and country code
phone = "PHONE #"
username = "USERNAME"

# Create the client and connect
client = TelegramClient(username, api_id, api_hash)
alex_ind = -1
nicole_ind = -1
# Display type
disp = LCD_2inch4.LCD_2inch4()
# Initialize library.
disp.Init()
# Clear display.
disp.clear()
width = disp.width
height = disp.height
tele_bg = Image.new("RGB", (height, width), "BLACK")
tele_draw = ImageDraw.Draw(tele_bg)
text_font = ImageFont.truetype('../Font/Metropolis-Medium.otf', 25)
meme_font = ImageFont.truetype('../Font/Metropolis-Medium.otf', 10)
emoji = Image.open("./heart_emoji_2.jpg")
@client.on(events.NewMessage(chats = "PiClock")) #maybe change to nicole Liau
async def my_event_handler(event):
    if 'trigger text' == event.raw_text:
        # tele_draw.rectangle((0,120,height,width-120), outline=0, fill=0) #have to go height, width     
        tele_draw.text((0 + 9, 80), "Display text", font=text_font, fill="WHITE")
        tele_bg.paste(emoji, (0 + 130, 125))
        tele_draw.text((0 + 105, 225), "Display text", font=meme_font, fill="WHITE")
        disp.ShowImage(tele_bg)
        time.sleep(3)
#=====================================

async def main():
    weather_list = ["01d", "01n", "02d", "02n", "03d", "03n","04d", "04n", "09d", "09n", "10d", "10n", "11d", "11n", "13d", "13n","50d", "50n"]

    # logging.basicConfig(level=logging.DEBUG)
    try:
        # display with hardware SPI:
        ''' Warning!!!Don't  creation of multiple displayer objects!!! '''
        #disp = LCD_2inch4.LCD_2inch4(spi=SPI.SpiDev(bus, device),spi_freq=10000000,rst=RST,dc=DC,bl=BL)

        # Create blank image for drawing.
        image1 = Image.new("RGB", (disp.height, disp.width), "BLACK")
        draw = ImageDraw.Draw(image1)

        # logging.info("draw rectangle")

        draw.rectangle((0,0,height,width), outline=0, fill=0)

        # First define some constants to allow easy resizing of shapes.
        padding = 2
        top = padding
        # Move left to right keeping track of the current x position for drawing shapes.
        x = padding
        # Draw an ellipse.

        # Load default font.
        date_font = ImageFont.truetype('../Font/Metropolis-Medium.otf', 25)
        temp_font = ImageFont.truetype('../Font/Lato-Bold.ttf', 18)
        time_font = ImageFont.truetype('../Font/Metropolis-Medium.otf', 70)
        curr_hour = 0
        count = 0

        #scheduling
        weather_update()
        schedule.every(10).minutes.do(weather_update) #every 10 mins

        #get all the images before we start the for loop
        weather_img = []
        for i in range(18):
            weather_img.append(Image.open("./Weather Icons/" + weather_list[i] + "_v2.png"))
        # weather_img = Image.open("./test_img/changed.png")
        while True:
            schedule.run_pending()
            time_now = datetime.datetime.now()
            mst_now = time_now.astimezone(local_tz)
            draw.rectangle((0,0,height,width), outline=0, fill=0) #have to go height, width     

            # logging.info("show date and time")
            draw.text((x+2, top+2),    mst_now.strftime("%a %b %d"), font=date_font, fill="WHITE")
            draw.text((x, top+30), mst_now.strftime("%H:%M:%S"), font=time_font, fill="WHITE")

            ####WEATHER####
            # logging.info("show hourly")
            curr_hour = mst_now.strftime("%H")
            time_list = time_update(curr_hour) #weather and time are actually desynced, so you should update the weather every time the hour changes
            if weather_update_hour != curr_hour: #if the hour has changed but we haven't updated weather, manually update
                weather_update()
            if have_internet:
                draw.text((0 + 9, 125), "Now", font=temp_font, fill="WHITE")
                draw.text((65 + 5, 125), time_list[0] + ":00", font=temp_font, fill="WHITE")
                draw.text((130 + 5, 125), time_list[1] + ":00", font=temp_font, fill="WHITE")
                draw.text((195 + 5, 125), time_list[2] + ":00", font=temp_font, fill="WHITE")
                draw.text((260 + 5, 125), time_list[3] + ":00", font=temp_font, fill="WHITE")

                # logging.info("show image")
                #grab weather data for the next 5 hours and paste images of weather
                index_0 = weather_img[weather_list.index(weather_data[0][1])]
                index_1 = weather_img[weather_list.index(weather_data[1][1])]
                index_2 = weather_img[weather_list.index(weather_data[2][1])]
                index_3 = weather_img[weather_list.index(weather_data[3][1])]
                index_4 = weather_img[weather_list.index(weather_data[4][1])]
                image1.paste(index_0, (0, 150))
                image1.paste(index_1, (65, 150))
                image1.paste(index_2, (130, 150))
                image1.paste(index_3, (195, 150))
                image1.paste(index_4, (260, 150))

                # logging.info("show temperatures")
                #Paste temperatures 
                draw.text((0 + 8, 150 + 55), weather_data[0][0], font=temp_font, fill="WHITE")
                draw.text((65 + 8, 150 + 55), weather_data[1][0], font=temp_font, fill="WHITE")
                draw.text((130 + 8, 150 + 55), weather_data[2][0], font=temp_font, fill="WHITE")
                draw.text((195 + 8, 150 + 55), weather_data[3][0], font=temp_font, fill="WHITE")
                draw.text((260 + 8, 150 + 55), weather_data[4][0], font=temp_font, fill="WHITE")
            else:
                draw.text((x+20, top+175), "NO WIFI CONNECTION", font=date_font, fill="RED")
            disp.ShowImage(image1)
            count +=1
            await asyncio.sleep(0.1)            # disp.display()
        disp.module_exit()
    except IOError as e:
        logging.info(e)    
    except KeyboardInterrupt:
        disp.module_exit()
        logging.info("quit:")
        exit()
client.start()
client.loop.run_until_complete(main())