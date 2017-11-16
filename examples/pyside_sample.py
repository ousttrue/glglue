'''
# pyside install on Windows

* https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyside
'''
from logging import getLogger
logger = getLogger(__name__)

import pathlib
import sys
sys.path.append(str(pathlib.Path(__file__).parents[1]))
import glglue.pysidegl
from PySide import QtGui as Qt
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
        glVertex(-1.0,-1.0)
        glVertex( 1.0,-1.0)
        glVertex( 0.0, 1.0)
        glEnd()

        glFlush()


class Window(Qt.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        # setup opengl widget
        self.controller=Controller()
        self.glwidget=glglue.pysidegl.Widget(self, self.controller)
        self.setCentralWidget(self.glwidget)


if __name__=="__main__":
    from logging import basicConfig, DEBUG
    basicConfig(
        format='%(levelname)s:%(name)s:%(message)s', level=DEBUG
    )    
    app = Qt.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
