import telebot
from telebot import types
# import requests
# from bs4 import BeautifulSoup
import json
import setings
import time

bot = telebot.TeleBot(setings.myTokenAlarm)
while True:
    # Alarm, when temp boiler 
    try:
        resultGetTemp = main.getTemp()
        if resultGetTemp["tempBoiler"] > setings.boiler_temp_alar or resultGetTemp["tempHouse"] < setings.home_temp_alarm:            
            bot.send_message(setings.myId, f'Температура вышла за установленные лимиты, температура в доме: {str(resultGetTemp["tempHouse"])}, температура теплоносителя: {str(resultGetTemp["tempBoiler"])}')

            # print() Print alarm message in log
        # Alarm, when temp in the bath > limits
        bath_temp = main.get_bath_temp()
        if bath_temp > setings.bath_temp_alarm:
            bot.send_message(setings.myId, f'Температура в сауне превысила {bath_temp}')
    except Exception as ex:
        print(ex)
    time.sleep(30)
            