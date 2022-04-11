# coding: utf-8
'''
# sdl2
require pyOpenGL + pysdl2 + sdl2.dll

# sdl2 install on Windows
* pip install pysdl2 pysdl2-dll
'''
from OpenGL import GL
import logging

LOGGER = logging.getLogger(__name__)
logging.basicConfig(format='%(levelname)s:%(name)s:%(message)s',
                    level=logging.DEBUG)


class Controller:
    """
    [CLASSES] Controllerクラスは、glglueの規約に沿って以下のコールバックを実装する
    """

    def __init__(self):
        pass

    def onResize(self, w, h):
        LOGGER.debug('onResize: %d, %d', w, h)
        GL.glViewport(0, 0, w, h)

    def onLeftDown(self, x, y):
        LOGGER.debug('onLeftDown: %d, %d', x, y)

    def onLeftUp(self, x, y):
        LOGGER.debug('onLeftUp: %d, %d', x, y)

    def onMiddleDown(self, x, y):
        LOGGER.debug('onMiddleDown: %d, %d', x, y)

    def onMiddleUp(self, x, y):
        LOGGER.debug('onMiddleUp: %d, %d', x, y)

    def onRightDown(self, x, y):
        LOGGER.debug('onRightDown: %d, %d', x, y)

    def onRightUp(self, x, y):
        LOGGER.debug('onRightUp: %d, %d', x, y)

    def onMotion(self, x, y):
        LOGGER.debug('onMotion: %d, %d', x, y)

    def onWheel(self, d):
        LOGGER.debug('onWheel: %d', d)

    def onKeyDown(self, keycode):
        LOGGER.debug('onKeyDown: %d', keycode)

    def onUpdate(self, d):
        #logger.debug('onUpdate: delta %d ms', d)
        pass

    def draw(self):
        GL.glClearColor(0.0, 0.0, 1.0, 0.0)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

        GL.glBegin(GL.GL_TRIANGLES)
        GL.glVertex(-1.0, -1.0)
        GL.glVertex(1.0, -1.0)
        GL.glVertex(0.0, 1.0)
        GL.glEnd()

        GL.glFlush()


def main():
    controller = Controller()

    import glglue.pysdl2
    loop = glglue.pysdl2.LoopManager(controller)
    lastTime = 0
    while True:
        time = loop.begin_frame()
        if not time:
            break
        if lastTime == 0:
            lastTime = time
            continue
        d = time - lastTime
        lastTime = time
        if d:
            controller.onUpdate(d)
            controller.draw()
            loop.end_frame()


if __name__ == "__main__":
    main()
