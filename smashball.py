__version__ = "$Id:$"
__docformat__ = "reStructuredText"

import sys,math

sys.dont_write_bytecode = 1

import pygame
from pygame.locals import *
from pygame.color import *
    
import pymunk
from pymunk.vec2d import Vec2d
from pymunk.pygame_util import draw_space, from_pygame, to_pygame

from scene import *
from entities import *
from actor import *
from damage import *

# --------------------------------------------------------

width, height = 690,400
fps = 60
dt = 1./fps

# --------------------------------------------------------

def main():
    ### PyGame init
    pygame.init()
    screen = pygame.display.set_mode((width,height)) 

    clock = pygame.time.Clock()
    running = True
    font = pygame.font.SysFont("Arial", 16)

    ### Physics stuff
    space = pymunk.Space()   
    space.gravity = 0,-1000
    # box walls 
    static = [pymunk.Segment(space.static_body, (10, 50), (330, 50), 5)
                , pymunk.Segment(space.static_body, (330, 50), (350, 50), 5)
                , pymunk.Segment(space.static_body, (350, 50), (680, 50), 5)
                , pymunk.Segment(space.static_body, (680, 50), (680, 370), 5)
                , pymunk.Segment(space.static_body, (680, 370), (10, 370), 5)
                , pymunk.Segment(space.static_body, (10, 370), (10, 50), 5)
                ]  
    static[1].color = pygame.color.THECOLORS['red']
    
    for s in static:
        s.friction = 1.
        s.group = 1
        s.elasticity = 0.9
        
    space.add(static)
    space.elasticIterations = 10

    scene = SceneGraph(screen, space)
   
    body = Actor()
    body.position = 100,100
    
    ball = Ball()
    ball.position = 200,200

    scene.register(ball)
    scene.register(body)
    
   
    while running:
        screen.fill(pygame.color.THECOLORS["black"])
        
        for event in pygame.event.get():
            if event.type == QUIT or \
                event.type == KEYDOWN and (event.key in [K_ESCAPE, K_q]):  
                running = False
            else:
                body.controller.onEvent(event)
                
        scene.update(dt)
        
        scene.draw(screen)
        screen.blit(font.render("fps: " + str(clock.get_fps()), 1, THECOLORS["white"]), (0,0))
        pygame.display.flip()
        
        space.step(dt)
        clock.tick(fps)


if __name__ == '__main__':
    sys.exit(main())
