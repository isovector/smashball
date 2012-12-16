import pygame
import pymunk
from pymunk.vec2d import Vec2d

# --------------------------------------------------------

class Entity(pymunk.Body):
    def __init__(self, mass):
        pymunk.Body.__init__(self, mass, pymunk.inf)
        self.damage = 0
        self.scene = None
        
        self.__damageQueue = []
        
        
    def onRegister(self, scene):
        self.scene = scene
        
        
    def __getDamageAttenuation(self, knockback):
        t = min(self.damage / 200.0, 1)
        
        modifier = 1 + ((6 * t - 15) * t + 10) * t * t * t
        return knockback * modifier / self.mass
        
        
    def onDamaged(self, source, damage):
        if not any(source == s for s in self.__damageQueue):
            self.damage += damage.amount
            if damage.hasKnockback:
                self.velocity = self.__getDamageAttenuation(damage.knockback)
                
            self.__damageQueue.append(source)
            if len(self.__damageQueue) > 5:
                self.__damageQueue = self.__damageQueue[1:]
        
        
    def update(self, delta):
        return
        
        
    def draw(self, screen):
        return

# --------------------------------------------------------
        
class Ball(Entity):
    def __init__(self):
        Entity.__init__(self, 1)
        self.shape = pymunk.Circle(self, 16, (0, 0))
        self.shape.color = pygame.Color(120, 0, 120)
        self.shape.elasticity = 1
        
        
    def onRegister(self, scene):
        Entity.onRegister(self, scene)
        scene.space.add(self.shape)
    
        
    def update(self, delta):
        if self.position[1] < 30:
            self.velocity = Vec2d(0, 0)
            self.position = Vec2d(350, 80)
        