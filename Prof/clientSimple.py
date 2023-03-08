# Un client à utiliser avec le serveurSimple.py

import socket, sys


#############################
# 1. Définition des variables
#############################

# Adresse ip et port de la socket sur laquelle va ecouter le serveur
# A ADAPTER A VOTRE MACHINE, vous pouvez mettre 0.0.0.0 pour écouter sur toutes les adresses IP du serveur
# Quelle est la conséquence d'écouter sur 127.0.0.1 ?
# HOST = '127.0.0.1'

# Saisir ici l'adresse IP de la machine windows de l'élève (pas celle de sa WSL)
HOST = {
        "local": "127.0.0.1",
        "Marius": "172.16.140.5",
        "Noé": "172.16.134.19",
        "Maxime": "172.16.133.1",
        "Eva": "172.16.137.1",
        "Camille": "172.16.136.1",
        "NC": "172.16.3.2",
    }
# Port TCP sur lequel on va se connecter
PORT = 63000


#############################
# 2. Création du socket
#############################

# On indique les protocoles (ici IP et TCP)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


#############################
# 3. Connexion du socket vers une paire hôte de destination, port
#############################
try:
    print ("Sur quel serveur voulez vous vous connecter?")
    for h in HOST:
        print (h)

    host_choosed = input()
    RHOST = HOST[host_choosed]

    print ("Connexion à " + RHOST)

    s.connect((RHOST, PORT))
except socket.error:
     # En cas d'échec de la liaison
    # La plupart du temps car la connexion est refusée
    print("La connexion a échoué.")
    #print (socket.error)
    # Arrêt du programme
    sys.exit()

print("\n<FIN> pour terminer la connexion\n\n")

#############################
# 4. Lecture du message de confirmation de connexion envoyé par le serveur
#############################
# On lit 15 octets sur la socket (augmenter pour lire plus...)
data = s.recv(150)


#############################
# 5. Affichage du message de bienvenue
#############################
# Convertir le tableau de 15 octets en une chaine de caractères
# et l'afficher.
print("> " + data.decode('utf-8'))



#############################
# 6. Echanges avec le serveur
#############################
while 1:

    # Lecture du message à envoyer
    ch = input()

    # Si le client veut mettre FIN
    if ch.upper() == 'FIN':
        s.send("FIN".encode('UTF-8'))
        break
    else:
        # Envoi du message
        s.send(ch.encode('UTF-8'))

        # Reception de l'ECHO du serveur
        data = s.recv(150)
        print("> " + data.decode('utf-8'))

# Fin de la connexion
data = s.recv(150)
print("> " + data.decode('utf-8'))

s.close()