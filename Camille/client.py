import socket
 
#demande l'adresse ip et le port de connexion
port = int(input('Port de connexion ? : '))
host = str(input('Adresse de connexion ? : '))


#se connecte au serveur
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

clientSocket.connect((host,port))

#attend une réponse du serveur
dataFromServer = clientSocket.recv(1000000)
#affiche la réponse du serveur
print(">"+ dataFromServer.decode())

#échange des messages avec le serveur
while 1:
    #demande a l'utilisateur de saisir un message
    data = str(input("message : "))
    #envoie d'un message au serveur
    clientSocket.send(data.encode())
    #attend la réponse du serveur
    dataFromServer = clientSocket.recv(1000000)
    #affiche la réponse du serveur
    print(">" + dataFromServer.decode())

    #arrete la discusion si le client reçoit le message 'FIN'
    if (dataFromServer.decode() == "FIN"):
        print("arret de la connection")
        break