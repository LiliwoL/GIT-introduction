# import du module socket
import socket

# définition des variables
port_d_ecoute = 63001
nom_d_hote = '127.0.0.1'

# création du socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# liaison du socket à l'adresse et au port
s.bind((nom_d_hote, port_d_ecoute))

print("Le serveur est en route")

while 1 :
    # écoute des connexions entrantes
    s.listen()

    # acceptation de la connexion
    (connexion_client, adresse) = s.accept()

    # affichage de l'adresse IP du client
    print("Un client est connecté depuis l'adresse IP %s et le port %s" % (adresse[0], adresse[1]))


    text = str("Bonjour, je suis le serveur de marius, vous etes connecte depuis l'adresse IP "+ str(adresse[0]) + " et le port " + str(adresse[1]))
    # envoi d'un message au client
    connexion_client.send(text.encode('UTF-8'))


# fermeture de la connexion
connexion_client.close()

# fermeture du socket
s.close()