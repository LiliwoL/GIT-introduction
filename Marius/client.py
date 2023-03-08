# import du module socket
import socket

# définition des variables
port_d_ecoute = 63000
nom_d_hote = '127.0.0.1'

# création du socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connexion au serveur
s.connect ((nom_d_hote, port_d_ecoute))

# envoi d'un message au serveur
s.send("Bonjour, je suis le client".encode('UTF-8'))

# réception de la réponse du serveur
data = s.recv(150)

# affichage de la réponse
print(data.decode('UTF-8'))