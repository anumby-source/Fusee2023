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
ssid=MonReseau
hw_mode=g
channel=7
wmm_enabled=0
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_passphrase=MonMotDePasse
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

