#import du module socket
import socket

#iniatialisation des variables host port
host = '0.0.0.0'
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
conn.send(("Vous etes connecte au serveur de eva ♥♥♥ "+host+": "+str(port)).encode('utf-8'))
#écoute infinie tant que le client n'est pas connecté
while 1:
    conn.send("\n Que voulez vous envoyer ? (pas d'insultes tolérées !☻) ?\n".encode('UTF-8'))
    data = conn.recv(1024)
    data = data.decode("utf-8")
    print (" Le client a envoyé : "+"\n → "+ data)
    conn.send(("ton message :  "+data +" a bien été envoyé ☻"+"\n").encode('UTF-8'))
    
    if data == "FIN":
        conn.send("Au revoir boloss ! Merci ! ♥.".encode('UTF-8'))
        print (" Fin de votre connexion. A plus tard le sang !")
        break
    
    
    
 #ch = input("Voulez-vous attendre un nouveau client sur votre super serveur du futur  ? <R>ecommencer <T>erminer ? ")
  #  if ch.upper() =='T':
   #     break    
#on ferme la connexion
