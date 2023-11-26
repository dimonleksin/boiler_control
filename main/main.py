# https://aiu.susu.ru/iot/summer/quick_start MQTT на esp
# https://www.emqx.com/en/blog/how-to-use-mqtt-in-python mqtt python


# Нужно проверять наличае заголовка с Nginx, Если он есть, то выполнять не все команды для безопасности
# Часть команд будут выполняться только из локальной сети

##### lib to multitreading #####
# from threading import Thread
# import time

import requests
import json
import main_settings
from flask import Flask, request, render_template
# import kafka
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
    ), 200
    # return 'Это бетта версия моего приложения умного дома'

@app.route('/gettemp')
def getTemp():
    try:
        result_temp
        temp = requests.get(f'{main_settings.boiler_address}/temp')
        result = BeautifulSoup(temp.text, "html.parser").string
        json_pars = json.loads(result)

        for k, v in json_pars.items():
            result_temp += f"<p>Temperature in {k} = {v}</p>"

        return json_pars, 200
    except Exception as ex:
        return ex, 501

# @app.route('/status')
# def getBoilerStatus ():
#     boiler1 = ""
#     boiler2 = ""

#     boiler_number = int(request.args.get('number'))
#     res1 = requests.get(f'{main_settings.boiler_address}/status-1')
#     status_boiler_1 = json.loads(BeautifulSoup(res1.text, "html.parser").string)

#     res1 = requests.get(f'{main_settings.boiler_address}/status-2')
#     status_boiler_2 = json.loads(BeautifulSoup(res1.text, "html.parser").string)

#     kafka.KafkaConsumer()

#     if status_boiler_1["boiler_1_status"] == "Boiler is on":
#         boiler1 = "checked"
#     else:
#         boiler1 = ""

#     if status_boiler_2["boiler_2_status"] == "Boiler is on":
#         boiler2 = "checked"
#     else:
#         boiler2 = ""

#     # Geting form 
#     if request.method == "POST":
#         boiler1 = bool(request.form.get("boiler_1", False))
#         boiler2 = bool(request.form.get("boiler_2", False))

#         content = "Boilers status changed."

#     content = ''
#     return render_template(
#         'index.html',
#         boiler1 = boiler1,
#         boiler2 = boiler2,
#         utc_dt = content,
#         title = title,
#         menu = main_settings.menu,
#         style = main_settings.css,
#         form = "True"
#     ), 200

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

@app.route('test')
def test():
    return {
        "tempBoiler": 22,
	    "tempHouse": 21,
	    "tempOutside": 43
    }

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