##################################################################################################################

#New-NetFireWallRule -DisplayName 'WSL 2' -Direction Outbound -LocalPort "3390" -Action Allow -Protocol TCP

#New-NetFireWallRule -DisplayName 'WSL 2' -Direction Inbound -LocalPort "3390" -Action Allow -Protocol TCP

#netsh interface portproxy add v4tov4 listenport=80 listenaddress=0.0.0.0 connectport=80 connectaddress=172.21.103.28

##################################################################################################################


########################################################################
# connections
########################################################################
import socket

##### connexion du premier joueur #####
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

port = 63000

serverSocket.bind(("0.0.0.0",port))

serverSocket.listen(5)

print("Serveur en marche")

(clientConnecte, clientAddresse) = serverSocket.accept()

clients = [[clientConnecte, clientAddresse]]

print("connection reçu de %s:%s"%(clientAddresse[0], clientAddresse[1]))

##### demande nombre de joueur au joueur 1 #####

clientConnecte.send("Combien de joueur ?".encode())

dataFromClient = clientConnecte.recv(150)

print("le nombre de joueur est : " + dataFromClient.decode())

clients[0][0].send("Bien reçu.".encode())

##### ouvre autant de port qu'il y a de joueur #####
nombreJoueur = int(dataFromClient)
for i in range (0,nombreJoueur-1):
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    port += 1
    print("port : " + str(port))

    serverSocket.bind(("0.0.0.0",port))

    serverSocket.listen(5)

    print("nouveau serveur en marche")

    (clientConnecte, clientAddresse) = serverSocket.accept()

    clients.append([clientConnecte, clientAddresse])

    print("connection reçu de %s:%s"%(clientAddresse[0], clientAddresse[1]))

print("tous les joueurs sont connectés")
    


##################################################################################################################
# interactions client serveur
##################################################################################################################

def question_client(client, question):
    '''envoie une question au client et attend une réponse'''
    client[0].send(question.encode())
    reponse = client[0].recv(150)
    return reponse.decode()







########################################################################
# Uno
########################################################################

#### importation des modules ####
import random

#### définition des constantes ####
COULEURS = ["rouge", "jaune", "vert", "bleu"]
VALEURS = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
VALEURS_SPECIALES = ["passe", "inversion", "+2"]
VALEURS_SPECIALES_JOKER = ["joker", "+4"]
NB_CARTES_PAR_COULEUR = 2
NB_CARTES_SPECIALES_PAR_COULEUR = 2
NB_CARTES_SPECIALES_JOKER = 4

#### définition des variables globales ####
pioche = []
joueurs = []


#### définition des classes ####
class joueur:
    def __init__(self, nom, connections = ['127.0.0.1', 63000]):
        self.nom = nom
        self.connections = connections
        self.main = []

    def __str__(self):
        return self.nom + " " + self.main

    def envoyer_main(self):
        ''' envoie la main du joueur au client '''
        for carte in self.main:
            self.connections[0].send(carte.encode())

    def piocher(self):
        ''' pioche une carte dans la pioche '''
        self.main.append(pioche.piocher())
        self.envoyer_main()

    def jouer(self, carte):
        ''' joue une carte '''
        if carte in self.main:
            if fosse.ajouter(carte):
                self.main.remove(carte)
            
            else:
                print("erreur : la carte n'est pas jouable")
        else:
            print("erreur : la carte n'est pas dans la main du joueur")

            
    def demander_jouer(self):
        ''' demande au joueur de jouer une carte '''
        carte = question_client(self.connections, "quelle carte voulez vous jouer ?")
        self.jouer(carte)




class carte:
    def __init__(self, couleur, valeur):
        self.couleur = couleur
        self.valeur = valeur

    def __str__(self):
        return self.couleur + " " + self.valeur

class fosse:
    def __init__(self):
        self.cartes = []

    def __str__(self):
        return self.cartes

    def ajouter(self, carte):
        ''' ajoute une carte à la fosse en verifiant que la carte est jouable '''
        if self.cartes == []:
            self.cartes.append(carte)
            return True
        else:
            if carte.couleur == self.cartes[-1].couleur or carte.valeur == self.cartes[-1].valeur:
                self.cartes.append(carte)
            else:
                print("carte non jouable")
                return False

class pioche:
    def __init__(self):
        self.cartes = []
        for couleur in COULEURS:
            for valeur in VALEURS:
                self.cartes.append(carte(couleur, valeur))
            for valeur in VALEURS_SPECIALES:
                self.cartes.append(carte(couleur, valeur))
        for i in range(NB_CARTES_SPECIALES_JOKER):
            self.cartes.append(carte("noir", "joker"))
            self.cartes.append(carte("noir", "+4"))


    def __str__(self):
        return self.cartes

    def ajouter(self, carte):
        ''' ajoute une carte à la pioche '''
        self.cartes.append(carte)

    def melanger(self):
        ''' mélange la pioche '''
        random.shuffle(self.cartes)

    def piocher(self):
        ''' pioche une carte dans la pioche '''
        return self.cartes.pop()





#### définition des fonctions du Uno ####

def creer_joueurs():
    ''' crée les joueurs en demandant leur nom '''
    for client in clients:
        nom = question_client(client, "quel est votre nom ?")
        joueurs.append(joueur(nom, client))
        print("le joueur " + nom + " a rejoint la partie")

def distribuer_cartes():
    ''' distribue 7 cartes à chaque joueur '''
    for i in range(7):
        for joueur in joueurs:
            joueur.piocher(pioche)



def jouer():
    ''' joue le Uno '''
    creer_joueurs()
    distribuer_cartes()
    for joueur in joueurs:
        joueur.demander_jouer()
        if joueur.main == []:
            print("le joueur " + joueur.nom + " a gagné !")
            joueurs.remove(joueur)
    jouer()
    

jouer()



def fermertout():
    ''' ferme toutes les connexions '''
    for client in clients:
        client[0].close()
    serverSocket.close()

fermertout()