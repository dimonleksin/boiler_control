#! /bin/sh
uci set network.vpn0=interface
uci set network.vpn0.ifname=tun0
uci set network.vpn0.proto=none
uci set network.vpn0.auto=1
uci set firewall.Allow_OpenVPN_Inbound=rule
uci set firewall.Allow_OpenVPN_Inbound.target=ACCEPT
uci set firewall.Allow_OpenVPN_Inbound.src=*
uci set firewall.Allow_OpenVPN_Inbound.proto=udp
uci set firewall.Allow_OpenVPN_Inbound.dest_port=22094
uci set firewall.vpn=zone
uci set firewall.vpn.name=vpn
uci set firewall.vpn.network=vpn0
uci set firewall.vpn.input=ACCEPT
uci set firewall.vpn.forward=REJECT
uci set firewall.vpn.output=ACCEPT
uci set firewall.vpn.masq=1
uci set firewall.vpn_forwarding_lan_out=forwarding
uci set firewall.vpn_forwarding_lan_out.src=lan
uci set firewall.vpn_forwarding_lan_out.dest=vpn
uci commit network
/etc/init.d/network reload
uci commit firewall
/etc/init.d/firewall reload
#
##################################
#
# Config openvpn

echo > /etc/config/openvpn # очистите UCI конфигурацию для OpenVPN
uci set openvpn.myvpn=openvpn
uci set openvpn.myvpn.enabled=1
uci set openvpn.myvpn.verb=3
uci set openvpn.myvpn.port=22094
uci set openvpn.myvpn.proto=udp
uci set openvpn.myvpn.dev=tun
uci set openvpn.myvpn.server='10.8.0.0 255.255.255.0'
uci set openvpn.myvpn.keepalive='10 120'
uci set openvpn.myvpn.ca=/etc/openvpn/ca.crt
uci set openvpn.myvpn.cert=/etc/openvpn/home-server.crt
uci set openvpn.myvpn.key=/etc/openvpn/home-server.key
uci set openvpn.myvpn.dh=/etc/openvpn/dh.pem
uci commit openvpn
/etc/init.d/openvpn enable
/etc/init.d/openvpn start
