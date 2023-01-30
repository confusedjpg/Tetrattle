import pyglet,time, random as rd
from pyglet.gl import glClearColor
from server import *
screen = pyglet.window.Window(1280,900,resizable=False)
# create windows in custom resolution
keyboard = pyglet.window.key.KeyStateHandler()
screen.push_handlers(keyboard)
# Get keyboards event
WIDTH, HEIGHT = screen.get_size()
#size of windows

Serveur = False

batchmenu = pyglet.graphics.Batch()
batchselect = pyglet.graphics.Batch()
batchjoin = pyglet.graphics.Batch()
batchserver = pyglet.graphics.Batch()
#optimize draw
scene = 0
#Change scene
background = pyglet.graphics.Group(order=0)
foreground = pyglet.graphics.Group(order=1)
#create a z order for put in forward elements

pyglet.font.add_file('content/font/ThaleahFat.ttf')
police = pyglet.font.load('ThaleahFat',16)

home = pyglet.text.Label('Bienvenue dans Tetrattle',font_name='ThaleahFat',font_size=70,
                          x=screen.width//2, y=screen.height/1.2,
                          anchor_x='center', anchor_y='center',batch = batchmenu)

play = pyglet.text.Label('Jouer',font_name='ThaleahFat',font_size=55,
                          x=screen.width//2, y=screen.height/2+8,
                          anchor_x='center', anchor_y='center',batch = batchmenu)

exite = pyglet.text.Label('Quitter',font_name='ThaleahFat',font_size=55,
                          x=screen.width//2, y=screen.height/1.2-500,
                          anchor_x='center', anchor_y='center',batch = batchmenu)

# Create Text of main menu


pressed_g = pyglet.image.SolidColorImagePattern((6,179,3,255)).create_image(400,150)
depressed_g = pyglet.image.SolidColorImagePattern((4,235,0,255)).create_image(400,150)

pressed_r = pyglet.image.SolidColorImagePattern((179,6,3,255)).create_image(400,150)
depressed_r = pyglet.image.SolidColorImagePattern((235,4,0,255)).create_image(400,150)

pressed_rmini = pyglet.image.SolidColorImagePattern((179,6,3,255)).create_image(200,75)
depressed_rmini = pyglet.image.SolidColorImagePattern((235,4,0,255)).create_image(200,75)

pressed_b = pyglet.image.SolidColorImagePattern((6,0,179,255)).create_image(400,150)
depressed_b = pyglet.image.SolidColorImagePattern((4,0,235,255)).create_image(400,150)

pressed_bmini = pyglet.image.SolidColorImagePattern((6,0,179,255)).create_image(300,100)
depressed_bmini = pyglet.image.SolidColorImagePattern((4,0,235,255)).create_image(300,100)

# Create rectangle button

from PodSixNet.Connection import ConnectionListener, connection

class PushButtonPlay(pyglet.gui.PushButton):
    def on_press(self):
        #batchmenu.delete()
        global scene
        scene = 1
        print(scene)
        screen.push_handlers(buttonheberg)
        screen.push_handlers(buttonrejoin)
        screen.push_handlers(buttonretour)
        screen.remove_handlers(buttong)
        screen.remove_handlers(buttonr)
        #pyglet.app.exit()

class PushButtonQuit(pyglet.gui.PushButton):
    def on_press(self):
        screen.close()
        pyglet.app.exit()

class PushButtonReturn(pyglet.gui.PushButton):
    def on_press(self):
        global scene
        if scene == 1:
            scene = 0
            screen.push_handlers(buttong)
            screen.push_handlers(buttonr)
            screen.remove_handlers(buttonheberg)
            screen.remove_handlers(buttonrejoin)
            screen.remove_handlers(buttonretour)
        if scene == 2:
            scene = 1
            screen.remove_handlers(textip)
            screen.remove_handlers(textport)
            screen.remove_handlers(buttonretour2)
            screen.push_handlers(buttonheberg)
            screen.push_handlers(buttonrejoin)
            screen.push_handlers(buttonretour)
        print('return')

