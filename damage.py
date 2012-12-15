import pymunk
from pymunk.vec2d import Vec2d

from enum import *

# --------------------------------------------------------

DamageType = enum('NORMAL')

# --------------------------------------------------------

class Damage:
    def __init__(self, type = DamageType.NORMAL, amount = 0, knockback = None):
        self.type = type
        self.amount = amount
        self.knockback = knockback
        self.hasKnockback = True
        
        if knockback is None:
            self.hasKnockback = False
            
# --------------------------------------------------------

class Attack:
    def start(self, instigator):
        return
        
# --------------------------------------------------------

class TestAttack(Attack):
    def start(self, instigator):
        for i in range(10):
            offset = Vec2d(30 + 3 * i, 0) * instigator.direction + Vec2d(0, -15 + 5 * i)
            knockback = Vec2d(100 + 25 * i, 0) * instigator.direction + Vec2d(0, 100 + 20  * i)
            instigator.scene.hitbox(instigator.position + offset, 8 + i, Damage(DamageType.NORMAL, 10, knockback), instigator)
            yield
        for i in range(10):
            yield
            