import math
from logging import getLogger
from OpenGL.GL import (glClear, glFlush, glEnable, glClearColor, glViewport,
                       GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT, GL_DEPTH_TEST)
import glglue
from .cube import Cube
from .axis import Axis
logger = getLogger(__name__)


class SampleController:
    def __init__(self):
        self.clear_color = (0.6, 0.6, 0.4, 0.0)
        self.axis = Axis(1.0)
        self.cube = Cube(0.3)
        self.camera = glglue.ctypesmath.Camera()
        self.isInitialized = False

    def onResize(self, w: int, h: int) -> None:
        glViewport(0, 0, w, h)
        self.camera.onResize(w, h)

    def onLeftDown(self, x: int, y: int) -> None:
        ''' mouse input '''
        self.camera.onLeftDown(x, y)

    def onLeftUp(self, x: int, y: int) -> None:
        ''' mouse input '''
        self.camera.onLeftUp(x, y)

    def onMiddleDown(self, x: int, y: int) -> None:
        ''' mouse input '''
        self.camera.onMiddleDown(x, y)

    def onMiddleUp(self, x: int, y: int) -> None:
        ''' mouse input '''
        self.camera.onMiddleUp(x, y)

    def onRightDown(self, x: int, y: int) -> None:
        ''' mouse input '''
        self.camera.onRightDown(x, y)

    def onRightUp(self, x: int, y: int) -> None:
        ''' mouse input '''
        self.camera.onRightUp(x, y)

    def onMotion(self, x: int, y: int) -> None:
        ''' mouse input '''
        self.camera.onMotion(x, y)

    def onWheel(self, d: int) -> None:
        ''' mouse input '''
        self.camera.onWheel(d)

    def onKeyDown(self, keycode: int) -> None:
        pass

    def onUpdate(self, d: int) -> None:
        '''
        milliseconds
        '''
        self.cube.update(d)

    def initialize(self):
        glEnable(GL_DEPTH_TEST)
        self.isInitialized = True

    def draw(self):
        if not self.isInitialized:
            self.initialize()
        glClearColor(*self.clear_color)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        self.axis.draw(self.camera.projection.matrix, self.camera.view.matrix)
        self.cube.draw(self.camera.projection.matrix, self.camera.view.matrix)

        glFlush()
