import nmap #Dl link => https://pypi.python.org/pypi/python-nmap
from subprocess import Popen, PIPE

scanner = nmap.PortScanner()
scanner.scan('192.168.1.1/24','22') #search for the losers (users) on the network. 

losers = scanner.all_hosts()
losersMac = []
for l in losers:
    losersMac.append(Popen(["arp", "-n", l], stdout=PIPE))


print repr(losers)