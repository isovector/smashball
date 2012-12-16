from collections import deque

import pygame
from pygame.locals import *

from enum import *

# --------------------------------------------------------

class InputEvent:
    def __init__(self, key, down):
        self.key = key
        self.down = down

# --------------------------------------------------------

class Controller:
    def __init__(self, actor):
        self.actor = actor
        self.events = deque()
        self.xdir = 0
        self.ydir = 0
    

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            self.xdir = -1
        elif keys[K_RIGHT]:
            self.xdir = 1
        else:
            self.xdir = 0
            
        if keys[K_UP]:
            self.ydir = 1
        elif keys[K_DOWN]:
            self.ydir = -1
        else:
            self.ydir = 0


    def queueInput(self, base, down):
        if base > Key.GRAB:
            if self.ydir == 1:
                base += 1
            elif self.ydir == -1:
                base += 2
            elif self.xdir == self.actor.direction:
                base += 3
            elif self.xdir != 0:
                base += 4
        self.events.append(InputEvent(base, down))

        
    def onEvent(self, event):
        down = True
        if event.type == KEYDOWN or event.type == KEYUP:
            if event.type == KEYUP:
                down = False
            if event.key == K_z:
                self.queueInput(Key.JUMP, down)
            elif event.key == K_x:
                self.queueInput(Key.GRAB, down)
            elif event.key == K_c:
                self.queueInput(Key.CN, down)
            elif event.key == K_v:
                self.queueInput(Key.VN, down)

        
    def pop(self):
        return self.events.popleft()