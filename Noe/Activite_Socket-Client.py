import socket

port = int(input("Entrez le port d'entrée : "))
hote = str(input("Entrez sur quel serveur : "))
message = ''
if (hote == 'Noé') :
    hote = '172.16.134.19'
if (hote == 'Eva') :
    hote = '172.16.137.1'
if (hote == 'Camille') :
    hote = '172.16.136.1'    

serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serveur.connect((hote, port))


# Réception du serveur
data = serveur.recv(150)
print("> " + data.decode('utf-8'))
data = serveur.recv(5000)
print("> " + data.decode('utf-8'))

#Envoi du message au serveur
while (message != 'FIN') :
    data = serveur.recv(150)
    message = input("📤  ")
    serveur.send(message.encode('UTF-8'))
    print("> " + data.decode('utf-8'))
