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

root = logging.getLogger() 
root.setLevel(logging.INFO) 
 
handler = logging.StreamHandler(sys.stdout) 
handler.setLevel(logging.DEBUG) 
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(funcName)s - %(message)s') 
handler.setFormatter(formatter) 
root.addHandler(handler)

def write_to_postgre(data: str) -> None:
    connect_string = f"postgresql://{settings.pg_user}:{settings.pg_passwd}@{settings.pg_url}:{settings.pg_port}/{settings.pg_db_name}"
    logging.info(connect_string)

    try:
        connection = psycopg2.connect(connect_string)
        logging.info(f"Successful connected to data base {settings.pg_db_name}")
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute(
                f"INSERT INTO {settings.pg_table_name}(temperature, timestp) VALUES({data}, now())"
            )
    except Exception as ex:
        logging.error(f"Error: {ex}")
    return



bot = telebot.TeleBot(os.getenv(settings.myToken))
while True:
    # Alarm, when temp boiler 
    try:
        resultGetTemp = requests.get(f"{settings.main_url}/gettemp")
        pars = json.loads(BeautifulSoup(resultGetTemp.text, "html.parser").string)
        tempBoiler = pars["tempBoiler"]
        logging.info(f"Geted temp {tempBoiler}")
        if float(tempBoiler) > settings.boiler_temp_alar: #or resultGetTemp["tempHouse"] < settings.home_temp_alarm:            
            bot.send_message(settings.myId, f'Температура вышла за установленные лимиты, температура теплоносителя: {tempBoiler}')
            logging.info("Sended alarm into telegramm")

        write_to_postgre(tempBoiler)



            # print() Print alarm message in log
        # Alarm, when temp in the bath > limits
        # bath_temp = main.get_bath_temp()
        # if bath_temp > settings.bath_temp_alarm:
        #     bot.send_message(settings.myId, f'Температура в сауне превысила {bath_temp}')
        # t = f"{datetime.datetime.now()}/{tempBoiler} \n"
        # with open(f"/mnt/temp_graf{datetime.date.today()}", "a") as f:
        #     f.write(str(t))
        #     print(f"Writed message {t} into file temp_graf")
    except Exception as ex:
        logging.error(ex)
    time.sleep(30)