#!/bin/bash

PROXY_IP='192.168.0.195'

# demarer le serveur web apache pour les pages web
# le répertoire web se trouve sous /var/www/
/etc/init.d/apache2 start

#configurer la table IP
iptables -t nat --flush
iptables --zero
iptables -A FORWARD --in-interface eth0 -j ACCEPT
iptables -t nat --append POSTROUTING --out-interface eth0 -j MASQUERADE

# Forward les paquets sur le port 80 vers notre serveur
echo "SENDING ALL WEBPAGE TO : $PROXY_IP"
iptables -t nat -A PREROUTING -p tcp --dport 80 --jump DNAT --to-destination $PROXY_IP
