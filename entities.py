import pygame
import pymunk

# --------------------------------------------------------

class Entity(pymunk.Body):
    def __init__(self, mass):
        pymunk.Body.__init__(self, mass, pymunk.inf)
        self.damage = 0
        
    def onRegister(self, space):
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
        
# --------------------------------------------------------
        
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