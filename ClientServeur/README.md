# configuration du Raspberry pour autoriser les clients extérieurs

Si vous n'avez pas de routeur, une option possible est de configurer votre Raspberry Pi  
en tant que point d'accès Wi-Fi, ce qui lui permettrait d'agir comme son propre routeur.

Ensuite, vous pourriez connecter vos appareils Android à ce point d'accès pour qu'ils soient sur le même réseau.

Voici les étapes générales pour configurer votre Raspberry Pi comme un point d'accès Wi-Fi :

# Installer les paquets nécessaires

Vous devez d'abord installer dnsmasq et hostapd.  
Ces logiciels permettent respectivement à votre Raspberry Pi de gérer les adresses IP  
pour les connexions réseau et d'agir comme un point d'accès sans fil.

Vous pouvez les installer avec les commandes suivantes :

sudo apt update
sudo apt install dnsmasq hostapd

# Configurer hostapd

Vous devez configurer hostapd avec les détails de votre point d'accès,  
comme le nom du réseau et le mot de passe.

Pour cela, éditez le fichier /etc/hostapd/hostapd.conf et ajoutez des lignes comme les suivantes :

interface=wlan0
ssid=AnumbyFusee
hw_mode=g
channel=7
wmm_enabled=0
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_passphrase=123456789
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP

# Configurer dnsmasq

dnsmasq doit être configuré pour gérer les adresses IP pour les connexions au point d'accès.  
Pour cela, éditez le fichier /etc/dnsmasq.conf et ajoutez des lignes comme les suivantes :

interface=wlan0
dhcp-range=192.168.4.2,192.168.4.20,255.255.255.0,24h

# Activer le routage IP :

Pour que le Raspberry Pi puisse transmettre du trafic entre le réseau sans fil et son propre réseau,  
vous devez activer le routage IP. Vous pouvez le faire en modifiant le fichier /etc/sysctl.conf et en décommentant la ligne suivante :

net.ipv4.ip_forward=1

# Redémarrer les services :

Enfin, redémarrez dnsmasq et hostapd pour qu'ils prennent en compte les nouvelles configurations :

sudo systemctl restart dnsmasq
sudo systemctl restart hostapd

# Configurer le service routeur

Pour exécuter votre script Python au démarrage sur un Raspberry Pi,  
vous pouvez utiliser le daemon systemd qui est intégré dans la plupart des distributions Linux modernes.

Voici comment vous pouvez le faire :

Écrivez un fichier de service pour votre application. Vous pouvez le créer  
dans le répertoire /etc/systemd/system. Par exemple, si votre application s'appelle myapp,  
vous pouvez créer un fichier appelé myapp.service:

sudo nano /etc/systemd/system/routeurfusee.service

[Unit]
Description=Routeur_Fusee

[Service]
ExecStart=/usr/bin/python3 /home/pi/Fusee2023/ClientServeur/clientserveur_aio.py
Restart=always
User=pi
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=routeurfusee

[Install]
WantedBy=multi-user.target

# lancer le service

Enregistrez et fermez le fichier. Maintenant, vous pouvez dire à systemd de  
démarrer ce service au démarrage et de lancer le service immédiatement :

sudo systemctl enable myapp
sudo systemctl start myapp

# Suivi du service:

Vous pouvez vérifier le statut de votre service à tout moment en utilisant la commande :

sudo systemctl status myapp

Et vous pouvez voir les logs de votre application avec :

sudo journalctl -u myapp

Notez que cette configuration suppose que vous utilisez Python 3 et que  
l'interpréteur Python est situé à /usr/bin/python3. Si ce n'est pas le cas,  
vous pouvez trouver le bon chemin avec la commande which python3.

De plus, assurez-vous que votre script peut être exécuté en tant que script autonome,  
c'est-à-dire qu'il a un shebang approprié à la première ligne (par exemple, #!/usr/bin/python3)  
et que les autorisations de fichier sont correctement définies  
(par exemple, en utilisant chmod +x /chemin/vers/votre/script.py).

# configurer l'accès SSH

SSH (Secure Shell) est un protocole qui vous permet de vous connecter et de  
contrôler votre Raspberry Pi à distance via un réseau. Pour l'activer et le  
configurer sur votre Raspberry Pi, suivez les étapes suivantes:

##  Activer SSH sur Raspberry Pi

- Si vous avez un écran, un clavier et une souris connectés à votre Raspberry Pi,  
  vous pouvez activer SSH via l'interface graphique de Raspberry Pi OS.  
  Allez dans le menu Préférences

  - Configuration du Raspberry Pi
  - Interfaces et activez SSH.

- Si vous n'avez pas accès à l'interface graphique, vous pouvez activer SSH en
  créant un fichier nommé ssh dans la partition de boot de la carte SD de votre Raspberry Pi.
  Vous pouvez le faire sur un autre ordinateur. Lorsque le Raspberry Pi démarre et détecte ce fichier,
  il active automatiquement le serveur SSH.

##  Se connecter à Raspberry Pi via SSH
Une fois SSH activé, vous pouvez vous y connecter depuis un autre ordinateur.  
Vous aurez besoin de l'adresse IP de votre Raspberry Pi sur votre réseau local.  
Vous pouvez généralement le trouver via l'interface d'administration de votre routeur,  
ou en utilisant des outils de réseau comme nmap.

Sur Linux ou macOS, ouvrez un terminal et tapez ssh pi@<IP_address>,  
en remplaçant <IP_address> par l'adresse IP de votre Raspberry Pi. Par exemple: ssh pi@192.168.1.5.

Sur Windows, vous devrez peut-être télécharger un client SSH comme PuTTY. Ouvrez PuTTY,  
entrez l'adresse IP de votre Raspberry Pi dans le champ "Host Name" et cliquez sur "Open".

## Authentification

Le nom d'utilisateur par défaut est pi et le mot de passe par défaut est raspberry.  
Pour des raisons de sécurité, il est recommandé de changer le mot de passe par défaut après votre première connexion.

## Accès à distance sécurisé
Si vous prévoyez d'accéder à votre Raspberry Pi via Internet (et pas seulement depuis votre réseau local),  
il est recommandé d'ajouter des mesures de sécurité supplémentaires,  
comme la configuration des clés SSH et l'installation d'un pare-feu.

Rappelez-vous qu'une fois que vous avez activé SSH, votre Raspberry Pi est  
potentiellement vulnérable aux attaques non désirées. Il est donc très important de  
changer votre mot de passe par défaut et de prendre des mesures supplémentaires  
pour sécuriser votre appareil, surtout si vous prévoyez de l'exposer à Internet.