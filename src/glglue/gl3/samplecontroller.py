from logging import getLogger
from typing import Any, List
from OpenGL import GL
from . import gizmo
import glglue.basecontroller
from glglue import ctypesmath
import glglue.gl3.vbo
import glglue.scene.material
from ..scene import cube
from . renderer import Renderer
logger = getLogger(__name__)


class Scene:
    def __init__(self) -> None:
        self.env: List[Any] = []
        self.drawables: List[Any] = [cube.create_cube(0.3)]
        self.renderer = Renderer()
        self.gizmo = gizmo.Gizmo()

    def update(self, d: int):
        for drawable in self.drawables:
            drawable.update(d)

    def draw(self, camera: ctypesmath.Camera):
        self.gizmo.begin(camera.view.matrix, camera.projection.matrix)

        for e in self.env:
            self.renderer.draw(
                e, camera.projection.matrix, camera.view.matrix)
        for i, drawable in enumerate(self.drawables):
            self.renderer.draw(
                drawable,
                camera.projection.matrix,
                camera.view.matrix)
            # aabb
            aabb = ctypesmath.AABB.new_empty()
            self.gizmo.aabb(drawable.expand_aabb(aabb))

        self.gizmo.end()


class SampleController(glglue.basecontroller.BaseController):
    def __init__(self):
        self.clear_color = (0.6, 0.6, 0.4, 0.0)
        self.camera = ctypesmath.Camera()
        self.gizmo = gizmo.Gizmo()
        self.scene = Scene()
        self.isInitialized = False

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
        if self.scene:
            self.scene.update(d)
        return False

    def initialize(self):
        import glglue
        logger.info(glglue.get_info())
        GL.glEnable(GL.GL_DEPTH_TEST)
        self.isInitialized = True

    def draw(self):
        if not self.isInitialized:
            self.initialize()
        GL.glClearColor(*self.clear_color)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT |
                   GL.GL_DEPTH_BUFFER_BIT)  # type: ignore
        if self.scene:
            self.scene.draw(self.camera)

        self.gizmo.begin(self.camera.view.matrix,
                         self.camera.projection.matrix)
        self.gizmo.axis(10)
        self.gizmo.end()
        GL.glFlush()
