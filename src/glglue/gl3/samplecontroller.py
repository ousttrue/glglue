from logging import getLogger
from typing import Any, List, NamedTuple
from OpenGL import GL
import glglue.basecontroller
import glglue.ctypesmath
import glglue.gl3.vbo
import glglue.scene.material
from ..scene import cube, axis
from . renderer import Renderer
logger = getLogger(__name__)


class SampleController(glglue.basecontroller.BaseController):
    def __init__(self):
        self.clear_color = (0.6, 0.6, 0.4, 0.0)
        self.env: List[Any] = [axis.create_axis(1.0)]
        self.drawables: List[Any] = [cube.create_cube(0.3)]
        self.camera = glglue.ctypesmath.Camera()
        self.isInitialized = False
        self.renderer = Renderer()

    def onResize(self, w: int, h: int) -> bool:
        GL.glViewport(0, 0, w, h)
        return self.camera.onResize(w, h)

    def onLeftDown(self, x: int, y: int) -> bool:
        ''' mouse input '''
        return self.camera.onLeftDown(x, y)

    def onLeftUp(self, x: int, y: int) -> bool:
        ''' mouse input '''
        return self.camera.onLeftUp(x, y)

    def onMiddleDown(self, x: int, y: int) -> bool:
        ''' mouse input '''
        return self.camera.onMiddleDown(x, y)

    def onMiddleUp(self, x: int, y: int) -> bool:
        ''' mouse input '''
        return self.camera.onMiddleUp(x, y)

    def onRightDown(self, x: int, y: int) -> bool:
        ''' mouse input '''
        return self.camera.onRightDown(x, y)

    def onRightUp(self, x: int, y: int) -> bool:
        ''' mouse input '''
        return self.camera.onRightUp(x, y)

    def onMotion(self, x: int, y: int) -> bool:
        ''' mouse input '''
        return self.camera.onMotion(x, y)

    def onWheel(self, d: int) -> bool:
        ''' mouse input '''
        return self.camera.onWheel(d)

    def onKeyDown(self, keycode: int) -> bool:
        return False

    def onUpdate(self, d: int) -> bool:
        '''
        milliseconds
        '''
        for drawable in self.drawables:
            drawable.update(d)
        return False

    def initialize(self):
        import glglue
        print(glglue.get_info())
        GL.glEnable(GL.GL_DEPTH_TEST)
        self.isInitialized = True

    def draw(self):
        if not self.isInitialized:
            self.initialize()
        GL.glClearColor(*self.clear_color)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT |
                   GL.GL_DEPTH_BUFFER_BIT)  # type: ignore

        for e in self.env:
            self.renderer.draw(
                e, self.camera.projection.matrix, self.camera.view.matrix)
        for drawable in self.drawables:
            self.renderer.draw(drawable, self.camera.projection.matrix,
                               self.camera.view.matrix)

        GL.glFlush()
