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
from flask import Flask, request, render_template
# import logging

# root = logging.getLogger() 
# root.setLevel(logging.INFO) 
 
# handler = logging.StreamHandler(sys.stdout) 
# handler.setLevel(logging.DEBUG) 
# formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(funcName)s - %(message)s') 
# handler.setFormatter(formatter) 
# root.addHandler(handler)

app = Flask(__name__)

@app.route('/')
def index():
    title = "Index page"
    content = "Это бетта версия моего приложения умного дома"
    return render_template(
        'index.html',
        utc_dt = content,
        title = title,
        menu = main_settings.menu,
        style = main_settings.css
    )
    # return 'Это бетта версия моего приложения умного дома'

@app.route('/gettemp')
def getTemp():
    try:
        temp = requests.get(f'{main_settings.boiler_address}/temp')
        result = BeautifulSoup(temp.text, "html.parser").string
        json_pars = json.loads(result)
        #print(json_pars)
        return json_pars, 200
    except Exception as ex:
        return ex, 501

@app.route('/get-status')
def getBoilerStatus ():
    boiler_number = int(request.args.get('number'))
    res = requests.get(f'{main_settings.boiler_address}/status-{boiler_number}')
    status = json.loads(BeautifulSoup(res.text, "html.parser").string)
    return status, 200

# For on boiler send args: ?status={1|0},number={boiler number}

@app.route('/set-status')
def setBoilerStatus():
    try:
        args = int(request.args.get('status'))
        boiler_number = int(request.args.get('number'))
        print(args)
        res = requests.get(f'{main_settings.boiler_address}/set-{boiler_number}-status/{args}')
        if res:
            pars = json.loads(BeautifulSoup(res.text, "html.parser").string)
            print(pars)
            return pars, 200
        else:
            return 'Запрос провалился', 501
        # return 'ok'
    except Exception as ex:
        return ex, 415

# Get current temp at bath
@app.route('/get_bath_temp')
def get_bath_temp():
    # r = requests.get(f'{main_settings.bath_address}/get_bath_temp')
    # temp = BeautifulSoup(r.text, 'html.parser').string
    return "", 404

# Get current state switch in the bath
@app.route('/set_switch_bath')
def set_switch_bath():
    return "", 404


# Get status of all device
@app.route('/get_all_stat')
def get_all_stat():
    return "", 404