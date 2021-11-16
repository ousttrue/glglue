from logging import getLogger

logger = getLogger(__name__)

from glglue.basecontroller import BaseController
import imgui
import imgui.integrations.opengl
from OpenGL import GL


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

    def onResize(self, w, h):
        if self.io.display_size == (w, h):
            return False
        self.io.display_size = w, h
        GL.glViewport(0, 0, w, h)
        return True

    def onLeftDown(self, x, y):
        self.io.mouse_down[0] = 1
        return False

    def onLeftUp(self, x, y):
        self.io.mouse_down[0] = 0
        return False

    def onMiddleDown(self, x, y):
        self.io.mouse_down[2] = 1
        return False

    def onMiddleUp(self, x, y):
        self.io.mouse_down[2] = 0
        return False

    def onRightDown(self, x, y):
        self.io.mouse_down[1] = 1
        return False

    def onRightUp(self, x, y):
        self.io.mouse_down[1] = 0
        return False

    def onMotion(self, x, y):
        self.io.mouse_pos = x, y
        return False

    def onWheel(self, d):
        self.io.mouse_wheel = d
        return False

    def onKeyDown(self, keycode):
        logger.debug('onKeyDown: %d', keycode)

    def onUpdate(self, d):
        #logger.debug('onUpdate: delta %d ms', d)
        self.io.delta_time = d * 0.001
        return True

    def draw(self):
        if not self.is_init:
            # initilize imgui context (see documentation)
            self.imgui_impl = imgui.integrations.opengl.ProgrammablePipelineRenderer(
            )
            self.is_init = True

        GL.glClearColor(0.0, 0.0, 1.0, 0.0)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

        GL.glBegin(GL.GL_TRIANGLES)
        GL.glVertex(-1.0, -1.0)
        GL.glVertex(1.0, -1.0)
        GL.glVertex(0.0, 1.0)
        GL.glEnd()

        # start new frame context
        imgui.new_frame()

        # open new window context
        imgui.begin("Your first window!", True)
        # draw text label inside of current window
        imgui.text("Hello world!")
        # close current window context
        imgui.end()

        imgui.end_frame()
        # pass all drawing comands to the rendering pipeline
        # and close frame context
        imgui.render()

        self.imgui_impl.render(imgui.get_draw_data())

        GL.glFlush()
