# IFT606_projet_final
Projet final du cours dans le cadre du cours IFT606

## Attaque ARP-POISONING
* Script: arp.py
* Language: python
* Description: Envoi des requêtes ARP vers la victime pour modifier son registre ARP 
* Résultat: Tous les paquets de la victime passe maintenant par l'ordinateur de l'attaquant et la victime n'est plus en mesure d'accèder au réseau
* Usage: python arp.py -v 192.168.0.5 -r 192.168.0.1

## Affichage d'une fausse page web
* Script: start.sh
* Language: batch
* Description: Démarre un serveur apache et modifie la table de routing
* Résultat: La victime tombe sur notre faux site web


