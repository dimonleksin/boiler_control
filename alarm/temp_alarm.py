import telebot
from telebot import types
import requests
# from bs4 import BeautifulSoup
import json
import alarm_settings
import datetime

bot = telebot.TeleBot(alarm_settings.myTokenAlarm)
while True:
    # Alarm, when temp boiler 
    try:
        resultGetTemp = requests.get(f"{alarm_settings.main_url}/gettemp")
        tempBoiler = resultGetTemp["tempBoiler"]
        if tempBoiler > alarm_settings.boiler_temp_alar: #or resultGetTemp["tempHouse"] < alarm_settings.home_temp_alarm:            
            bot.send_message(alarm_settings.myId, f'Температура вышла за установленные лимиты, температура в доме: {str(resultGetTemp["tempHouse"])}, температура теплоносителя: {str(tempBoiler)}')

            # print() Print alarm message in log
        # Alarm, when temp in the bath > limits
        # bath_temp = main.get_bath_temp()
        # if bath_temp > alarm_settings.bath_temp_alarm:
        #     bot.send_message(alarm_settings.myId, f'Температура в сауне превысила {bath_temp}')
        t = f"{datetime.datetime.now()} {tempBoiler}"
        with open("temp_graf", "wa") as f:
            f.write(str(t))
    except Exception as ex:
        print(ex)
    time.sleep(30)