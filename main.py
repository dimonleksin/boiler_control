#Тут нужен будет телеграм бот, который будет получать от SiriDB информацию по текущей температуре и отдавать в чат
# https://aiu.susu.ru/iot/summer/quick_start MQTT на esp
# https://www.emqx.com/en/blog/how-to-use-mqtt-in-python mqtt python

# import telebot
# from telebot import types
import requests
from bs4 import BeautifulSoup
import json
import setings
from flask import Flask, request

app = Flask(__name__)


# bot = telebot.TeleBot(setings.myToken)

@app.route('/')
def index():
    return 'Тестовый запуск удался'
    
@app.route('/gettemp')
def getTemp():
    try:
        temp = requests.get(f'{setings.address}/temp')
        result = BeautifulSoup(temp.text, "html.parser").string
        json_pars = json.loads(result)
        #print(json_pars)
        return json_pars
    except Exception as ex:
        return ex

@app.route('/get-status')
def getBoilerStatus ():
    res = requests.get(f'{setings.address}/status')
    return json.loads(BeautifulSoup(res.text, "html.parser").string)["boilerStatus"]
    
@app.route('/set-status')
def setBoilerStatus():
    try:
        args = request.args.get('status')
        print(args)
        return 'ok'
    except Exception as ex:
        return ex
    # if state == 0:
    #     res = requests.get(f'{setings.address}/setstatus/0')
    #     if res:
    #         pars = json.loads(BeautifulSoup(res.text, "html.parser").string)["boilerStatus"]
    #         print(pars)
    #         return pars

    # elif state == 1:
    #     res = requests.get(f'{setings.address}/setstatus/1')
    #     if res:
    #         pars = json.loads(BeautifulSoup(res.text, "html.parser").string)["boilerStatus"]
    #         print(pars)
    #         return pars
# @bot.message_handler(commands = ['start'])
# def start (message):
#     if message.chat.id == setings.myId or message.chat.id == setings.sheId:
#         bot.send_message(message.from_user.id, "Првиет. Я твой помошник по управлению и мониторингу котла в доме. Напиши мне что нибудь")
#     else:
#         bot.send_message(message.from_user.id, "Простите, этот бот не для вас")
#         print(f'{message.chat.id} пытался написать в наш чат: {message.text}')

# @bot.message_handler(content_types= ['text'])
# def OnOfBoiler (message):
#     if message.chat.id == setings.myId or message.chat.id == setings.sheId:
#         markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#         btn1 = types.KeyboardButton('temp')
#         btn2 = types.KeyboardButton('on')
#         btn3 = types.KeyboardButton('off')
#         btn4 = types.KeyboardButton('boiler_now')
#         markup.add(btn1, btn2, btn3, btn4)
#         bot.send_message(message.from_user.id, 'Выбери', reply_markup=markup) #ответ бота

#         #print(message.text)
#         if message.text == 'temp':
#             returned_json = getTemp()
#             bot.send_message(message.from_user.id, f'Температура теплоносителя: {returned_json["tempBoiler"]}. Температура в доме: {returned_json["tempHouse"]}. Температура за окном: {returned_json["tempOutside"]}.')
#         elif message.text == 'on':
#             bot.send_message(message.from_user.id, setBoilerStatus(1))
#         elif message.text == 'off':
#             bot.send_message(message.from_user.id, setBoilerStatus(0))
#         elif message.text == 'boiler_now':
#             bot.send_message(message.from_user.id, f'В настоящий момент {getBoilerStatus()}')
#         else:
#             bot.send_message(message.from_user.id, 'Прости, не понимаю что ты хочешь')
#             print(f'{message.chat.id} написал в чат: {message.text}')


# bot.polling(none_stop=True, interval=0) #recikle send request new message

