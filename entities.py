import pygame
import pymunk

# --------------------------------------------------------

class Entity(pymunk.Body):
    def __init__(self, mass):
        pymunk.Body.__init__(self, mass, pymunk.inf)
        self.damage = 0
        
        
    def onRegister(self, space):
        return
        
        
    def update(self, delta):
        return
        
        
    def draw(self, screen):
        return

# --------------------------------------------------------
        
class Ball(Entity):
    def __init__(self):
        Entity.__init__(self, 5)
        self.shape = pymunk.Circle(self, 12, (0, 0))
        self.shape.color = pygame.color.THECOLORS['green']
        self.shape.elasticity = 1
        
        
    def onRegister(self, space):
        space.add(self.shape)
        