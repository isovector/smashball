import math

import pygame
from pygame.locals import *
from pygame.color import *
    
import pymunk
from pymunk.vec2d import Vec2d
from pymunk.pygame_util import draw_space, from_pygame, to_pygame

from damage import *
from controller import *
from entities import *
from enum import *

# --------------------------------------------------------

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

# --------------------------------------------------------

def cpfclamp(f, min_, max_):
    """Clamp f between min and max"""
    return min(max(f, min_), max_)

def cpflerpconst(f1, f2, d):
    """Linearly interpolate from f1 to f2 by no more than d."""
    return f1 + cpfclamp(f2 - f1, -d, d)
    
# --------------------------------------------------------
        
class Actor(Entity):
    def __init__(self):
        Entity.__init__(self, 5)
        self.head = pymunk.Circle(self, 18, (0,5))
        self.head2 = pymunk.Circle(self, 18, (0,18))
        self.head2.elasticity = 0.95
        self.feet = pymunk.Circle(self, 18, (0,-8))

        self.head.layers = self.head2.layers = 0b1000
        self.feet.collision_type = 1
        
        self.moveStyle = MoveStyle.PHYSICS_DRIVEN
        self.direction = 1
        self.jumpsLeft = 1
        self.onGround = False
        self.helpless = False
        
        self.isBusy = False
        self.controller = Controller(self)
        
        self.__currentAttack = None
        self.__groundVelocity = Vec2d.zero()
                    
                    
    def onRegister(self, scene):
        Entity.onRegister(self, scene)
        scene.space.add(self.head, self.head2, self.feet)
    
    
    def onInput(self, input):
        if input.key == Key.JUMP:
            if input.down and (self.onGround or self.jumpsLeft > 0):
                jump_v = math.sqrt(2.0 * JUMP_HEIGHT * abs(self.scene.space.gravity.y))
                self.velocity.y = self.__groundVelocity.y + jump_v;
                self.jumpsLeft -=1
            elif not input.down:
                self.velocity.y = min(self.velocity.y, JUMP_CUTOFF_VELOCITY)
        elif input.down:
            if input.key == Key.VN:
                self.__currentAttack = TestVNAttack().start(self)
            elif input.key == Key.VF:
                self.__currentAttack = TestVFAttack().start(self)
            elif input.key == Key.VD:
                self.__currentAttack = TestVDAttack().start(self)
            elif input.key == Key.CD:
                self.__currentAttack = TestCDAttack().start(self)
            elif input.key == Key.CU:
                self.__currentAttack = TestCUAttack().start(self)
            elif input.key == Key.CN:
                self.__currentAttack = TestCNAttack().start(self)
            else:
                self.__currentAttack = TestAttack().start(self)
        
        
    def update(self, delta):
        self.controller.update()
        
        self.isBusy = self.__currentAttack is not None
        
        if len(self.controller.events) > 0:
            inputEvent = self.controller.pop()
            if not self.isBusy and not self.helpless:
                self.onInput(inputEvent)
        
        if self.isBusy:
            try:
                 self.__currentAttack.next()     
            except StopIteration:
                 self.__currentAttack = None
        
        self.onGround = False
        
        grounding = {
            'normal' : Vec2d.zero(),
            'penetration' : Vec2d.zero(),
            'impulse' : Vec2d.zero(),
            'position' : Vec2d.zero(),
            'body' : None,
        }
        
        def onHit(arbiter):
            n = -arbiter.contacts[0].normal
            if n.y > grounding['normal'].y:
                grounding['normal'] = n
                grounding['penetration'] = -arbiter.contacts[0].distance
                grounding['body'] = arbiter.shapes[1].body
                grounding['impulse'] = arbiter.total_impulse
                grounding['position'] = arbiter.contacts[0].position
        self.each_arbiter(onHit)
        
        if grounding['body'] != None and abs(grounding['normal'].x/grounding['normal'].y) < self.feet.friction:
            self.onGround = True
            self.helpless = False
            self.jumpsLeft = 1
    
        if self.moveStyle == MoveStyle.PHYSICS_DRIVEN:
            self.__groundVelocity = Vec2d.zero()
            if self.onGround:
                self.__groundVelocity = grounding['body'].velocity
                
            target_vx = 0
            
            if not self.isBusy:
                xdir = self.controller.xdir
                if xdir != 0:
                    if self.onGround:
                        self.direction = xdir
                    target_vx += PLAYER_VELOCITY * xdir
                
            self.feet.surface_velocity = target_vx,0
            
            if grounding['body'] != None:
                self.feet.friction = -PLAYER_GROUND_ACCEL/self.scene.space.gravity.y
                self.head.friciton = HEAD_FRICTION
            else:
                self.feet.friction, self.head.friction = 0,0
            
            # Air control
            if not self.isBusy:
                if grounding['body'] == None:
                    self.velocity.x = cpflerpconst(self.velocity.x, target_vx + self.__groundVelocity.x, PLAYER_AIR_ACCEL*delta)
            
            self.velocity.y = max(self.velocity.y, -FALL_VELOCITY)
        