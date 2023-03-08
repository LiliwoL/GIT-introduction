##################################################################################################################
#Commande pour les rêgles du firewall

# D'abord, on supprime les éventuelles restes de précédentes règles
#netsh interface portproxy delete v4tov4 listenport=$port listenaddress=$addr 
#netsh interface portproxy add v4tov4 listenport=$port listenaddress=$addr connectport=$port connectaddress=$remoteport


#New-NetFireWallRule -DisplayName 'WSL 2' -Direction Outbound -LocalPort "3390" -Action Allow -Protocol TCP
#New-NetFireWallRule -DisplayName 'WSL 2' -Direction Inbound -LocalPort "3390" -Action Allow -Protocol TCP
#netsh interface portproxy add v4tov4 listenport=80 listenaddress=0.0.0.0 connectport=80 connectaddress=172.21.103.28

##################################################################################################################

import socket

#démare le serveur
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#lie le serveur au port 63000
serverSocket.bind(("0.0.0.0",63000))
#fait écouter le serveur
serverSocket.listen(5)
#affiche un message
print("Serveur en marche")

#etablie une connection avec le client
(clientConnecte, clientAddresse) = serverSocket.accept()

print("connection reçu de %s:%s"%(clientAddresse[0], clientAddresse[1]))

#envoie un message au client
clientConnecte.send("""

 _   _         _  _       
| | | |  ___  | || |  ___  
| |_| | / _ \ | || | / _ \  
|  _  |/ /_\ \| || |/ / \ \ 
| | | |\ ,___/| || |\ \_/ / 
|_| |_| \___/ |_||_| \___/  
                              ,-'_ `-.                              
                              ::".^-. `.                            
                              ||<    >. \                           
                              |: _, _| \ \                          
                              : .'| '|  ;\`.                        
                              _\ .`  '  | \ \                       
                            .' `\ *-'   ;  . \                      
                           '\ `. `.    /\   . \                     
                         _/  `. \  \  :  `.  `.;                    
                       _/ \  \ `-._  /|  `  ._/                     
                      / `. `. `.   /  :    ) \                      
                      `;._.  \  _.'/   \ .' .';                     
                      /     .'`._.* /    .-' (                      
                    .'`._  /    ; .' .-'     ;                      
                    ; `._.:     |(    ._   _.'|                     
                    `._   ;     ; `.-'        |                     
                     |   / .-'./ .'  \ .     /:                     
                     |  +.'  \ `-.   .\ *--*' ;\                    
                     ;.' `. \ `.    /` `.    /  .                   
                    /.L-'\_: L__..-*     \   ".  \                  
                   :/ / .' `' ;   `-.     `.   \  .                 
                   / /_/     /              \   ;  \                
              |  _/ /       /          \     `./    .               
            `   .  ;       /    .'      `-.   ;      \              
           --  /  /  --   ,    /           `"' \      .             
          .   .  '       /   .'                 `.     \            
             /  /    `  /   /                  |  `-.   .           
        --  .  '   \   /                         `.  `-._\          
       .   /  /       : `*.                    :   `.    `-.        
          .  '    `   |    \                    \    `-._   `-._    
     --  /  /   \     :     ;                    \              |   
   .    .  '           ;                          `.  \      :  ;   
       /  /   `       : \    \                      `. `._  /  /    
  --  .  '  \         |  `.   `.                      `-. `'  /\    
     /  .             ;         `-.              \       `-..'  ;   
 `  .  '   `          |__                     |   `.         `-._.  
_  :  /  \              ;`-.                  :     `-.           ; 
    `"  `               |   `.                 \       `*-.__.-*"' \
' /  . \                ;_.  :`-._              `._                /
                       /   `  . ; `"*-._                       _.-` 
                     .'"'    _;  `-.__                     _.-`     
                     `-.__.-"         `""---...___...--**"' |       
                                                  `.____..--'
Bienvenue sur le serveur de camille!
Pour terminer la connexion envoyer 'FIN'.


                    """.encode())

#échange des messages avec le serveur tant que le client n'envoie pas le message 'FIN'
fin = "fin"
while(fin != "FIN"):
    #attend la réponse du client
    dataFromClient = clientConnecte.recv(10000)
    #affiche la réponse du client
    print(">" + dataFromClient.decode())
    #envoie d'un message au client
    clientConnecte.send("""


     ____ ___ _____ _   _    ____  _____ ____ _   _
    | __ )_ _| ____| \ | |  |  _ \| ____/ ___| | | |
    |  _ \| ||  _| |  \| |  | |_) |  _|| |   | | | |
    | |_) | || |___| |\  |  |  _ <| |__| |___| |_| |
    |____/___|_____|_| \_|  |_| \_\_____\____|\___/
    

    """.encode())

    if (dataFromClient.decode() == "DESSIN"):
        #envoie d'un message au client
        clientConnecte.send("FIN".encode())

    #arrete la discusion si le serveur reçoit le message 'FIN'
    if (dataFromClient.decode() == "FIN"):
        #envoie d'un message au client
        clientConnecte.send("FIN".encode())
        #affiche un message
        print("arret de la connection")
        break
 