class PushButtonHeberg(pyglet.gui.PushButton):
    def on_press(self):
        global scene
        global Serveur
        scene = 2
        screen.remove_handlers(buttonheberg)
        screen.remove_handlers(buttonrejoin)
        screen.remove_handlers(buttonretour)
        IPshowlabel.text,Portshowlabel.text,Serveur = Launch()
        ClientNetwork = MyNetworkListener(IPshowlabel.text,int(Portshowlabel.text))
        print(scene)

class PushButtonJoin(pyglet.gui.PushButton):
    def on_press(self):
        global scene
        scene = 3
        screen.remove_handlers(buttonheberg)
        screen.remove_handlers(buttonrejoin)
        screen.remove_handlers(buttonretour)
        screen.push_handlers(textip)
        screen.push_handlers(textport)
        screen.push_handlers(buttonconnect)
        screen.push_handlers(buttonretour2)
        print(scene)

#Create all buttons

ClientNetwork = False
class PushButtonConnect(pyglet.gui.PushButton):
    def on_press(self):
        print(textip.value,int(textport.value))
        global ClientNetwork
        ClientNetwork = MyNetworkListener(textip.value,int(textport.value))
        # Create client network
    
buttong = PushButtonPlay(WIDTH/2-pressed_g.width/2,HEIGHT/2-pressed_g.height/2+5,batch = batchmenu,pressed = pressed_g,depressed = depressed_g)
buttonr = PushButtonQuit(WIDTH/2-pressed_r.width/2,HEIGHT/2-pressed_r.height/2-200,batch = batchmenu,pressed = pressed_r,depressed = depressed_r)

screen.push_handlers(buttong)
screen.push_handlers(buttonr)

subtitle1 = pyglet.text.Label('Mode de connexion',font_name='ThaleahFat',font_size=70,
                          x=screen.width//2, y=screen.height/1.2,
                          anchor_x='center', anchor_y='center',batch = batchselect)

heberg = pyglet.text.Label('Heberger',font_name='ThaleahFat',font_size=55,
                          x=screen.width//2, y=screen.height/2+8,
                          anchor_x='center', anchor_y='center',batch = batchselect)

rejoin = pyglet.text.Label('Rejoindre',font_name='ThaleahFat',font_size=55,
                          x=screen.width//2, y=screen.height/1.2-500,
                          anchor_x='center', anchor_y='center',batch = batchselect)

retour = pyglet.text.Label('Retour',font_name='ThaleahFat',font_size=40,
                          x=screen.width//2, y=screen.height*0.1,
                          anchor_x='center', anchor_y='center',batch = batchselect)

buttonheberg = PushButtonHeberg(WIDTH/2-pressed_b.width/2,HEIGHT/2-pressed_b.height/2+5,batch = batchselect,pressed = pressed_b,depressed = depressed_b)
buttonrejoin = PushButtonJoin(WIDTH/2-pressed_r.width/2,HEIGHT/2-pressed_r.height/2-200,batch = batchselect,pressed = pressed_g,depressed = depressed_g)
buttonretour = PushButtonReturn(WIDTH/2-pressed_rmini.width/2,HEIGHT*0.1-pressed_rmini.height/2,batch = batchselect,pressed = pressed_rmini,depressed = depressed_rmini)
#### CONNECT PAGE #### 
class TextEntryIP(pyglet.gui.TextEntry):
    def __init__(self, text, x, y, width, fontsize,
                 color=(255, 255, 255, 255),
                 text_color=(0, 0, 0, 255),
                 caret_color=(0, 0, 0),
                 batch=None, group=None):

        self._doc = pyglet.text.document.UnformattedDocument(text)
        self._doc.set_style(0, len(self._doc.text), dict(color=text_color,
                                                         font_size=fontsize,
                                                         font_name='ThaleahFat',
                                                         bold=True))
        font = self._doc.get_font()
        height = font.ascent - font.descent
        y = y + font.descent

        self._user_group = group

        # Rectangular outline with 2-pixel pad:
        self._pad = p = 2
        self._outline = pyglet.shapes.Rectangle(
            x-p, y-p, width+p+p, height+p+p, color[:3], batch)
        self._outline.opacity = color[3]

        # Text and Caret:
        self._layout = pyglet.text.layout.IncrementalTextLayout(
            self._doc, width, height, multiline=False, batch=batch)
        self._layout.x = x
        self._layout.y = y
        self._caret = pyglet.text.caret.Caret(self._layout, color=caret_color)
        self._caret.visible = False

        self._focus = False

        super(pyglet.gui.TextEntry, self).__init__(x, y, width, height)
    def on_mouse_press(self,x,y,buttons,modifiers):
        if not self.enabled:
            return
        if self._check_hit(x, y):
            self._set_focus(True)
            self._caret.on_mouse_press(x, y, buttons, modifiers)
        else:
            self._set_focus(False)
        
        #super(pyglet.gui.TextEntry, self).on_mouse_drag(x, y)


