import socket

#initialisation des variables
hote = "172.16.136.1"
port = 63000
envoi="\nServeur es-tu là?"

#ouverture du socket
socket_ecoute = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#connection au socket
socket_ecoute.connect((hote, port))

#
data = socket_ecoute.recv(150)
print (" on recoit ceci ")
print("> " + data.decode('utf-8'))


##while (message != 'FIN'):
#while 1:

    # Lecture du message à envoyer
 #   ch = input()

    # Si le client veut mettre FIN
  #  if ch.upper() == 'FIN':
   #     socket_ecoute.send("FIN".encode('UTF-8'))
    #    break
    #else:
        # Envoi du message
     #   socket_ecoute.send(ch.encode('UTF-8'))

        # Reception de l'ECHO du serveur
data = socket_ecoute.recv(150)
print(data.decode('utf-8'),"\nReçue")

#fermeture du socket
data = socket_ecoute.recv(150)
print("> " + data.decode('utf-8'))
socket_ecoute.close()



