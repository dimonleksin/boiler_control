# ============================================
# Boiler control settings
# add address to esp8266 in boiler room

boiler_address = 'http://192.168.0.116'

# ============================================
# Light switch and temp bath
# add address to esp8266 in bath room

bath_address = 'http://'

menu = '<p><a href="/gettemp">Текущая температура в доме</a></p>' \
    '<p><a href="/status">Статус котла</a></p>'
css = '<link rel="stylesheet" href="./styles/style.css">'
bootstrap_servers = "kafka:9092"