subtitle2 = pyglet.text.Label("Entrez l'adresse IP du Joueur",font_name='ThaleahFat',font_size=70,
                          x=screen.width//2, y=screen.height/1.2,
                          anchor_x='center', anchor_y='center',batch = batchjoin)

IPlabel = pyglet.text.Label('Adresse IP :',font_name='ThaleahFat',font_size=55,
                          x=screen.width//2.23, y=screen.height/1.7+8,
                          anchor_x='center', anchor_y='center',batch = batchjoin)

textip = TextEntryIP('10.72.212.145',fontsize = 50,x=screen.width//2-500/2, y=screen.height/2+8,width=500,color = (87,87,87,255),
                     text_color=(255, 255, 255, 255),batch = batchjoin)

Portlabel = pyglet.text.Label('Port :',font_name='ThaleahFat',font_size=55,
                          x=screen.width//2.67, y=screen.height/2.4+5,
                          anchor_x='center', anchor_y='center',batch = batchjoin)

textport = TextEntryIP('31425',fontsize = 50,x=screen.width//2-500/2, y=screen.height/3,width=500,color = (87,87,87,255),
                     text_color=(255, 255, 255, 255),batch = batchjoin)

connectlabel = pyglet.text.Label('Rejoindre',font_name='ThaleahFat',font_size=50,
                          x=screen.width//2, y=screen.height/4.4,
                          anchor_x='center', anchor_y='center',batch = batchjoin)

buttonconnect = PushButtonConnect(WIDTH/2-pressed_bmini.width/2,HEIGHT/4.5-pressed_bmini.height/2,batch = batchjoin,pressed = pressed_bmini,depressed = depressed_bmini)

retour2 = pyglet.text.Label('Retour',font_name='ThaleahFat',font_size=40,
                          x=screen.width//2, y=screen.height*0.1,
                          anchor_x='center', anchor_y='center',batch = batchjoin)

buttonretour2 = PushButtonReturn(WIDTH/2-pressed_rmini.width/2,HEIGHT*0.1-pressed_rmini.height/2,batch = batchjoin,pressed = pressed_rmini,depressed = depressed_rmini) 
#### CONNECT PAGE #### 


#### SERVER PAGE #### 

subtitle2 = pyglet.text.Label("Votre IP et Port a partager",font_name='ThaleahFat',font_size=70,
                          x=screen.width//2, y=screen.height/1.2,
                          anchor_x='center', anchor_y='center',batch = batchserver)

IPshowlabel = pyglet.text.Label("En Attente...",font_name='ThaleahFat',font_size=70,
                          x=screen.width//2, y=screen.height/2,
                          anchor_x='center', anchor_y='center',batch = batchserver)

Portshowlabel = pyglet.text.Label("En Attente...",font_name='ThaleahFat',font_size=70,
                          x=screen.width//2, y=screen.height/3,
                          anchor_x='center', anchor_y='center',batch = batchserver)

