# coding: utf-8
'''
Win32APIでOpenGLホストするサンプル。

* Windows専用
* 追加のインストールは不要
'''
from OpenGL import GL
import logging
import glglue.basecontroller

LOGGER = logging.getLogger(__name__)


class Controller(glglue.basecontroller.BaseController):
    """
    [CLASSES] Controllerクラスは、glglueの規約に沿って以下のコールバックを実装する
    """

    def __init__(self) -> None:
        self.is_initialized = False

    def onResize(self, w: int, h: int) -> None:
        LOGGER.debug('onResize: %d, %d', w, h)
        GL.glViewport(0, 0, w, h)

    def onLeftDown(self, x: int, y: int) -> None:
        LOGGER.debug('onLeftDown: %d, %d', x, y)

    def onLeftUp(self, x: int, y: int) -> None:
        LOGGER.debug('onLeftUp: %d, %d', x, y)

    def onMiddleDown(self, x: int, y: int) -> None:
        LOGGER.debug('onMiddleDown: %d, %d', x, y)

    def onMiddleUp(self, x: int, y: int) -> None:
        LOGGER.debug('onMiddleUp: %d, %d', x, y)

    def onRightDown(self, x: int, y: int) -> None:
        LOGGER.debug('onRightDown: %d, %d', x, y)

    def onRightUp(self, x: int, y: int) -> None:
        LOGGER.debug('onRightUp: %d, %d', x, y)

    def onMotion(self, x: int, y: int) -> None:
        LOGGER.debug('onMotion: %d, %d', x, y)

    def onWheel(self, d: int) -> None:
        LOGGER.debug('onWheel: %d', d)

    def onKeyDown(self, keycode: int) -> None:
        LOGGER.debug('onKeyDown: %d', keycode)

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
        GL.glClearColor(0.0, 0.0, 1.0, 0.0)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

        GL.glBegin(GL.GL_TRIANGLES)
        GL.glVertex(-1.0, -1.0)
        GL.glVertex(1.0, -1.0)
        GL.glVertex(0.0, 1.0)
        GL.glEnd()

        GL.glFlush()


def main():
    logging.basicConfig(
        format='%(levelname)s:%(name)s:%(message)s', level=logging.DEBUG)

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


if __name__ == "__main__":
    main()
