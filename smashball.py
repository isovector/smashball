__version__ = "$Id:$"
__docformat__ = "reStructuredText"

import sys,math

import pygame
from pygame.locals import *
from pygame.color import *
    
import pymunk
from pymunk.vec2d import Vec2d
from pymunk.pygame_util import draw_space, from_pygame, to_pygame


def cpfclamp(f, min_, max_):
    """Clamp f between min and max"""
    return min(max(f, min_), max_)

def cpflerpconst(f1, f2, d):
    """Linearly interpolate from f1 to f2 by no more than d."""
    return f1 + cpfclamp(f2 - f1, -d, d)


class Entity(pymunk.Body):
    def __init__(self, mass):
        pymunk.Body.__init__(self, mass, pymunk.inf)
        self.damage = 0
        
    def onRegister(self, space):
        return
        
class Ball(Entity):
    def __init__(self):
        Entity.__init__(self, 5)
        self.shape = pymunk.Circle(self, 12, (0, 0))
        self.shape.color = pygame.color.THECOLORS['green']
        self.shape.elasticity = 1
        
    def onRegister(self, space):
        space.add(self.shape)
        
class Actor(Entity):
    def __init__(self):
        Entity.__init__(self, 5)
        self.head = pymunk.Circle(self, 10, (0,5))
        self.head2 = pymunk.Circle(self, 10, (0,13))
        self.head2.elasticity = 0.95
        self.feet = pymunk.Circle(self, 10, (0,-5))

        self.head.layers = self.head2.layers = 0b1000
        self.feet.collision_type = 1
    
    def onRegister(self, space):
        space.add(self.head, self.head2, self.feet)
    

class SceneGraph:
    def __init__(self, screen, space):
        self.space = space
        self.screen = screen
        self.entities = []
    
    def register(self, object):
        self.entities.append(object)
        self.space.add(object)
        object.onRegister(self.space)
    
    def hitbox(self, pos, radius, vec, source):
        pygame.draw.circle(self.screen, pygame.color.THECOLORS['pink'], to_pygame(pos, self.screen), radius)
        for entity in self.entities:
            if entity != source:
                if pos.get_distance(entity.position) < radius:
                    entity.damage += 10
                    entity.velocity = vec * entity.damage / 100
    



width, height = 690,400
fps = 60
dt = 1./fps
PLAYER_VELOCITY = 100. *2.
PLAYER_GROUND_ACCEL_TIME = 0.05
PLAYER_GROUND_ACCEL = (PLAYER_VELOCITY/PLAYER_GROUND_ACCEL_TIME)

PLAYER_AIR_ACCEL_TIME = 0.25
PLAYER_AIR_ACCEL = (PLAYER_VELOCITY/PLAYER_AIR_ACCEL_TIME)

JUMP_HEIGHT = 26.*3
JUMP_BOOST_HEIGHT = 36.
JUMP_CUTOFF_VELOCITY = 100
FALL_VELOCITY = 250.

HEAD_FRICTION = 0.7

PLATFORM_SPEED = 1

