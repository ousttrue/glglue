from typing import List, Iterable
import ctypes
import logging
#
from OpenGL import GL
import pydear as ImGui
from pydear.utils.dockspace import DockView
from glglue.basecontroller import BaseController
from .renderview import RenderView
logger = logging.getLogger(__name__)


def create_docks() -> List[DockView]:
    views: List[DockView] = []

    views.append(DockView(
        'metrics', (ctypes.c_bool * 1)(True), ImGui.ShowMetricsWindow))

    def show_hello(p_open: ctypes.Array):
        # open new window context
        if ImGui.Begin("CustomGUI", p_open):
            # draw text label inside of current window
            if ImGui.Button("Debug"):
                logger.debug("debug message")
        # close current window context
        ImGui.End()
    views.append(DockView(
        'hello', (ctypes.c_bool * 1)(True), show_hello))

    #
    # 3D View
    #
    render_view = RenderView()
    views.append(DockView(
        '3d', (ctypes.c_bool * 1)(True), render_view.draw))

    is_point = (ctypes.c_bool * 1)(False)

    def show_env(p_open: ctypes.Array):
        if ImGui.Begin("env", p_open):
            ImGui.Checkbox("point or direction", is_point)
            if is_point[0]:
                render_view.light.w = 1
            else:
                render_view.light.w = 0
            ImGui.SliderFloat3(
                'light position', render_view.light, -10, 10)  # type: ignore
        ImGui.End()
    views.append(DockView(
        'env', (ctypes.c_bool * 1)(True), show_env))

    # logger
    from pydear.utils.loghandler import ImGuiLogHandler
    log_handle = ImGuiLogHandler()
    log_handle.register_root()
    views.append(DockView('log', (ctypes.c_bool * 1)
                          (True), log_handle.draw))

    return views


class PydearController(BaseController):
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

        self.imgui_font()

        self.io.DisplayFramebufferScale = ImGui.ImVec2(scale, scale)
        from pydear.backends.opengl import Renderer
        self.impl_gl = Renderer()
        self.viewport = (1, 1)

        # imgui view
        self.imgui_docks = [dock for dock in self.imgui_create_docks()]

    def imgui_create_docks(self) -> List[DockView]:
        return create_docks()

    def imgui_font(self):
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

    def imgui_draw(self):
        from pydear.utils.dockspace import dockspace
        dockspace(self.imgui_docks)

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
        self.imgui_draw()
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
