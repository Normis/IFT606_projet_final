#!/bin/bash


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


PROXY_IP=$1
IFACE=$2
USE80=$3
USE443=$4

/etc/init.d/apache2 start

#configurer la table IP
iptables -t nat --flush
iptables --zero
iptables -A FORWARD --in-interface $IFACE -j ACCEPT
iptables -t nat --append POSTROUTING --out-interface $IFACE -j MASQUERADE

echo "SENDING ALL WEBPAGE TO : $PROXY_IP"
if [ "$USE80" != "0" ]
then
    # Forward les paquets sur le port 80 vers notre serveur
    echo "Forwarding 80"
    iptables -t nat -A PREROUTING -p tcp --dport 80 --jump DNAT --to-destination $PROXY_IP
fi

if [ "$USE443" != "0" ]
then
    # Forward les paquets sur le port 443 vers notre serveur
    echo "Forwarding 443"
    iptables -t nat -A PREROUTING -p tcp --dport 443 --jump DNAT --to-destination $PROXY_IP
fi

