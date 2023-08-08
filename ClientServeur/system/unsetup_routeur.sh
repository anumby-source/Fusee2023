#!/bin/bash

CLIENTSERVEUR=/home/pi/Fusee2023/ClientServeur
CLIENTSERVEURSYSTEM=$CLIENTSERVEUR/system
CLIENTSERVEURSYSTEMORIGIN=$CLIENTSERVEUR/system_origin

sudo restore_system_config.sh

sudo systemctl stop routeurfusee
sudo systemctl disable routeurfusee
sudo systemctl stop routeurfusee

