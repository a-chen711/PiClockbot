# PiClockbot :clock8:

I originally set out to build my own recreation of the [Lovebox](https://en.lovebox.love/) as an anniversary gift to my girlfriend but as I continued into the design process, I found that I wanted my gift to be a bit different than a simple recreation...thus PiClockbot was born. 

<p align="middle">
  <img src="https://user-images.githubusercontent.com/59714253/166198233-af17eb06-545a-4326-9e7d-e68399701d80.JPEG" alt="Front" width="270">
  <img src="https://user-images.githubusercontent.com/59714253/166198389-00df85c3-ef52-410c-9791-7af7f7907db4.JPEG" alt="Side" width="270">
  <img src="https://user-images.githubusercontent.com/59714253/166198820-acaaf151-20c1-4068-9781-bf9319afc02d.JPEG" alt="Side2" width="270">
</p>

## Hardware Components 💻

- Raspberry Pi Zero W (Already setup with Raspbian OS and headers)
- 2.4 inch LCD Display Module (Found [here](https://www.waveshare.com/2.4inch-lcd-module.htm))
- 3D Printed Housing (Based on the TinyMac [here](https://www.instructables.com/Making-a-Tiny-Mac-From-a-Raspberry-Pi-Zero/))

## Software :page_with_curl:

### Files 

- _PiClock_Tele.py_ is the final implementation of the project
- _PiClock.py_ only has the clock face and weather forecast, no Telegram functionality
- _Weather Icons_ has all the weather images used, courtesy of Apple Weather Icons found [here](https://support.apple.com/guide/iphone/view-the-weather-icons-iph4305794fb/ios)
- _fonts_ has all the fonts used
- _listener.py_ is the test for the Telethon API
- _weather.py_ is the test for the Open Weather API
- _caseback_edit.blend_ contains my edits to the caseback STL found on the TinyMac Repo
- _front_edit.blend_ contains my edits to the front_plus STL found on the TinyMac Repo
- _launcher.sh_ is the shell script to run the code at startup (I followed [this tutorial](https://www.instructables.com/Raspberry-Pi-Launch-Python-script-on-startup/))
- _requirements.txt_ contains all the packages used

### Design

I used a combination of the [Open Weather API](https://openweathermap.org/) and [Telethon API](https://docs.telethon.dev/en/stable/) to create the functionality of this project. Both the weather forecast and Telegram scraper run asynchronously. 
You may notice that occasionally a stutter will occur, likely due to some network latency in updating the weather data. Files were transferred to the Raspberry Pi via SSH. 

#### Weather Forecast

The display outputs the date and time, then uses a scheduler to update the weather forecast for the following 4 hours every 10 minutes and at the hour change using Open Weather. 
I used the returned weather data codes and corresponding weather widget icons to display the temperature and weather icon for the forecasts. .
Weather data codes and their corresponding icons can be found in the Open Weather documentation. If no internet connection is detected, then the forecast will be replaced with a "NO WIFI CONNECTION" text. 

#### Telegram Integration

A Telegram client is created that listens async to any messages sent into a chosen chat or channel and upon receiving a certain message, will trigger a new message to be displayed, overriding the clock face.

## Demo :rocket:

https://user-images.githubusercontent.com/59714253/166200621-98a90127-fb53-409c-ade5-eab1906b04a8.mp4

