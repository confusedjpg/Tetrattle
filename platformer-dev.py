import pyglet, random as rd, pymunk
from pyglet.window import key
from pymunk.pyglet_util import DrawOptions
from tetromino import *
from camera import *

options = DrawOptions() #debug

grid = set()
for x in range(0,WIDTH,CUBESIZE):
    grid.add(pyglet.shapes.Line(x,0,x,HEIGHT,2,(60,60,60,50), batch=batch, group=background))

for y in range(0,HEIGHT,CUBESIZE):
    grid.add(pyglet.shapes.Line(0,y,WIDTH,y,2,(60,60,60,50), batch=batch, group=background))

blocks = set()
bloc = Scenery.Tetromino(5, 150,150)
blocks.add(bloc)
def spawn_block(dt):
    block = Scenery.Tetromino(rd.randint(0,6), rd.randrange(CUBESIZE,WIDTH-CUBESIZE*3,CUBESIZE), HEIGHT)
    blocks.add(block)

def handle_blocks(dt):
    temp_blocks = blocks.copy()
    for block in temp_blocks:
        if block.tetro_position[1] >= CUBESIZE*3:
            block.move(0,-CUBESIZE)
        if block.tetro_position[1] < -CUBESIZE*4:
            blocks.remove(block)

walls = Scenery.Wall()

floor = pymunk.Segment(space.static_body, a=(0,0), b=(WIDTH,0), radius=10.0)
floor.friction = 1.0

def limit_velocity(body, gravity, damping, dt): #limit the maximum velocity of a given body
    max_velocity_len = 600
    pymunk.Body.update_velocity(body, gravity, damping, dt)
    l = body.velocity.length
    if l > max_velocity_len:
        scale = max_velocity_len / l
        body.velocity = body.velocity * scale

    if body.velocity[0] > 250:
        body.velocity = (250, body.velocity[1])
    if body.velocity[0] < -250:
        body.velocity = (-250, body.velocity[1])

#player's body
dyn_body = pymunk.Body(1,float('inf'))
dyn_body.position = 200,200
dyn_body.velocity_func = limit_velocity
player_shape = pymunk.Poly.create_box(dyn_body, (30,60), 1.0)#pymunk.Circle(dyn_body, radius=11)
player_shape.filter = pymunk.ShapeFilter(1)
player_shape.friction = 1.0

dyn_body2 = pymunk.Body(1,float('inf'))
dyn_body2.position = 200,200
dyn_body2.velocity_func = limit_velocity
player_shape2 = pymunk.Poly.create_box(dyn_body2, (30,60), 1.0)
player_shape2.filter = pymunk.ShapeFilter(1)

fps_display = pyglet.window.FPSDisplay(window)

keyboard = key.KeyStateHandler()
window.push_handlers(keyboard)

space.add(dyn_body, dyn_body2, player_shape, player_shape2, floor)

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

class Player(pyglet.sprite.Sprite):
    def __init__(self, shape, perso="punk"):
        self.perso = perso
        self.shape = shape
        self.body = self.shape.body

        #set sprite
        pyglet.sprite.Sprite.__init__(self, ani_dict[self.perso]["idler"]["ani"], self.body.position[0], self.body.position[1], batch = batch , group = background)

        self.scale = 2.0
        self.lastkey = "right"
        self.up = self.left = self.right = False
        self.speed = 50
        self.grounded = None
        self.reset = False
        self.old_vel = 0

    def changeanim(self):
        if self.up:
            if self.lastkey == "right":
                self.image = ani_dict[self.perso]["jumpr"]["ani"]
            else:
                self.image = ani_dict[self.perso]["jumpl"]["ani"].get_transform(flip_x=True)


        elif self.left:
            self.image = ani_dict[self.perso]["runl"]["ani"].get_transform(flip_x=True)
        
        elif self.right:
            self.image = ani_dict[self.perso]["runr"]["ani"]
        
        else:
            if self.lastkey == "right":
                self.image = ani_dict[self.perso]["idler"]["ani"]
            else:
                self.image = ani_dict[self.perso]["idlel"]["ani"].get_transform(flip_x=True)

    def move(self, dx=0, dy=0):
        self.body.apply_impulse_at_world_point((dx,dy), (self.width/2, self.height/2))
        
    def update(self):
        self.position = self.body.position[0]-self.width/3, self.body.position[1]-self.height/3, 0
        self.draw()

        #window borders collision, pymunk collisions suck at stopping the player
        x,y = self.body.position
        if x-self.shape.radius <= CUBESIZE*2:
            self.body.position = (CUBESIZE*2+self.shape.radius, y)
        if x+self.shape.radius >= WIDTH-CUBESIZE*1.6:
            self.body.position = (WIDTH-CUBESIZE*1.6-self.shape.radius,y)

        #dirty jump fix
        if self.body.velocity[1] == 0 and self.old_vel <= 0:
            self.grounded = True
        else:
            self.grounded = False
        #movement
        if self.left:
            self.move(-self.speed)
        if self.right:
            self.move(self.speed)
        if self.up and self.grounded:
            self.body.update_velocity(self.body, (0,60), 1.0, 7.0)
            self.body.apply_impulse_at_world_point((0,90), (self.width/2, self.height/2))
            self.changeanim()

        #stop sliding lmao
        if self.grounded:
            if not (self.right or self.left):
                self.body.velocity = (0, self.body.velocity[1])

        if self.reset and self.grounded:
            self.changeanim()
            self.reset = False
        
        self.old_vel = self.body.velocity[1]

player = Player(player_shape)
player2 = Player(player_shape2)

camera = Camera()

@window.event
def on_draw():
    window.clear()
    player.update()
    player2.update()
    camera.offset_x, camera.offset_y = max(player.body.position, player2.body.position)
    camera.begin()
    batch.draw()

    space.debug_draw(options) #debug drawing, change into proper drawing

    space.step(1/60)
    fps_display.draw() #debug


@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.LEFT:
        player.lastkey = "left"
        player.left = True
        player.changeanim()
    if symbol == key.RIGHT:
        player.lastkey = "right"
        player.right = True
        player.changeanim()
    if symbol == key.UP or symbol == key.SPACE:
        player.up = True
    
    if symbol == key.Q:
        player2.lastkey = "left"
        player2.left = True
        player2.changeanim()
    if symbol == key.D:
        player2.lastkey = "right"
        player2.right = True
        player2.changeanim()
    if symbol == key.Z or symbol == key.SPACE:
        player2.up = True

@window.event
def on_key_release(symbol, modifiers):
    if symbol == key.LEFT:
        player.left = False
        if player.grounded:
            player.changeanim()
    if symbol == key.RIGHT:
        player.right = False
        if player.grounded:
            player.changeanim()
    if symbol == key.UP or symbol == key.SPACE:
        player.up = False
        player.reset = True
    
    if symbol == key.Q:
        player2.left = False
        if player2.grounded:
            player2.changeanim()
    if symbol == key.D:
        player2.right = False
        if player2.grounded:
            player2.changeanim()
    if symbol == key.Z or symbol == key.SPACE:
        player2.up = False
        player2.reset = True

pyglet.clock.schedule_once(spawn_block, .1)
pyglet.clock.schedule_interval(spawn_block, 5.0)
pyglet.clock.schedule_interval(handle_blocks, .5)
run()
