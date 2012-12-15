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

class TestVNAttack(Attack):
    def start(self, instigator):
        offset = Vec2d(30, 0) * instigator.direction
        for i in range(3):
            instigator.scene.hitbox(instigator.position + offset, 15, Damage(DamageType.NORMAL, 10, offset * 8), instigator)
            yield
        for i in range(3):
            yield
            
class TestVFAttack(Attack):
    def start(self, instigator):
        offset = Vec2d(30, 0) * (instigator.direction, 1)
        for i in range(3):
            instigator.scene.hitbox(instigator.position + offset, 15, Damage(DamageType.NORMAL, 10, offset * 10), instigator)
            instigator.scene.hitbox(instigator.position + offset * 2, 25, Damage(DamageType.NORMAL, 10, offset * 20), instigator)
            yield
        for i in range(3):
            yield

class TestAttack(Attack):
    def start(self, instigator):
        for i in range(10):
            offset = Vec2d(30 + 3 * i, 0) * instigator.direction + Vec2d(0, -15 + 5 * i)
            knockback = Vec2d(100 + 25 * i, 0) * instigator.direction + Vec2d(0, 100 + 50  * i)
            instigator.scene.hitbox(instigator.position + offset, 8 + i, Damage(DamageType.NORMAL, 10, knockback), instigator)
            yield
        for i in range(10):
            yield
            
class ParsedAttack(Attack):
    def start(self, instigator):
        scene = instigator.scene
        dir = Vec2d(instigator.direction, -1)
        for i in range(2):
            yield
        scene.hitbox(instigator.position + Vec2d(115, 0) * dir, 12, Damage(DamageType.NORMAL, 5, Vec2d(0, -19) * dir * 10), instigator)
        for i in range(3):
            yield
        scene.hitbox(instigator.position + Vec2d(91, -15) * dir, 10, Damage(DamageType.NORMAL, 7, Vec2d(22, -14) * dir * 10), instigator)
        for i in range(5):
            yield
        scene.hitbox(instigator.position + Vec2d(63, -35) * dir, 9, Damage(DamageType.NORMAL, 9, Vec2d(52, -2) * dir * 10), instigator)

