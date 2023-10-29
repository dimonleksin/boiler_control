import telebot
import telebot
import requests
from bs4 import BeautifulSoup
import json
import alarm_settings as settings
import datetime
import os
import sys
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

def write_to_postgre(
    home: str,
    boiler: str='28.32'
) -> None:
    connect_string = f"postgresql://{settings.pg_user}:{settings.pg_passwd}@{settings.pg_url}:{settings.pg_port}/{settings.pg_db_name}"
    # logging.info(connect_string)

    try:
        connection = psycopg2.connect(connect_string)
        logging.info(f"Successful connected to data base {settings.pg_db_name}")
        connection.autocommit = True
        request = f"INSERT INTO {settings.pg_table_name}(temperature,sensor_n,timestp) VALUES({home}, 'home', now()); INSERT INTO {settings.pg_table_name}(temperature,sensor_n,timestp) VALUES({boiler}, 'boiler', now());"
        with connection.cursor() as cursor:
            cursor.execute(
                request
            )
            logging.info("Successfuly insert into table")
    except Exception as ex:
        logging.error(f"Error, when send request to SQL: {ex}")
    return


try:
    token = os.getenv(str(settings.myToken))
    bot = telebot.TeleBot(token)
    logging.info(f"Successfuly received token bot")
except Exception as ex:
    logging.error("Token not found")

while True:
    # Alarm, when temp boiler 
    try:
        resultGetTemp = requests.get(f"{settings.main_url}/gettemp")
        pars = json.loads(BeautifulSoup(resultGetTemp.text, "html.parser").text)

        logging.info("Succesfuly received from main server")

        tempBoiler = pars["tempBoiler"]
        tempHouse = pars["tempHouse"]
        logging.info(f"Geted temp boiler: {tempBoiler}, house: {tempHouse}")

        if float(tempBoiler) > settings.boiler_temp_alar:# or float(tempHouse) < settings.home_temp_alarm:            
            bot.send_message(settings.myId, f'Температура вышла за установленные лимиты, температура теплоносителя: {tempBoiler}')
            logging.info("Sended alarm into telegramm")
        
        write_to_postgre(tempBoiler, tempHouse)

    except Exception as ex:
        logging.error(f"Error, when send request to main server. Err: {ex}")
        bot.send_message(settings.myId, "Не смог связаться с сервером ")
        continue
    
    
    
    
        # print() Print alarm message in log
    # Alarm, when temp in the bath > limits
    # bath_temp = main.get_bath_temp()
    # if bath_temp > settings.bath_temp_alarm:
    #     bot.send_message(settings.myId, f'Температура в сауне превысила {bath_temp}')
    # t = f"{datetime.datetime.now()}/{tempBoiler} \n"
    # with open(f"/mnt/temp_graf{datetime.date.today()}", "a") as f:
    #     f.write(str(t))
    #     print(f"Writed message {t} into file temp_graf")
    time.sleep(30)