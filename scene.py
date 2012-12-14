import pygame
import pymunk
from pymunk.pygame_util import draw_space, from_pygame, to_pygame

# --------------------------------------------------------

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
                    