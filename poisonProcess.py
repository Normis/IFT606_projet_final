import arpPoison
import sys

routerIP = sys.args[2]
victimeIP = sys.args[2]

ArpPoison(routerIP, victimeIP)
