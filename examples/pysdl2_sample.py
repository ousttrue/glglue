# coding: utf-8
'''
# sdl2
require pyOpenGL + pysdl2 + sdl2.dll

# sdl2 install on Windows

* なんとかしてSDL2.dllを入手(vcpkgでビルドするなど) 
* 環境変数PYSDL2_DLL_PATHを設定する
'''
import pathlib
import sys
import logging
from OpenGL.GL import *
HERE = pathlib.Path(__file__).absolute().parent
sys.path.insert(0, str(HERE.parent / 'src'))
logger = logging.getLogger(__name__)


class Controller:
    """
    [CLASSES] Controllerクラスは、glglueの規約に沿って以下のコールバックを実装する
    """
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
        glVertex(-1.0, -1.0)
        glVertex(1.0, -1.0)
        glVertex(0.0, 1.0)
        glEnd()

        glFlush()


if __name__ == "__main__":
    logging.basicConfig(format='%(levelname)s:%(name)s:%(message)s',
                        level=logging.DEBUG)
    # sdl2.dllにパスが通っていない場合は、
    # import する前に環境変数'PYSDL2_DLL_PATH'を設定する
    import glglue.pysdl2
    controller = Controller()
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
