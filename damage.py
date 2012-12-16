from random import *

import pymunk
from pymunk.vec2d import Vec2d

from enum import *

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
    def __init__(self):
        hash = int(random() * 1000000)
        self.__hash = hash - hash % 10
    
    def start(self, instigator):
        return
    
    
    def uniq(self, i):
        return self.__hash + i
        
# --------------------------------------------------------

class TestVNAttack(Attack):
    def start(self, instigator):
        offset = Vec2d(30, 0) * instigator.direction
        for i in range(3):
            instigator.scene.hitbox(self.uniq(0), instigator.position + offset, 15, Damage(DamageType.NORMAL, 4, offset * 8), instigator)
            yield
        for i in range(3):
            yield
            
class TestVDAttack(Attack):
    def start(self, instigator):
        dir = Vec2d(instigator.direction, -1)
        for i in range(3):
            instigator.scene.hitbox(self.uniq(0), instigator.position + Vec2d(35, 10) * dir, 20, Damage(DamageType.NORMAL, 4, Vec2d(5, -40) * dir * 10), instigator)
            yield
        for i in range(3):
            yield
            
class TestVFAttack(Attack):
    def start(self, instigator):
        offset = Vec2d(30, 0) * (instigator.direction, 1)
        for i in range(4):
            if i % 2 == 0:
                instigator.scene.hitbox(self.uniq(0), instigator.position + offset, 15, Damage(DamageType.NORMAL, 3, offset * 10), instigator)
            else:
                instigator.scene.hitbox(self.uniq(1), instigator.position + offset * 2, 25, Damage(DamageType.NORMAL, 7, offset * 20), instigator)
            yield
        for i in range(3):
            yield

class TestAttack(Attack):
    def start(self, instigator):
        for i in range(10):
            offset = Vec2d(30 + 3 * i, 0) * instigator.direction + Vec2d(0, -15 + 5 * i)
            knockback = Vec2d(100 + 25 * i, 0) * instigator.direction + Vec2d(0, 100 + 50  * i)
            instigator.scene.hitbox(self.uniq(i), instigator.position + offset, 8 + i, Damage(DamageType.NORMAL, 2, knockback), instigator)
            yield
        for i in range(10):
            yield
            
class TestCDAttack(Attack):
    def start(self, instigator):
        scene = instigator.scene
        dir = Vec2d(instigator.direction, -1)
        
        instigator.moveStyle = MoveStyle.ANIM_DRIVEN
        instigator.velocity = Vec2d(-400, 200) * Vec2d(instigator.direction, 1)
        for i in range(10):
            scene.hitbox(self.uniq(0), instigator.position + Vec2d(40, -10) * dir, 25, Damage(DamageType.NORMAL, 5 + i / 2, Vec2d(5.2 * i, -5.2 * (10 - i)) * dir * 10), instigator)
            yield
            
        for i in range(5):
            yield
        
        instigator.moveStyle = MoveStyle.PHYSICS_DRIVEN
        instigator.helpless = True
        
        for i in range(15):
            yield

class TestCUAttack(Attack):
    def start(self, instigator):
        scene = instigator.scene
        dir = Vec2d(instigator.direction, -1)
        
        instigator.moveStyle = MoveStyle.ANIM_DRIVEN
        instigator.velocity = Vec2d(100, 450) * Vec2d(instigator.direction, 1)
        for i in range(10):
            scene.hitbox(self.uniq(0), instigator.position + Vec2d(30, -20) * dir, 20, Damage(DamageType.NORMAL, 12 - i / 2, Vec2d(32, -50) * dir * 10), instigator)
            yield
            
        instigator.moveStyle = MoveStyle.PHYSICS_DRIVEN
        instigator.helpless = True

class TestCNAttack(Attack):
    def start(self, instigator):
        dir = Vec2d(instigator.direction, -1)
        
        instigator.moveStyle = MoveStyle.ANIM_DRIVEN
        instigator.velocity = Vec2d(0, 250) * Vec2d(instigator.direction, 1)
        for i in range(10):
            yield
        instigator.scene.hitbox(self.uniq(0), instigator.position + Vec2d(35, 28) * dir, 25, Damage(DamageType.NORMAL, 3, Vec2d(-50, 0) * dir * 10), instigator)
        for i in range(15):
            yield
        instigator.moveStyle = MoveStyle.PHYSICS_DRIVEN