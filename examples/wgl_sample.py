# coding: utf-8
'''
Win32APIでOpenGLホストするサンプル
'''
from logging import getLogger
logger = getLogger(__name__)

from OpenGL.GL import *  # pylint: disable=W0614, W0622, W0401


class Controller:
    """
    [CLASSES] Controllerクラスは、glglueの規約に沿って以下のコールバックを実装する
    """

    def __init__(self):
        self.is_initialized = False

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

    def initialize(self):
        self.is_initialized = True

    def draw(self):
        if not self.is_initialized:
            self.initialize()
        glClearColor(0.0, 0.0, 1.0, 0.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glBegin(GL_TRIANGLES)
        glVertex(-1.0, -1.0)
        glVertex(1.0, -1.0)
        glVertex(0.0, 1.0)
        glEnd()

        glFlush()


if __name__ == "__main__":
    from logging import basicConfig, DEBUG
    basicConfig(
        format='%(levelname)s:%(name)s:%(message)s', level=DEBUG
    )
    controller = Controller()
    import pathlib
    import sys
    sys.path.append(str(pathlib.Path(__file__).parents[1]))
    import glglue.wgl
    glglue.wgl.mainloop(controller, width=640, height=480, title=b"sample")
