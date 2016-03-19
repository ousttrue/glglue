# coding: utf-8
from OpenGL.GL import *


class Controller(object):
    def __init__(self):
        pass

    def onResize(self, w, h):
        glViewport(0, 0, w, h)

    def onLeftDown(self, x, y):
        print('onLeftDown', x, y)

    def onLeftUp(self, x, y):
        print('onLeftUp', x, y)

    def onMiddleDown(self, x, y):
        print('onMiddleDown', x, y)

    def onMiddleUp(self, x, y):
        print('onMiddleUp', x, y)

    def onRightDown(self, x, y):
        print('onRightDown', x, y)

    def onRightUp(self, x, y):
        print('onRightUp', x, y)

    def onMotion(self, x, y):
        print('onMotion', x, y)

    def onWheel(self, d):
        print('onWheel', d)

    def onKeyDown(self, keycode):
        print('onKeyDown', keycode)

    def onUpdate(self, d):
        print('onUpdate', d)

    def draw(self):
        glClearColor(0.9, 0.5, 0.0, 0.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glBegin(GL_TRIANGLES)
        glVertex(-1.0,-1.0)
        glVertex( 1.0,-1.0)
        glVertex( 0.0, 1.0)
        glEnd()

        glFlush()


if __name__=="__main__":
    controller=Controller()
    import glglue.glut
    glglue.glut.mainloop(controller, width=640, height=480, title=b"sample")    
    #import glglue.wgl
    #glglue.wgl.mainloop(controller, width=640, height=480, title=b"sample")

