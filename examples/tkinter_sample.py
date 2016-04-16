'''
tkinterのTOGLでOpenGLをホストするサンプル。

Windowsでは、すべての64bit版とPython3.2より後のバージョンの32bit版の
ビルド済みTOGLのdllが入手困難(誰もビルドして配布していない)。

glglue.toglも諦めてメンテナンスしないつもりである。
'''


import pathlib
import sys
sys.path.append(str(pathlib.Path(__file__).parents[1]))

import glglue.togl
import tkinter

from OpenGL.GL import *
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(
        format='%(levelname)s:%(name)s:%(message)s'
        , level=logging.DEBUG
        )


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
        glVertex(-1.0,-1.0)
        glVertex( 1.0,-1.0)
        glVertex( 0.0, 1.0)
        glEnd()

        glFlush()

class Frame(tkinter.Frame):
    def __init__(self, width, height, master=None, **kw):
        #super(Frame, self).__init__(master, **kw)
        tkinter.Frame.__init__(self, master, **kw)
        # setup opengl widget
        self.controller=Controller()
        self.glwidget=glglue.togl.Widget(
                self, self.controller, width=width, height=height)
        self.glwidget.pack(fill=tkinter.BOTH, expand=True)
        # event binding(require focus)
        self.bind('<Key>', self.onKeyDown)
        self.bind('<MouseWheel>', lambda e: self.controller.onWheel(-e.delta) and self.glwidget.onDraw())

    def onKeyDown(self, event):
        key=event.keycode
        if key==27:
            # Escape
            sys.exit()
        if key==81:
            # q
            sys.exit()
        else:
            logger.debug("keycode: %d", key)


if __name__=="__main__":
    f = Frame(width=600, height=600)
    f.pack(fill=tkinter.BOTH, expand=True)
    f.focus_set()
    f.mainloop()

