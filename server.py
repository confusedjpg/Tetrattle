import PodSixNet.Channel
import PodSixNet.Server
import sys
from time import sleep
import socket
class ClientChannel(PodSixNet.Channel.Channel):
    def Network(self, data):
        print (data)

    def Network_message(self, data):
        print("Envoyé depuis client",data)

class ServerNetwork(PodSixNet.Server.Server):
    channelClass = ClientChannel
    def __init__(self, *args, **kwargs):
        PodSixNet.Server.Server.__init__(self, *args, **kwargs)
        self.players = []

    def Connected(self, channel, addr):
        print ('Nouvelle Connection :', str(channel)[34:])
        self.players.append(channel)
        if len(self.players) == 2:
            self.SendAllPlayers("launch","test")
        channel.Send({"action": "message", "data":"Bienvenue"})  
        
    def SendAllPlayers(self,action,data):
        for p in self.players:
            p.Send({"action": action, "data":data})
        
def Launch():
    name = socket.gethostname()
    IP = socket.gethostbyname(name)
    host, port = IP,"31425"
    Serveur = ServerNetwork(localaddr=(host, int(port)))
    print("Serveur:",str(Serveur)[22:])
    print ("Lancement du serveur en localhost")
    return host,port,Serveur
#Serveur = ServerNetwork()


##    print(sys.argv)
##    if len(sys.argv) != 2:
##        print("Usage:", sys.argv[0], "host:port")
##        print("e.g.", sys.argv[0], "localhost:31425")
##    else:

##name = socket.gethostname()
##IP = socket.gethostbyname(name)
##host, port = IP,"31425"
##Serveur = ServerNetwork(localaddr=(host, int(port)))
##
##print("Serveur:",str(Serveur)[22:])
##while True:
##    Serveur.Pump()
##    sleep(0.01)
