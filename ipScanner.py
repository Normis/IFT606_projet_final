#source https://code.google.com/p/jaccon-ipscanner/source/browse/ipscanner.py
#j'ai essayer d'utiliser python nmap mais a part spinner il ne fait rien,
# aussi l'utilitaire arp -a ne semble pas fonctioner 

import os
import time
import sys
from subprocess import Popen

class IpScanner:
    ipRange = '192.168.0'
    listAlive = []
    listNoReply = []
    listError = []

    def __init__(self, ipRange):
        self.ipRange = ipRange
    def __init__ (self):
        self.ipRange = '192.168.0' #Pour ne rien faire sinon sa prend un constructeur par default

    def scan(self):
        self.listAlive = []
        devnull = open(os.devnull, 'wb')
        processToDo = []
        #on scan les IP du range donner de 1 a 255
        for n in range(1,255): # start ping processes 
            ip = self.ipRange + ".%d" % n
            #remplie une list de subprocess a executer avec la commande ping
            processToDo.append((ip, Popen(['ping', '-c', '3', ip], stdout=devnull,stderr=devnull)))
        while processToDo:
            for i, (ip, proc) in enumerate(processToDo):
                if proc.poll() is not None: # ping finished
                    #si le ping a repondu avec un code sans erreur on sais que l'IP est up 
                    #si il y a erreure on assume que l'IP n'est pas bon
                    processToDo.remove((ip, proc)) # this makes it O(n**2)
                    if proc.returncode == 0:
                        self.listAlive.append(ip)
                    elif proc.returncode == 2:
                        self.listNoReply.append(ip)
                    else:
                        self.listError.append(ip)
            time.sleep(.04) 
        devnull.close()

        return self.listAlive

    def getAliveIps():
        return self.listAlive
