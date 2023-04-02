import requests, json
from bs4 import BeautifulSoup

address = 'http://192.168.1.70'

def getTemp():
    temp = requests.get(f'{address}/boilertemp')
    soup = BeautifulSoup(temp.text, "html.parser").string
    json_pars = json.loads(soup)
    print(soup, json_pars['tempBoiler'])
#    return json_pars

getTemp()