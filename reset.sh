#!/bin/bash
#Remettre en ordre la table IP
echo "Resetting iptables"
iptables -t nat --flush
iptables --zero

/etc/init.d/apache2 stop