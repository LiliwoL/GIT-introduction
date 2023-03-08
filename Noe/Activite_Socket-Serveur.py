import socket

# Initialisation des variables
port = 63000
hote = '0.0.0.0'
message = ''

# Création du socket
socket_ecoute = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_ecoute.bind((hote, port))
print(" Le serveur est en route 🟢")

# Mise en écoute du serveur
socket_ecoute.listen()

(client, adresse) = socket_ecoute.accept()
# Connection d'un client au serveur
print("Un client est connecté depuis l'adresse IP %s et le port %s" % (adresse[0], adresse[1]))

client.send(("Vous êtes connecté au serveur de Noé au port : "+str(port)+".\n") + .encode('UTF-8'))

while 1:
    client.send("\n Quel message souhaitez vous envoyer ?\n".encode('UTF-8'))
    data = client.recv(1024)
    data = data.decode("utf-8")
    print ("\n 📥 "+ data)
    client.send(("Ton message :  '"+ data +"' a bien été envoyé au serveur."+"\n").encode('UTF-8'))

    if data == "FIN":
        client.send("Au revoir mon gars, prend ce ratio au passage.".encode('UTF-8'))
        print ("Le serveur n'a pas eu le succès escompté, on reviendra plus fort la team 💪🔥")
        break