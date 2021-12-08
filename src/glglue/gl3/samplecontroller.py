from abc import ABCMeta, abstractmethod
from logging import getLogger
from typing import Any, List
from OpenGL import GL
from . import gizmo
import glglue.basecontroller
from glglue.ctypesmath import Camera, FrameState, AABB, Float4
import glglue.gl3.vbo
import glglue.scene.material
from ..scene import cube
from . renderer import Renderer
logger = getLogger(__name__)


class BaseScene(metaclass=ABCMeta):
    def __init__(self):
        pass

    @abstractmethod
    def update(self, d: int) -> bool:
        return False

    @abstractmethod
    def draw(self, state: FrameState):
        pass


class Scene(BaseScene):
    def __init__(self) -> None:
        self.env: List[Any] = []
        self.drawables: List[Any] = [cube.create_cube(0.3)]
        self.renderer = Renderer()
        self.gizmo = gizmo.Gizmo()

    def update(self, d: int) -> bool:
        updated = False
        for drawable in self.drawables:
            if drawable.update(d):
                updated = True
        return updated

    def draw(self, state: FrameState):
        self.gizmo.begin(state)
        self.gizmo.axis(10)

        for e in self.env:
            self.renderer.draw(e, state)
        for _, drawable in enumerate(self.drawables):
            self.renderer.draw(drawable, state)
            # aabb
            aabb = AABB.new_empty()
            self.gizmo.aabb(drawable.expand_aabb(aabb))

        self.gizmo.end()


class SampleController(glglue.basecontroller.BaseController):
    def __init__(self):
        self.clear_color = (0.6, 0.6, 0.4, 0.0)
        self.camera = Camera()
        self.scene: BaseScene = Scene()
        self.isInitialized = False

    def onResize(self, w: int, h: int) -> bool:
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
        if not self.scene:
            return False
        return self.scene.update(d)

    def initialize(self):
        import glglue
        logger.info(glglue.get_info())
        self.isInitialized = True

    def draw(self):
        if not self.isInitialized:
            self.initialize()
        GL.glClearColor(*self.clear_color)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT |
                   GL.GL_DEPTH_BUFFER_BIT)  # type: ignore

        state = self.camera.get_state()
        GL.glViewport(int(state.viewport.x), int(state.viewport.y),
                      int(state.viewport.z), int(state.viewport.w))

        if self.scene:
            self.scene.draw(state)

        GL.glFlush()
