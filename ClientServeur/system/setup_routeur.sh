#!/bin/bash

CLIENTSERVEUR=/home/pi/Fusee2023/ClientServeur
CLIENTSERVEURSYSTEM=$CLIENTSERVEUR/system
CLIENTSERVEURSYSTEMORIGIN=$CLIENTSERVEUR/system_origin

# installe la configuration
sudo apt update
sudo apt install dnsmasq hostapd

sudo cat $CLIENTSERVEURSYSTEM/hostapd.conf >> /etc/hostapd/hostapd.conf
sudo cat $CLIENTSERVEURSYSTEM/dnsmasq.conf >> /etc/dnsmasq.conf
sudo sed -ri 's/# net.ipv4.ip_forward=1/net.ipv4.ip_forward=1/' /etc/sysctl.conf

sudo systemctl restart dnsmasq
sudo systemctl restart hostapd

sudo chmod +x $CLIENTSERVEUR/routeurfusee.py

sudo cat $CLIENTSERVEURSYSTEM/routeurfusee.service  >> /etc/systemd/system/routeurfusee.service

sudo systemctl enable routeurfusee
sudo systemctl start routeurfusee

# sudo systemctl status routeurfusee
# sudo journalctl -u routeurfusee
