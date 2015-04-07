#!/bin/bash

PROXY_IP=$1

# demarer le serveur web apache pour les pages web
# le répertoire web se trouve sous /var/www/
#
# Dans les configuration apache(/etc/apache2/apache2.conf:
#
#<Directory /var/www/>
#    Options Indexes FollowSymLinks
#    ...
#    FallbackResource /index.html  <-Cette ligne doit être ajoutée
#</Directory>


/etc/init.d/apache2 start

#configurer la table IP
iptables -t nat --flush
iptables --zero
iptables -A FORWARD --in-interface eth0 -j ACCEPT
iptables -t nat --append POSTROUTING --out-interface eth0 -j MASQUERADE

# Forward les paquets sur le port 80 vers notre serveur
echo "SENDING ALL WEBPAGE TO : $PROXY_IP"
iptables -t nat -A PREROUTING -p tcp --dport 80 --jump DNAT --to-destination $PROXY_IP

# Forward les paquets sur le port 443 vers notre serveur
iptables -t nat -A PREROUTING -p tcp --dport 443 --jump DNAT --to-destination $PROXY_IP

