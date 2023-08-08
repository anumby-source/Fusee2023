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

