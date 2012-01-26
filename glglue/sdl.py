import pygame
from pygame.locals import *
import glglue.sample


if __name__=="__main__":   
    pygame.init()
    size=(640, 480)
    pygame.display.gl_set_attribute(pygame.GL_STENCIL_SIZE, 2)
    screen = pygame.display.set_mode(size, 
            HWSURFACE | OPENGL | DOUBLEBUF)

    controller=glglue.sample.SampleController()
    controller.onResize(*size)

    clock = pygame.time.Clock()    
    is_running=True
    while is_running:
        #pressed = pygame.key.get_pressed()

        # event handling
        for event in pygame.event.get():
            if event.type == QUIT:
                is_running=False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    is_running=False
                else:
                    controller.onKeyDown(event.key)
            
        # update
        d = clock.tick()
        if d>0:
            controller.onUpdate(d)
            controller.draw()
            pygame.display.flip()

