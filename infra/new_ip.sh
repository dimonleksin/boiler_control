#! /bin/sh
old_ip=$(cat /www/curent_ip)
current_ip=$(curl ifconfig.me/ip)
if [[ $old_ip != $current_ip ]]; then
curl "https://api.telegram.org/bot6906656172:AAEngHkpw32TIsKlGWQXFh-BpJAfxonrrH8/sendMessage?chat_id=1776929080&text=$current_ip"
echo "send new ip"
else
echo "ip not different"
fi
