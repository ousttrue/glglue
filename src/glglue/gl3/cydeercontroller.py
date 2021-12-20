import ctypes
import logging
#
from OpenGL import GL
import cydeer as ImGui
from glglue.basecontroller import BaseController
from .cameraview import CameraView
logger = logging.getLogger(__name__)


class CydeerController(BaseController):
    """
    [CLASSES] Controllerクラスは、glglueの規約に沿って以下のコールバックを実装する
    """

    def __init__(self, scale: float = 1):
        #
        # imgui
        #
        ImGui.CreateContext()
        self.io = ImGui.GetIO()
        self.io.ConfigFlags |= ImGui.ImGuiConfigFlags_.DockingEnable

        self.load_font()

        self.io.DisplayFramebufferScale = ImGui.ImVec2(scale, scale)
        from cydeer.backends.opengl import Renderer
        self.impl_gl = Renderer()
        self.viewport = (1, 1)

        #
        # 3D View
        #
        self.view = CameraView()

        #
        # dock
        #
        from cydeer.utils.dockspace import DockView
        self.metrics_view = DockView(
            'metrics', (ctypes.c_bool * 1)(True), ImGui.ShowMetricsWindow)

        def show_hello(p_open: ctypes.Array):
            # open new window context
            ImGui.Begin("CustomGUI")
            # draw text label inside of current window
            ImGui.Text("cydeer !")
            # close current window context
            ImGui.End()
        self.hello_view = DockView(
            'hello', (ctypes.c_bool * 1)(True), show_hello)

        self.scene_view = DockView(
            '3d', (ctypes.c_bool * 1)(True), self.view.draw)

    def load_font(self):
        # create texture before: ImGui.NewFrame()
        self.io.Fonts.GetTexDataAsRGBA32(
            (ctypes.c_void_p * 1)(),
            (ctypes.c_int * 1)(), (ctypes.c_int * 1)())

    def onResize(self, w, h):
        if self.viewport == (w, h):
            return False
        self.viewport = (w, h)
        return True

    def onLeftDown(self, x, y):
        self.io.MouseDown[0] = 1
        return False

    def onLeftUp(self, x, y):
        self.io.MouseDown[0] = 0
        return False

    def onMiddleDown(self, x, y):
        self.io.MouseDown[2] = 1
        return False

    def onMiddleUp(self, x, y):
        self.io.MouseDown[2] = 0
        return False

    def onRightDown(self, x, y):
        self.io.MouseDown[1] = 1
        return False

    def onRightUp(self, x, y):
        self.io.MouseDown[1] = 0
        return False

    def onMotion(self, x, y):
        self.io.MousePos = ImGui.ImVec2(x, y)
        return False

    def onWheel(self, d):
        self.io.MouseWheel = d
        return False

    def onKeyDown(self, keycode):
        logger.debug('onKeyDown: %d', keycode)

    def onUpdate(self, d):
        #logger.debug('onUpdate: delta %d ms', d)
        self.io.DeltaTime = d * 0.001
        return True

    def draw_imgui(self):
        from cydeer.utils.dockspace import dockspace
        dockspace(self.metrics_view, self.hello_view, self.scene_view)

    def draw(self):
        # state = self.camera.get_state()

        #
        # new frame
        #
        self.io.DisplaySize = ImGui.ImVec2(*self.viewport)
        ImGui.NewFrame()

        #
        # imgui
        #
        self.draw_imgui()
        ImGui.EndFrame()
        ImGui.Render()

        #
        # clear frame buffer
        #
        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, 0)
        GL.glViewport(0, 0, *self.viewport)
        GL.glClearColor(0.0, 0.0, 1.0, 0.0)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT |
                   GL.GL_DEPTH_BUFFER_BIT)  # type: ignore

        #
        # render
        #
        # pass all drawing comands to the rendering pipeline
        # and close frame context
        self.impl_gl.render(ImGui.GetDrawData())

        GL.glFlush()