def main():
    ### PyGame init
    pygame.init()
    screen = pygame.display.set_mode((width,height)) 

    clock = pygame.time.Clock()
    running = True
    font = pygame.font.SysFont("Arial", 16)

    ### Physics stuff
    space = pymunk.Space()   
    space.gravity = 0,-1000
    # box walls 
    static = [pymunk.Segment(space.static_body, (10, 50), (330, 50), 5)
                , pymunk.Segment(space.static_body, (330, 50), (350, 50), 5)
                , pymunk.Segment(space.static_body, (350, 50), (680, 50), 5)
                , pymunk.Segment(space.static_body, (680, 50), (680, 370), 5)
                , pymunk.Segment(space.static_body, (680, 370), (10, 370), 5)
                , pymunk.Segment(space.static_body, (10, 370), (10, 50), 5)
                ]  
    static[1].color = pygame.color.THECOLORS['red']

    
    for s in static:
        s.friction = 1.
        s.group = 1
        s.elasticity = 0.9
        
    space.add(static)
    space.elasticIterations = 10


    scene = SceneGraph(screen, space)
   
    body = Actor()
    body.position = 100,100
    
    ball = Ball()
    ball.position = 200,200

    scene.register(ball)
    scene.register(body)
    

    direction = 1
    remaining_jumps = 2
    landing = {'p':Vec2d.zero(), 'n':0}
    frame_number = 0
    
    landed_previous = False
    
    while running:
        screen.fill(pygame.color.THECOLORS["black"])
        
        
        grounding = {
            'normal' : Vec2d.zero(),
            'penetration' : Vec2d.zero(),
            'impulse' : Vec2d.zero(),
            'position' : Vec2d.zero(),
            'body' : None
        }
        # find out if player is standing on ground
        
                
        def f(arbiter):
            n = -arbiter.contacts[0].normal
            if n.y > grounding['normal'].y:
                grounding['normal'] = n
                grounding['penetration'] = -arbiter.contacts[0].distance
                grounding['body'] = arbiter.shapes[1].body
                grounding['impulse'] = arbiter.total_impulse
                grounding['position'] = arbiter.contacts[0].position
        body.each_arbiter(f)
            
        well_grounded = False
        if grounding['body'] != None and abs(grounding['normal'].x/grounding['normal'].y) < body.feet.friction:
            well_grounded = True
            remaining_jumps = 2
    
        ground_velocity = Vec2d.zero()
        if well_grounded:
            ground_velocity = grounding['body'].velocity
    
        for event in pygame.event.get():
            if event.type == QUIT or \
                event.type == KEYDOWN and (event.key in [K_ESCAPE, K_q]):  
                running = False
            
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                ball.apply_impulse((ball.position - body.position + Vec2d(0, 100)).normalized() * 1000)
            
            elif event.type == KEYDOWN and event.key == K_SPACE:
                scene.hitbox(body.position + Vec2d(20, 0), 20, Vec2d(0,400), body)
                
            elif event.type == KEYDOWN and event.key == K_p:
                pygame.image.save(screen, "platformer.png")

            elif event.type == KEYDOWN and event.key == K_UP:
                if well_grounded or remaining_jumps > 0:                    
                    jump_v = math.sqrt(2.0 * JUMP_HEIGHT * abs(space.gravity.y))
                    body.velocity.y = ground_velocity.y + jump_v;
                    remaining_jumps -=1
            elif event.type == KEYUP and event.key == K_UP:                
                body.velocity.y = min(body.velocity.y, JUMP_CUTOFF_VELOCITY)
                
        # Target horizontal velocity of player
        target_vx = 0
        
        if body.velocity.x > .01:
            direction = 1
        elif body.velocity.x < -.01:
            direction = -1
        
        keys = pygame.key.get_pressed()
        if (keys[K_LEFT]):
            direction = -1
            target_vx -= PLAYER_VELOCITY
        if (keys[K_RIGHT]):
            direction = 1
            target_vx += PLAYER_VELOCITY
        if (keys[K_DOWN]):
            direction = -3
            
        body.feet.surface_velocity = target_vx,0

        
        if grounding['body'] != None:
            body.feet.friction = -PLAYER_GROUND_ACCEL/space.gravity.y
            body.head.friciton = HEAD_FRICTION
        else:
            body.feet.friction, body.head.friction = 0,0
        
        # Air control
        if grounding['body'] == None:
            body.velocity.x = cpflerpconst(body.velocity.x, target_vx + ground_velocity.x, PLAYER_AIR_ACCEL*dt)
        
        body.velocity.y = max(body.velocity.y, -FALL_VELOCITY) # clamp upwards as well?
        
       
        ### Helper lines
        for y in [50,100,150,200,250,300]:
            color = pygame.color.THECOLORS['darkgrey']
            pygame.draw.line(screen, color, (10,y), (680,y), 1)
        
        ### Draw stuff
        draw_space(screen, space)
        
        # Did we land?
        if abs(grounding['impulse'].y) / body.mass > 200 and not landed_previous:
            ##sound.play()
            landing = {'p':grounding['position'],'n':5}
            landed_previous = True
        else:
            landed_previous = False
        if landing['n'] > 0:
            pygame.draw.circle(screen, pygame.color.THECOLORS['yellow'], to_pygame(landing['p'], screen), 5)
            landing['n'] -= 1
        
        # Info and flip screen
        screen.blit(font.render("fps: " + str(clock.get_fps()), 1, THECOLORS["white"]), (0,0))
        screen.blit(font.render("Move with Left/Right, jump with Up, press again to double jump", 1, THECOLORS["darkgrey"]), (5,height - 35))
        screen.blit(font.render("Press D to toggle sprite draw, ESC or Q to quit", 1, THECOLORS["darkgrey"]), (5,height - 20))
        
       
        pygame.display.flip()
        frame_number += 1
        ### Update physics
        
        space.step(dt)
        
        clock.tick(fps)

if __name__ == '__main__':
    sys.exit(main())
