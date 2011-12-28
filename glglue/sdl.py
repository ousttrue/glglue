import pygame
from pygame.locals import *
import glglue.sample


if __name__=="__main__":   
    pygame.init()
    size=(640, 480)
    screen = pygame.display.set_mode(size, 
            HWSURFACE | OPENGL | DOUBLEBUF)

    controller=glglue.sample.SampleController()
    controller.onResize(*size)

    clock = pygame.time.Clock()    
    is_running=True
    while is_running:
        # event handling
        for event in pygame.event.get():
            if event.type == QUIT:
                is_running=False
            if event.type == KEYUP and event.key == K_ESCAPE:
                is_running=False
        pressed = pygame.key.get_pressed()
            
        time_passed = clock.tick()
        
        # Show the screen
        controller.draw()
        pygame.display.flip()
