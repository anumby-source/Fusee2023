#!/bin/bash

CLIENTSERVEUR=/home/pi/Fusee2023/ClientServeur
CLIENTSERVEURSYSTEM=$CLIENTSERVEUR/system
CLIENTSERVEURSYSTEMORIGIN=$CLIENTSERVEUR/system_origin

FILE=CLIENTSERVEURSYSTEMORIGIN/hostapd.conf
if [ -f "$FILE" ]; then
    sudo cp $CLIENTSERVEURSYSTEMORIGIN/hostapd.conf /etc/hostapd
    sudo cp $CLIENTSERVEURSYSTEMORIGIN/dnsmasq.conf /etc/
    sudo cp $CLIENTSERVEURSYSTEMORIGIN/sysctl.conf /etc/
fi

sudo systemctl stop routeurfusee
sudo systemctl disable routeurfusee
sudo systemctl stop routeurfusee

