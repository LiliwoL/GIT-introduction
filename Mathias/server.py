#import du module socket
import socket

#iniatialisation des variables host port
host = "0.0.0.0"
port = 63000
renvoi="\nPrésent"

#socket crée
socket_ecoute = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#associé au port 63000
socket_ecoute.bind((host, port))
print ("♥ Socket en écoute au port 63000.. ♥")
socket_ecoute.listen(5)
conn, addr = socket_ecoute.accept()
print("Un client est connecté depuis l'adresse IP %s et le port %s" % (addr[0], addr[1]))
conn.send(("Vous etes connecte au serveur "+host+": "+str(port)).encode('utf-8'))
#écoute infinie tant que le client n'est pas connecté
while 1:
    data = conn.recv(150)
    if not data:
        break
    conn.sendall(data)
#on ferme la connexion
conn.close()


