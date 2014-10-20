import pygame
from pygame.locals import *
from pygame.color import *

import pymunk
from pymunk.pygame_util import from_pygame, to_pygame

# --------------------------------------------------------

class SceneGraph:
    def __init__(self, screen, space):
        self.space = space
        self.screen = screen
        self.entities = []


    def register(self, object):
        self.entities.append(object)
        self.space.add(object)
        object.onRegister(self)


    def hitbox(self, attack, pos, radius, damage, source):
        numHit = 0
        pygame.draw.circle(self.screen, pygame.color.THECOLORS['pink'], to_pygame(pos, self.screen), radius)
        for entity in self.entities:
            if entity != source:
                if pos.get_distance(entity.position) < radius:
                    numHit += 1
                    entity.onDamaged(attack, damage)
        return numHit


    def update(self, delta):
        for entity in self.entities:
            entity.update(delta)


    def draw(self, screen):
        for y in [50,100,150,200,250,300]:
            color = pygame.color.THECOLORS['darkgrey']
            pygame.draw.line(screen, color, (10,y), (690,y), 1)
        pygame.draw.line(screen, color, (350,30), (350,350), 1)

        pymunk.pygame_util.draw(screen, self.space)

        for entity in self.entities:
            entity.draw(screen)

