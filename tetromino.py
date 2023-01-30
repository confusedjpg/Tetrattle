import pyglet, pymunk
from time import time,sleep
from pymunk.pyglet_util import DrawOptions

#physics stuff
space = pymunk.Space()
space.collision_bias = 0
space.gravity = 0,-1400

# _#_#_## CONSTANTES ##_#_#_
CUBESIZE = 36
HALF = CUBESIZE //2 # used to determine the anchor of the image
WIDTH, HEIGHT = CUBESIZE*24,CUBESIZE*24

window = pyglet.window.Window(WIDTH, HEIGHT)

batch = pyglet.graphics.Batch()
background = pyglet.graphics.Group(order=0)
foreground = pyglet.graphics.Group(order=1)
#fieldOfPlay = pyglet.window.Window(CUBESIZE*12,CUBESIZE*24,caption='Tetris Duel')



tetrominoImage = pyglet.image.load('assets/tetromino.png')
tetrominoImage.anchor_x = 18
tetrominoImage.anchor_y = 18

class Building_blocks:
    '''class of tetromino constituing block'''
    def __init__(self,x=0,y=0,colour=(100,100,100),batch=batch):
        self.body = pymunk.Body(1,float("inf"),body_type=pymunk.Body.KINEMATIC)
        self.shape = pymunk.Poly.create_box(self.body, size=(CUBESIZE,CUBESIZE))
        space.add(self.body, self.shape)
        self.sprite = pyglet.sprite.Sprite(img=tetrominoImage,
                                           x=x+HALF, y=y+HALF,
                                           batch=batch,
                                           group=foreground
                                           )
        self.sprite.color = colour
    def move(self,nx,ny):
        '''don't forget that anchor is in the middle of the image!'''
        self.sprite.position = (nx,ny,0)
        self.body.position = nx,ny
    def def_colour(self,r,g,b):
        self.sprite.color = (r,g,b)

class Scenery:
# all decor objects which the user can interact with
# mainly for collisions etc
# collection of Building_blocks-class objects

    class Wall:
        # Would be nice to not have to redraw it each frame.
        # Could even be just an image w/ a player-side
        # limitation to not go through.
        def __init__(self):
            self.L = []
            for i in range(2):
                for j in range(0,HEIGHT,CUBESIZE):
                    self.L.append(Building_blocks(x=i*(WIDTH-CUBESIZE),y=j))
                
##        # ici le background
##        # voir pour un group background
    class Tetromino:
        # ici les tetrominos
        # voir pour un group middle (foreground -> persos et powerups)
        def __init__(self,n,x=0,y=0):
            '''Gets the right config :
            0 -> cube,
            1 -> L,
            2 -> I,
            3 -> Z,
            4 -> S,
            5 -> T,
            6 -> reverse L
            objects spawns upper right of coordinates'''
            # doesn't check for a valid n

            self.L = []
            self.type = n # hopeless attempt to facilitate the tetrominoes rotation
            self.tetro_position = (x,y)
            match n:
                case 0:
                    colour = (225,225,0) #yellow cube
                    self.L.append(Building_blocks(x=x,y=y,colour=colour))
                    self.L.append(Building_blocks(x=x,y=y+CUBESIZE,colour=colour))
                    self.L.append(Building_blocks(x=x+CUBESIZE,y=y,colour=colour))
                    self.L.append(Building_blocks(x=x+CUBESIZE,y=y+CUBESIZE,colour=colour))
                case 1:
                    colour = (225,165,0) #orange L
                    self.L.append(Building_blocks(x=x,y=y,colour=colour))
                    self.L.append(Building_blocks(x=x,y=y+CUBESIZE,colour=colour))
                    self.L.append(Building_blocks(x=x+CUBESIZE,y=y,colour=colour))
                    self.L.append(Building_blocks(x=x,y=y+2*CUBESIZE,colour=colour))
                case 2:
                    colour = (0,255,255) #cyan I
                    self.L.append(Building_blocks(x=x,y=y,colour=colour))
                    self.L.append(Building_blocks(x=x,y=y+CUBESIZE,colour=colour))
                    self.L.append(Building_blocks(x=x,y=y+2*CUBESIZE,colour=colour))
                    self.L.append(Building_blocks(x=x,y=y+3*CUBESIZE,colour=colour))
                case 3:
                    colour = (255,0,0) #red Z
                    self.L.append(Building_blocks(x=x+CUBESIZE,y=y,colour=colour))
                    self.L.append(Building_blocks(x=x+CUBESIZE,y=y+CUBESIZE,colour=colour))
                    self.L.append(Building_blocks(x=x,y=y+CUBESIZE,colour=colour))
                    self.L.append(Building_blocks(x=x+2*CUBESIZE,y=y,colour=colour))
                case 4:
                    colour = (0,255,0) #green S
                    self.L.append(Building_blocks(x=x,y=y,colour=colour))
                    self.L.append(Building_blocks(x=x+CUBESIZE,y=y,colour=colour))
                    self.L.append(Building_blocks(x=x+CUBESIZE,y=y+CUBESIZE,colour=colour))
                    self.L.append(Building_blocks(x=x+2*CUBESIZE,y=y+CUBESIZE,colour=colour))
                case 5:
                    colour = (255,0,255) #magenta T
                    self.L.append(Building_blocks(x=x,y=y,colour=colour))
                    self.L.append(Building_blocks(x=x+CUBESIZE,y=y,colour=colour))
                    self.L.append(Building_blocks(x=x+CUBESIZE,y=y+CUBESIZE,colour=colour))
                    self.L.append(Building_blocks(x=x+2*CUBESIZE,y=y,colour=colour))
                case 6:
                    colour = (0,0,255) #blue reverse L
                    self.L.append(Building_blocks(x=x,y=y,colour=colour))
                    self.L.append(Building_blocks(x=x+CUBESIZE,y=y,colour=colour))
                    self.L.append(Building_blocks(x=x+CUBESIZE,y=y+CUBESIZE,colour=colour))
                    self.L.append(Building_blocks(x=x+CUBESIZE,y=y+2*CUBESIZE,colour=colour))
                    

        def move(self,x,y):
            '''moves the whole tetromino relative to previous position'''
            for block in self.L:
                block.move(block.sprite.position[0]+x,block.sprite.position[1]+y)
            self.tetro_position = (self.tetro_position[0]+x,self.tetro_position[1]+y)

        def rotate(self):
            '''rotates around the most bottom then left cube'''
            # due to the definition order of the pieces
            op = self.L[0].sprite.position
            for block in self.L:
                # rotates each block around the origin (0;0)
                block.sprite.position = (-block.sprite.position[1],block.sprite.position[0],0)
                block.sprite.rotation = -90
            # brings it back to the correct position i.e. relative to the block of index 0
            np = self.L[0].sprite.position
            self.move(op[0]-np[0],op[1]-np[1])

def run():
    pyglet.app.run()