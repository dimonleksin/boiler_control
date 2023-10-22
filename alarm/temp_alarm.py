import telebot
from telebot import types
import requests
from bs4 import BeautifulSoup
import json
import alarm_settings as settings
import datetime
import os
import time 
import logging
import psycopg2


def write_to_postgre(data):
    connection = psycopg2.connect(f"posgresql://{settings.pg_user}:{settings.pg_passwd}@{settings.pg_url}:{settings.pg_port}/{settings.pg_db_name}")
    with connection.cursor as cursor:
        cursor.execute(
            "INSERT INTO "
        )



bot = telebot.TeleBot(os.getenv(alarm_settings.myToken))
while True:
    # Alarm, when temp boiler 
    try:
        resultGetTemp = requests.get(f"{alarm_settings.main_url}/gettemp")
        pars = json.loads(BeautifulSoup(resultGetTemp.text, "html.parser").string)
        tempBoiler = pars["tempBoiler"]
        print(f"Geted temp {tempBoiler}")
        if float(tempBoiler) > alarm_settings.boiler_temp_alar: #or resultGetTemp["tempHouse"] < alarm_settings.home_temp_alarm:            
            bot.send_message(alarm_settings.myId, f'Температура вышла за установленные лимиты, температура теплоносителя: {tempBoiler}')
            print("Sended alarm into telegramm")
            # print() Print alarm message in log
        # Alarm, when temp in the bath > limits
        # bath_temp = main.get_bath_temp()
        # if bath_temp > alarm_settings.bath_temp_alarm:
        #     bot.send_message(alarm_settings.myId, f'Температура в сауне превысила {bath_temp}')
        # t = f"{datetime.datetime.now()}/{tempBoiler} \n"
        # with open(f"/mnt/temp_graf{datetime.date.today()}", "a") as f:
        #     f.write(str(t))
        #     print(f"Writed message {t} into file temp_graf")
    except Exception as ex:
        print(ex)
    time.sleep(30)