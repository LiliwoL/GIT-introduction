# Définition d'un serveur simple
# Le serveur attend la connexion d'un client et fait un echo des messages reçu

import socket, sys


#############################
# 1. Définition des variables
#############################

# Adresse ip et port de la socket sur laquelle va ecouter le serveur
# A ADAPTER A VOTRE MACHINE, vous pouvez mettre 0.0.0.0 pour écouter sur toutes les adresses IP du serveur
# Quelle est la conséquence d'écouter sur 127.0.0.1 ?
HOST = '0.0.0.0'
PORT = 63000



#############################
# 2. Création du socket
#############################

# On indique les protocoles (ici IP et TCP)
mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


#############################
# 3. Configuration du socket
#############################
try:
    # Liaison du socket créé à une paire (adresse IP, Numéro de port)
    mySocket.bind((HOST, PORT)) # Attention à bien laisser les deux parenthèses! Ca correspond à une paire
except socket.error:
    # En cas d'échec de la liaison
    # La plupart du temps car le port est déjà en cours d'utilisation
    print("La liaison du socket à l'adresse choisie a échoué.")
    # Arrêt du programme
    sys.exit()


#############################
# 4. Un serveur est souvent une boucle infinie qui attend des connexions.
#############################
while 1:
    # Le serveur se bloque en attente de la requête de connexion d'un client
    print(" **** Serveur simple en attente... ****")
    mySocket.listen(5) # Allez voir la documentation officielle de Python pour voir les paramètres de listen()



    #############################
    # 5. Le serveur se débloque lors de l'établissement de la connexion
    #############################
    connexion, adresse = mySocket.accept()  # La méthode accept() renvoie une paire contenant la connexion et les informations sur le client
    print("Un client est connecté depuis l'adresse IP %s et le port %s" % (adresse[0], adresse[1])) # Attention au formatage d'une string en python



    #############################
    # 6. Envoi d'un message de bienvenue au client
    #############################

    # Attention la chaine de caractère DOIT etre convertie en un tableau d'octets
    #    le paramète 'UTF-8" indique l'encodage des caractères qui doit être utilisé.
    connexion.send(("Vous êtes connecté au serveur "+HOST+":"+str(PORT)+".\n").encode('UTF-8'))



    #############################
    # 7. Le serveur commence maintenant un echange avec le client connecté
    #############################
    while 1:
        # envoi de la question au client
        connexion.send("Votre message ?\n".encode('UTF-8'))

        # attente de la reponse
        msgClient = connexion.recv(1024)

        # le message est converti d'une tableau d'octets en chaine de caractères
        msgClient = msgClient.decode("utf-8")

        # Si la reponse est FIN ou un ligne vide, le dialogue d'arrête.
        if msgClient.upper().strip() == "FIN" or msgClient.strip() == "":
           break

        # Traitement de la réponse
        # le serveur affiche sur sa console
        print("     Reçu du client >"+msgClient+"<")
        # et envoi un echo au client
        connexion.send(("ECHO : "+msgClient+"\n").encode('UTF-8'))


    #############################
    # 8. Si l'on est sorti de la boucle il faut terminer le programme et clore la connexion
    #############################

    connexion.send("Good Bye.".encode('UTF-8'))
    print("Connexion interrompue.")

    # Le serveur ferme la connexion
    connexion.close()

    ch = input("Attendre un autre client ? <R>ecommencer <T>erminer ? ")
    if ch.upper() =='T':
        break