#### SERVER PAGE ####

class MyNetworkListener(ConnectionListener):
    def __init__(self,IP="",port=0):
        self.Connect((str(IP), port))
        print("IP=",str(connection)[29:])
        #connection.Send({'action':'message','data':'Merci à vous'})

    def ConnectServ(self,IP="",port=0):
        self.Connect((IP, port))
        print("IP=",str(connection)[29:])
       
    def Network(self, data):
        print ('Network Info:', data)
        
    def Network_connected(self, data):
        print ("Tu es connecté")
        
    def Network_error(self, data):
        print ("Erreur:", data['error'][1])
        
    def Network_disconnected(self, data):
        print ("Tu es deconnecté")
        
    def Network_message(self, data):
        print("Message du serveur :",data)

    def Network_launch(self, data):
        print("Lancement de la partie")
        global scene
        scene = 20
        screen.remove_handlers(buttonconnect)
        screen.remove_handlers(buttonretour2)
        pyglet.app.exit()

# Client Network

@screen.event
def on_draw():
    screen.clear()
    if scene == 0:
        batchmenu.draw()
    elif scene == 1:
        batchselect.draw()
    elif scene == 2:
        batchserver.draw()
    elif scene == 3:
        batchjoin.draw()
    if Serveur:
        Serveur.Pump()
    if ClientNetwork:
        ClientNetwork.Pump()
        connection.Pump()
    print('batchmenu')
pyglet.app.run()

glClearColor(255, 255, 255, 1.0)
# blank background
batch = pyglet.graphics.Batch()
## ANIMATION ##
ani_dict = {"biker":{
            "idler":{"ani":False,"columns":4,"duration":0.1},
            "idlel":{"ani":False,"columns":4,"duration":0.1},
            "runr":{"ani":False,"columns":6,"duration":0.1},
            "runl":{"ani":False,"columns":6,"duration":0.1},
            "jumpr":{"ani":False,"columns":6,"duration":0.12},
            "jumpl":{"ani":False,"columns":6,"duration":0.12},
            "deatha":{"ani":False,"columns":6,"duration":0.1}
            },
            "cyborg":{
            "idler":{"ani":False,"columns":4,"duration":0.1},
            "idlel":{"ani":False,"columns":4,"duration":0.1},
            "runr":{"ani":False,"columns":6,"duration":0.1},
            "runl":{"ani":False,"columns":6,"duration":0.1},
            "jumpr":{"ani":False,"columns":6,"duration":0.12},
            "jumpl":{"ani":False,"columns":6,"duration":0.12},
            "deatha":{"ani":False,"columns":6,"duration":0.1}
            },
            "punk":{
            "idler":{"ani":False,"columns":4,"duration":0.1},
            "idlel":{"ani":False,"columns":4,"duration":0.1},
            "runr":{"ani":False,"columns":6,"duration":0.1},
            "runl":{"ani":False,"columns":6,"duration":0.1},
            "jumpr":{"ani":False,"columns":6,"duration":0.12},
            "jumpl":{"ani":False,"columns":6,"duration":0.12},
            "deatha":{"ani":False,"columns":6,"duration":0.1}
            }}
for k in ani_dict:
    for i in ani_dict[k]:
        sprite = pyglet.resource.image('content/characters/'+k+'/'+k+'_'+i[:-1]+'.png')
        image_grid = pyglet.image.ImageGrid(sprite, rows=1, columns=ani_dict[k][i]["columns"])
        image_grid.anchor_x,image_grid.anchor_y = image_grid.width//2,image_grid.height//2
        ani = pyglet.image.Animation.from_image_sequence(image_grid, duration=ani_dict[k][i]["duration"])
        if i[-1] == "l":
            for f in ani.frames:
                f.image.anchor_x = ani.get_max_width()//2          
        ani_dict[k][i]["ani"] = ani

