import telebot
from telebot import types
import requests
# from bs4 import BeautifulSoup
import json
import alarm_settings
import datetime
import os
import time 
import logging

bot = telebot.TeleBot(os.getenv(alarm_settings.myToken))
while True:
    # Alarm, when temp boiler 
    try:
        resultGetTemp = requests.get(f"{alarm_settings.main_url}/gettemp")
        tempBoiler = resultGetTemp["tempBoiler"]
        print(f"Geted temp {tempBoiler}")
        if tempBoiler > alarm_settings.boiler_temp_alar: #or resultGetTemp["tempHouse"] < alarm_settings.home_temp_alarm:            
            bot.send_message(alarm_settings.myId, f'Температура вышла за установленные лимиты, температура в доме: {str(resultGetTemp["tempHouse"])}, температура теплоносителя: {str(tempBoiler)}')
            print("Sended alarm into telegramm")
            # print() Print alarm message in log
        # Alarm, when temp in the bath > limits
        # bath_temp = main.get_bath_temp()
        # if bath_temp > alarm_settings.bath_temp_alarm:
        #     bot.send_message(alarm_settings.myId, f'Температура в сауне превысила {bath_temp}')
        t = f"{datetime.datetime.now()} {tempBoiler}"
        with open("/mnt/temp_graf", "a") as f:
            f.write(str(t))
            print(f"Writed message {t} into file temp_graf")
    except Exception as ex:
        print(ex)
    time.sleep(30)