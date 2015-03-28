#source https://code.google.com/p/jaccon-ipscanner/source/browse/ipscanner.py
#j'ai essayer d'utiliser python nmap mais a part spinner il ne fait rien,
# aussi l'utilitaire arp -a ne semble pas fonctioner 

import os
import time
import sys
import socket
import subprocess
from subprocess import Popen

class IpScanner:
    ipRange = '192.168.0'
    listAlive = []

    def __init__(self, ipRange='192.168.0'):
        self.ipRange = ipRange
    #def __init__ (self):
    #    self.ipRange = '192.168.0' #Pour ne rien faire sinon sa prend un constructeur par default

    def scan(self):
        self.listAlive = []
        devnull = open(os.devnull, 'wb')
        processToDo = []
        #on scan les IP du range donner de 1 a 255
        for n in range(1,255): # start ping processes 
            ip = self.ipRange + ".%d" % n
            #remplie une list de subprocess a executer avec la commande ping
            #le -c 3 permet de pas faire ping a l'infenie 
            processToDo.append((ip, Popen(['ping', '-c', '3', ip], stdout=devnull,stderr=devnull)))
        while processToDo:
            for i, (ip, proc) in enumerate(processToDo[:]):
                if proc.poll() is not None: # ping finished
                    #si le ping a repondu avec un code sans erreur on sais que l'IP est up 
                    #si il y a erreure on assume que l'IP n'est pas bon
                    processToDo.remove((ip, proc)) # this makes it O(n**2)
                    if proc.returncode == 0:
                        self.listAlive.append(ip)
            time.sleep(.04) 
        devnull.close()
        try:
            self.listAlive.remove(socket.gethostbyname(socket.gethostname())) # so on ne se tir pas dans le pied
        except:
            None 
        return self.listAlive

    
    def getOsForIp(self, ip):
        answer = 'failed'
        try:
            devnull = open(os.devnull, 'wb')
            process = Popen(['sudo','nmap','-v','-O','-sS',ip], stdout=subprocess.PIPE, stderr = devnull)
            out,err = process.communicate()


            #look in the text to get the OS 
            lines = out.splitlines()
            answer = 'Unknown'
            for l in lines: 
                if 'Running' in l:
                    answer = l.split(' ', 1)

            process.kill()
        except: 
            None
        return answer

    def getHostName(self,ip):
        answer = 'Failed'
        try:
            return socket.gethostbyaddr(ip)[0]
        except: 
            return answer

