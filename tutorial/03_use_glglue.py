# coding: utf-8
from OpenGL.GL import *
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(
        format='%(levelname)s:%(name)s:%(message)s'
        , level=logging.DEBUG
        )

'''
02のsimple_rendererをglglueのController規約に沿って記述した。

    glglue.glut.mainloop(controller)

の部分を

    glglue.wgl.mainloop(controller)

等に差し替えることでGUIとOpenGLの依存を断ち切って、
複数のGUIに対して同じOpenGLコードを動作させることができる。
'''

class Controller(object):
    def __init__(self):
        pass

    def onResize(self, w, h):
        logger.debug('onResize: %d, %d', w, h)
        glViewport(0, 0, w, h)

    def onLeftDown(self, x, y):
        logger.debug('onLeftDown: %d, %d', x, y)

    def onLeftUp(self, x, y):
        logger.debug('onLeftUp: %d, %d', x, y)

    def onMiddleDown(self, x, y):
        logger.debug('onMiddleDown: %d, %d', x, y)

    def onMiddleUp(self, x, y):
        logger.debug('onMiddleUp: %d, %d', x, y)

    def onRightDown(self, x, y):
        logger.debug('onRightDown: %d, %d', x, y)

    def onRightUp(self, x, y):
        logger.debug('onRightUp: %d, %d', x, y)

    def onMotion(self, x, y):
        logger.debug('onMotion: %d, %d', x, y)

    def onWheel(self, d):
        logger.debug('onWheel: %d', d)

    def onKeyDown(self, keycode):
        logger.debug('onKeyDown: %d', keycode)

    def onUpdate(self, d):
        #logger.debug('onUpdate: delta %d ms', d)
        pass

    def draw(self):
        glClearColor(0.0, 0.0, 1.0, 0.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glBegin(GL_TRIANGLES)
        glVertex(-1.0,-1.0)
        glVertex( 1.0,-1.0)
        glVertex( 0.0, 1.0)
        glEnd()

        glFlush()


if __name__=="__main__":
    import pathlib
    import sys
    sys.path.append(str(pathlib.Path(__file__).parents[1]))
    import glglue.glut
    controller=Controller()
    glglue.glut.mainloop(controller)
