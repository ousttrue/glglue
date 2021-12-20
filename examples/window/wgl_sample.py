# coding: utf-8
'''
Win32APIでOpenGLホストするサンプル。

* Windows専用
* 追加のインストールは不要
'''
from logging import getLogger

logger = getLogger(__name__)

from logging import basicConfig, DEBUG

basicConfig(format='%(levelname)s:%(name)s:%(message)s', level=DEBUG)

from OpenGL.GL import *  # pylint: disable=W0614, W0622, W0401


class Controller:
    """
    [CLASSES] Controllerクラスは、glglueの規約に沿って以下のコールバックを実装する
    """
    def __init__(self) -> None:
        self.is_initialized = False

    def onResize(self, w: int, h: int) -> None:
        logger.debug('onResize: %d, %d', w, h)
        glViewport(0, 0, w, h)

    def onLeftDown(self, x: int, y: int) -> None:
        logger.debug('onLeftDown: %d, %d', x, y)

    def onLeftUp(self, x: int, y: int) -> None:
        logger.debug('onLeftUp: %d, %d', x, y)

    def onMiddleDown(self, x: int, y: int) -> None:
        logger.debug('onMiddleDown: %d, %d', x, y)

    def onMiddleUp(self, x: int, y: int) -> None:
        logger.debug('onMiddleUp: %d, %d', x, y)

    def onRightDown(self, x: int, y: int) -> None:
        logger.debug('onRightDown: %d, %d', x, y)

    def onRightUp(self, x: int, y: int) -> None:
        logger.debug('onRightUp: %d, %d', x, y)

    def onMotion(self, x: int, y: int) -> None:
        logger.debug('onMotion: %d, %d', x, y)

    def onWheel(self, d: int) -> None:
        logger.debug('onWheel: %d', d)

    def onKeyDown(self, keycode: int) -> None:
        logger.debug('onKeyDown: %d', keycode)

    def onUpdate(self, d: int) -> None:
        '''
        milliseconds
        '''
        #logger.debug('onUpdate: delta %d ms', d)
        pass

    def initialize(self) -> None:
        self.is_initialized = True

    def draw(self) -> None:
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
    controller = Controller()
    import glglue.wgl
    loop = glglue.wgl.LoopManager(controller,
                                  width=640,
                                  height=480,
                                  title=b"sample")
    
    lastCount = 0
    while True:
        count = loop.begin_frame()
        if not count:
            break
        d = count - lastCount
        lastCount = count
        if d > 0:
            controller.onUpdate(d)
            controller.draw()
            loop.end_frame()
