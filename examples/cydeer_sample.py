from typing import Optional
import logging
import ctypes
#
from OpenGL import GL
import cydeer as ImGui
from glglue.basecontroller import BaseController
from glglue.ctypesmath.camera import Camera
from glglue.gl3.samplecontroller import BaseScene, Scene
logger = logging.getLogger(__name__)


class Texture:
    def __init__(self, width: int, height: int) -> None:
        self.fbo = GL.glGenFramebuffers(1)
        self.width = width
        self.height = height
        # color
        self.texture = GL.glGenTextures(1)
        GL.glBindTexture(GL.GL_TEXTURE_2D, self.texture)
        GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGBA, width,
                        height, 0, GL.GL_RGBA, GL.GL_UNSIGNED_BYTE, None)
        GL.glTexParameteri(
            GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)
        GL.glTexParameteri(
            GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)
        # depth
        self.depth = GL.glGenRenderbuffers(1)
        GL.glBindRenderbuffer(GL.GL_RENDERBUFFER, self.depth)
        GL.glRenderbufferStorage(
            GL.GL_RENDERBUFFER, GL.GL_DEPTH_COMPONENT, width, height)

        # bind fbo with texture nd depth
        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, self.fbo)
        GL.glFramebufferTexture2D(
            GL.GL_FRAMEBUFFER, GL.GL_COLOR_ATTACHMENT0, GL.GL_TEXTURE_2D, self.texture, 0)
        GL.glFramebufferRenderbuffer(
            GL.GL_FRAMEBUFFER, GL.GL_DEPTH_ATTACHMENT, GL.GL_RENDERBUFFER, self.depth)
        GL.glDrawBuffers([GL.GL_COLOR_ATTACHMENT0])
        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, 0)

        # logger.debug(
        #     f'create fbo {self.fbo}, texture {self.texture}, {self.depth}: {width} x {height}')

    def __del__(self):
        # logger.debug(
        #     f'delte fbo {self.fbo}, texture {self.texture}, {self.depth}')
        if self.fbo:
            GL.glDeleteFramebuffers(1, [self.fbo])
            self.fbo = 0
        if self.texture:
            GL.glDeleteTextures([self.texture])
            self.texture = 0
        if self.depth:
            GL.glDeleteRenderbuffers(1, [self.depth])
            self.depth = 0


class View:
    def __init__(self) -> None:
        self.camera = Camera()
        self.scene: BaseScene = Scene()
        self.texture: Optional[Texture] = None
        self.clear_color = (0.2, 0.2, 0.2, 1)

    def __del__(self):
        if self.texture:
            del self.texture
            self.texture = None

    def render(self, width: int, height: int) -> int:
        if self.texture:
            if self.texture.width != width or self.texture.height != height:
                del self.texture
                self.texture = None
        if width == 0 or height == 0:
            return 0
        if not self.texture:
            self.texture = Texture(width, height)

        #
        # update view camera
        #
        self.camera.onResize(width, height)

        #
        # render
        #
        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, self.texture.fbo)
        GL.glViewport(0, 0, width, height)
        GL.glClearColor(*self.clear_color)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT |
                   GL.GL_DEPTH_BUFFER_BIT)  # type: ignore

        state = self.camera.get_state()
        if self.scene:
            self.scene.draw(state)
        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, 0)
        # <class 'numpy.uintc'>
        return int(self.texture.texture)


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
        # create texture before: ImGui.NewFrame()
        self.io.Fonts.GetTexDataAsRGBA32(
            (ctypes.c_void_p * 1)(),
            (ctypes.c_int * 1)(), (ctypes.c_int * 1)())
        self.io.DisplayFramebufferScale = ImGui.ImVec2(scale, scale)
        from cydeer.backends.opengl import Renderer
        self.impl_gl = Renderer()
        self.viewport = (1, 1)

        #
        # 3D View
        #
        self.view = View()

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

        def show_render_view(p_open: ctypes.Array):
            '''
            button に fbo を描画する
            '''
            ImGui.PushStyleVar_2(
                ImGui.ImGuiStyleVar_.WindowPadding, ImGui.ImVec2(0, 0))
            if ImGui.Begin(
                    "render target", None, ImGui.ImGuiWindowFlags_.NoScrollbar | ImGui.ImGuiWindowFlags_.NoScrollWithMouse):
                w, h = ImGui.GetContentRegionAvail()
                x, y = ImGui.GetWindowPos()
                y += ImGui.GetFrameHeight()
                io = ImGui.GetIO()

                mouse_x = io.MousePos.x - x
                mouse_y = -(io.MousePos.y - y)

                if ImGui.IsMouseDown(0):
                    self.view.camera.onLeftDown(mouse_x, mouse_y)
                elif ImGui.IsMouseReleased(0):
                    self.view.camera.onLeftUp(mouse_x, mouse_y)
                if ImGui.IsMouseDown(1):
                    self.view.camera.onRightDown(mouse_x, mouse_y)
                elif ImGui.IsMouseReleased(1):
                    self.view.camera.onRightUp(mouse_x, mouse_y)
                if ImGui.IsMouseDown(2):
                    self.view.camera.onMiddleDown(mouse_x, mouse_y)
                elif ImGui.IsMouseReleased(2):
                    self.view.camera.onMiddleUp(mouse_x, mouse_y)

                if io.MouseWheel:
                    self.view.camera.onWheel(int(io.MouseWheel))

                if ImGui.IsMouseDragging(0) or ImGui.IsMouseDragging(1) or ImGui.IsMouseDragging(2):
                    self.view.camera.onMotion(mouse_x, mouse_y)

                texture = self.view.render(int(w), int(h))
                if texture:
                    ImGui.ImageButton(
                        ctypes.c_void_p(texture), (w, h), (0.0, 0.0), (1.0, 1.0), 0, bg_col=ImGui.ImVec4(0, 0, 0, 1), tint_col=ImGui.ImVec4(1, 1, 1, 1))
            ImGui.End()
            ImGui.PopStyleVar()
        self.scene_view = DockView(
            '3d', (ctypes.c_bool * 1)(True), show_render_view)

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
        from cydeer.utils.dockspace import dockspace
        dockspace(self.metrics_view, self.hello_view, self.scene_view)
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


if __name__ == "__main__":
    logging.basicConfig(
        format='%(levelname)s:%(name)s:%(message)s', level=logging.DEBUG)

    controller = CydeerController()

    import glglue.wgl
    loop = glglue.wgl.LoopManager(controller,
                                  width=640,
                                  height=480,
                                  title=b"cydeer")

    lastCount = 0
    while True:
        count = loop.begin_frame()
        if not count:
            break
        d = count - lastCount
        lastCount = count
        if d > 0:
            controller.onUpdate(d)
            controller.draw()
            loop.end_frame()
