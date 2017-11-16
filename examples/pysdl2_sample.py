# coding: utf-8
'''
# sdl2
requrie pyOpenGL + pysdl2 + sdl2.dll

# sdl2 install on Windows

* なんとかしてSDL2.dllを入手(vcpkgでビルドするなど) 
* 環境変数PYSDL2_DLL_PATHを設定する
'''

from logging import getLogger
logger = getLogger(__name__)

import pathlib
import sys
import os
sys.path.append(str(pathlib.Path(__file__).parents[1]))
from OpenGL.GL import *



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
    from logging import basicConfig, DEBUG
    basicConfig(
        format='%(levelname)s:%(name)s:%(message)s', level=DEBUG
    )    
    # import する前に環境変数'PYSDL2_DLL_PATH'を設定するべし
    import glglue.pysdl2
    glglue.pysdl2.mainloop(Controller(), b'pysdl2 sample', 640, 480)
