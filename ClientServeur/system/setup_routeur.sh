#!/bin/bash

CLIENTSERVEUR=/home/pi/Fusee2023/ClientServeur
CLIENTSERVEURSYSTEM=$CLIENTSERVEUR/system
CLIENTSERVEURSYSTEMORIGIN=$CLIENTSERVEUR/system_origin

# sauvegarde les fichiers system d'origine
FILE=CLIENTSERVEURSYSTEMORIGIN/hostapd.conf
if [ ! -f "$FILE" ]; then
    echo "$FILE does not exist, save system files."
    cp /etc/hostapd/hostapd.conf CLIENTSERVEURSYSTEMORIGIN
    cp /etc/dnsmasq.conf CLIENTSERVEURSYSTEMORIGIN
    cp /etc/sysctl.conf CLIENTSERVEURSYSTEMORIGIN
fi

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
