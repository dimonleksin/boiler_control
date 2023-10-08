# https://aiu.susu.ru/iot/summer/quick_start MQTT на esp
# https://www.emqx.com/en/blog/how-to-use-mqtt-in-python mqtt python


# Нужно проверять наличае заголовка с Nginx, Если он есть, то выполнять не все команды для безопасности
# Часть команд будут выполняться только из локальной сети

##### lib to multitreading #####
# from threading import Thread
# import time

import requests
from bs4 import BeautifulSoup
import json
import main_settings
from flask import Flask, request

app = Flask(__name__)

# bot = telebot.TeleBot(main_settings.myToken)

@app.route('/')
def index():
    return 'Тестовый запуск удался'

@app.route('/gettemp')
def getTemp():
    try:
        temp = requests.get(f'{main_settings.boiler_address}/temp')
        result = BeautifulSoup(temp.text, "html.parser").string
        json_pars = json.loads(result)
        #print(json_pars)
        return json_pars
    except Exception as ex:
        return ex

@app.route('/get-status')
def getBoilerStatus ():
    res = requests.get(f'{main_settings.boiler_address}/status-1')
    status = json.loads(BeautifulSoup(res.text, "html.parser").string)
    return status

# For on boiler send args: ?status={1|0},number={boiler number}

@app.route('/set-status')
def setBoilerStatus():
    try:
        args = int(request.args.get('status'))
        boiler_number = int(request.args.get('number'))
        print(args)
        if args == 0 and boiler_number == 1:
            res = requests.get(f'{main_settings.boiler_address}/set-1-status/0')
            if res:
                pars = json.loads(BeautifulSoup(res.text, "html.parser").string)
                print(pars)
                return pars
            else:
                return 'Запрос провалился'

        elif args == 1 and boiler_number == 1:
            res = requests.get(f'{main_settings.boiler_address}/set-1-status/1')
            if res:
                pars = json.loads(BeautifulSoup(res.text, "html.parser").string)
                print(pars)
                return pars
            else:
                return 'Запрос провалился'


        if args == 0 and boiler_number == 2:
            res = requests.get(f'{main_settings.boiler_address}/set-2-status/0')
            if res:
                pars = json.loads(BeautifulSoup(res.text, "html.parser").string)
                print(pars)
                return pars
            else:
                return 'Запрос провалился'

        elif args == 1 and boiler_number == 2:
            res = requests.get(f'{main_settings.boiler_address}/set-2-status/1')
            if res:
                pars = json.loads(BeautifulSoup(res.text, "html.parser").string)
                print(pars)
                return pars
            else:
                return 'Запрос провалился'

        return args
        # return 'ok'
    except Exception as ex:
        return ex

# Get current temp at bath
@app.route('/get_bath_temp')
def get_bath_temp():
    r = requests.get(f'{main_settings.bath_address}/get_bath_temp')
    temp = BeautifulSoup(r.text, 'html.parser').string
    return

# Get current state switch in the bath
@app.route('/set_switch_bath')
def set_switch_bath():
    pass


# Get status of all device
@app.route('/get_all_stat')
def get_all_stat():
    pass