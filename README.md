# IFT606_projet_final
Projet final du cours dans le cadre du cours IFT606

## Attaque ARP-POISONING
* Script: mitm.py
* Language: python
* Description: Envoi des requêtes ARP vers les victimes pour modifier son registre ARP
* Résultat: Tous les paquets des victimes passe maintenant par l'ordinateur de l'attaquant.

```
usage: mitm.py [-h] [-i] [-m MYIP] [-n NETIFACE] [-r ROUTERIP] [-x] [-y]

optional arguments:
  -h, --help            show this help message and exit
  -i, --interactive     manually choose targets
  -m MYIP, --myIp MYIP  Manually specify your IP if not able to automatically
                        get it
  -n NETIFACE, --netiface NETIFACE
                        Specify the interface to use by default wlan0
  -r ROUTERIP, --routerIP ROUTERIP
                        Specify the IP for the router if not able to
                        automatically find it
  -x, --ignoreHttp      Don't redirect paquet from port 80 to the local
                        webserver
  -y, --ignoreHttps     Don't redirect paquet from port 443 to the local
                        webserver
```