##############
class Player:
    def __init__(self, size, color=(255,255,255),perso="biker"):
        self.perso = perso
        self.sprite = pyglet.sprite.Sprite(ani_dict[self.perso]["idler"]["ani"],batch = batch , group = foreground)
        self.sprite.scale = 2.0
        self.sprite.x = 500
        self.sprite.y = 40
        self.key_left = False
        self.key_right = False
        self.key_space = False
        self.lastkey = "right"
        self.gravity = 0
        self.bottom = 40
        self.reset = False
        self.cpt = 0
        # All variables needed for a work player
    def update(self):
        if self.key_left:
            self.sprite.x -= 5
        if self.key_right:
            self.sprite.x += 5
        # Move player with command
        if self.sprite.y == self.bottom:
                if self.key_space:
                    self.gravity = -20
                    self.changeanim()
                elif self.reset:
                    self.reset = not self.reset
                    self.changeanim()
        # For stop jump animation
        self.gravity += 1
        self.move(0,-self.gravity)
        # Gravity of player
        #player.handle_collision(objet)
        
    def move(self,dx=0,dy=0):
        self.sprite.x = self.sprite.x+dx
        self.sprite.y = self.sprite.y+dy
        if self.sprite.y < self.bottom:
            self.sprite.y = self.bottom

    def tp(self, x,y):
        self.sprite.x, self.sprite.y = x,y
        
    def changeanim(self):
        if not self.reset:
            if self.key_space:
                if self.lastkey == "right":
                    self.sprite.image = ani_dict[self.perso]["jumpr"]["ani"]
                else:
                    self.sprite.image = ani_dict[self.perso]["jumpl"]["ani"].get_transform(flip_x=True)
                self.reset = True
                self.key_space = False
                    
            elif self.key_left:
                self.sprite.image = ani_dict[self.perso]["runl"]["ani"].get_transform(flip_x=True)
            elif self.key_right:
                self.sprite.image = ani_dict[self.perso]["runr"]["ani"]
            else:
                if self.lastkey == "right":
                    self.sprite.image = ani_dict[self.perso]["idler"]["ani"]
                else:
                    self.sprite.image = ani_dict[self.perso]["idlel"]["ani"].get_transform(flip_x=True)
                # idle

class Grille:
    def __init__(self,size):
        self.rect = pyglet.shapes.BorderedRectangle(x=WIDTH/2-(size[0]/2), y=(HEIGHT-size[1])/2, width=size[0], height=size[1], border_color=(0,0,0),border = 1,batch = batch , group = background)
        self.rect.opacity = 0
        self.minirect = []
        for x in range(10):
            for y in range(22):
                self.minirect.append(pyglet.shapes.BorderedRectangle(x=self.rect.x+(x*(self.rect.width/10)), y=self.rect.y+(y*(self.rect.height/22)), width=self.rect.width/10, height=self.rect.height/22, border_color=(0,0,0),border = 1,batch = batch , group = background))
                self.minirect[-1].opacity = 0

carre = Grille((WIDTH/3.3,HEIGHT/1.1))

player = Player((50,50))


@screen.event
def on_draw():
    #screen.clear()
    print('batch')
    batch.draw()
    player.update()
# Draw elements

@screen.event
def on_key_press(key, modifiers):
    if key == pyglet.window.key.LEFT:
        player.key_left = True
        player.lastkey = "left"
        player.changeanim()
    elif key == pyglet.window.key.RIGHT:
        player.key_right = True
        player.lastkey = "right"
        player.changeanim()
    if key == pyglet.window.key.SPACE:
        if not player.reset:
            player.key_space = True
# Detect key press

@screen.event
def on_key_release(key, modifiers):
    if key == pyglet.window.key.LEFT:
        player.key_left = False
        player.changeanim()
    elif key == pyglet.window.key.RIGHT:
        player.key_right = False
        player.changeanim()
    if key == pyglet.window.key.SPACE:
        pass
# Detect key release
print('lancement')
pyglet.app.run()
