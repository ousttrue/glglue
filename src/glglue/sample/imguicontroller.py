from OpenGL import GL
from glglue.ctypesmath.camera import Camera
import imgui.integrations.opengl
import imgui
from glglue.basecontroller import BaseController
from logging import getLogger
from ..gl3.samplecontroller import Scene, BaseScene

logger = getLogger(__name__)


class ImGuiController(BaseController):
    """
    [CLASSES] Controllerクラスは、glglueの規約に沿って以下のコールバックを実装する
    """

    def __init__(self, scale=1):
        self.is_init = False
        imgui.create_context()
        self.io = imgui.get_io()
        self.io.fonts.get_tex_data_as_rgba32()
        self.io.display_fb_scale = scale, scale
        self.viewport = (1, 1)
        self.camera = Camera()
        self.scene: BaseScene = Scene()

    def onResize(self, w, h):
        if self.viewport == (w, h):
            return False
        self.camera.onResize(w, h)
        self.viewport = (w, h)
        return True

    def onLeftDown(self, x, y):
        self.io.mouse_down[0] = 1
        if not self.io.want_capture_mouse:
            self.camera.onLeftDown(x, y)

        return False

    def onLeftUp(self, x, y):
        self.io.mouse_down[0] = 0
        if not self.io.want_capture_mouse:
            self.camera.onLeftUp(x, y)

        return False

    def onMiddleDown(self, x, y):
        self.io.mouse_down[2] = 1
        if not self.io.want_capture_mouse:
            self.camera.onMiddleDown(x, y)

        return False

    def onMiddleUp(self, x, y):
        self.io.mouse_down[2] = 0
        if not self.io.want_capture_mouse:
            self.camera.onMiddleUp(x, y)

        return False

    def onRightDown(self, x, y):
        self.io.mouse_down[1] = 1
        if not self.io.want_capture_mouse:
            self.camera.onRightDown(x, y)

        return False

    def onRightUp(self, x, y):
        self.io.mouse_down[1] = 0
        if not self.io.want_capture_mouse:
            self.camera.onRightUp(x, y)

        return False

    def onMotion(self, x, y):
        self.io.mouse_pos = x, y
        if not self.io.want_capture_mouse:
            self.camera.onMotion(x, y)

        return False

    def onWheel(self, d):
        self.io.mouse_wheel = d
        if not self.io.want_capture_mouse:
            self.camera.onWheel(d)

        return False

    def onKeyDown(self, keycode):
        logger.debug('onKeyDown: %d', keycode)

    def onUpdate(self, d):
        #logger.debug('onUpdate: delta %d ms', d)
        self.io.delta_time = d * 0.001
        return True

    def on_imgui(self):
        # open new window context
        imgui.begin("Your first window!", True)
        # draw text label inside of current window
        imgui.text("Hello world!")
        # close current window context
        imgui.end()

    def draw(self):
        if not self.is_init:
            # initilize imgui context (see documentation)
            self.imgui_impl = imgui.integrations.opengl.ProgrammablePipelineRenderer(
            )
            self.is_init = True

        state = self.camera.get_state()

        #
        # imgui
        #
        self.io.display_size = self.viewport

        # start new frame context
        imgui.new_frame()

        self.on_imgui()

        imgui.end_frame()

        #
        # render
        #
        GL.glViewport(0, 0, *self.viewport)

        GL.glClearColor(0.0, 0.0, 1.0, 0.0)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT |
                   GL.GL_DEPTH_BUFFER_BIT)  # type: ignore
        if self.scene:
            self.scene.draw(state)

        # pass all drawing comands to the rendering pipeline
        # and close frame context
        imgui.render()
        self.imgui_impl.render(imgui.get_draw_data())

        GL.glFlush()
