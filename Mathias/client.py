import socket

#initialisation des variables
hote = "127.0.0.1"
port = 63000
envoi="\nServeur es-tu là?"

#ouverture du socket
socket_ecoute = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#connection au socket
socket_ecoute.connect((hote, port))

#
data = socket_ecoute.recv(1024)
#fermeture du socket
socket_ecoute.close()

print(data.decode('utf-8'),"\nReçue")

