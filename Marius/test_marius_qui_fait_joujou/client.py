########################################################################
# connections
########################################################################
import socket
 
port = 63000
host = str(input('Adresse de connexion ? : '))



def connection(port, host):
    global clientSocket
    try:   
        print("connection au port : " + str(port))
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


        clientSocket.connect((host,port))
        print("connection réussi")


    except:
        if (port == 36010):
            print("tous les ports sont occupés")
            return
        print("erreur de connection")
        print("reconnection au port : " + str(port +1))
        connection(port +1 , host)



    

    


connection(port, host)

while True:
    dataFromServer = clientSocket.recv(150)

    if ("?" in dataFromServer.decode()):
        print(">"+ dataFromServer.decode())
        data = str(input())
        clientSocket.send(data.encode())


clientSocket.close()
