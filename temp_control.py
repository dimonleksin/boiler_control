import telebot
from telebot import types
import requests
from bs4 import BeautifulSoup
import json
import setings
import main

bot = telebot.TeleBot(setings.myTokenAlarm)
while True:
    try:
        resultGetTemp = main.getTemp()
        if resultGetTemp["tempBoiler"] > 30.00:
            bot.send_message(setings.myId, f'Температура превысила установленный лимит{main.getTemp()}')

    except Exception as ex:
        print(ex)