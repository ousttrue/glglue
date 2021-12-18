import logging
import ctypes
#
from OpenGL import GL
import cydeer as ImGui
from glglue.basecontroller import BaseController
from glglue.ctypesmath.camera import Camera
from glglue.gl3.samplecontroller import BaseScene, Scene
logger = logging.getLogger(__name__)


class CydeerController(BaseController):
    """
    [CLASSES] Controllerクラスは、glglueの規約に沿って以下のコールバックを実装する
    """

    def __init__(self, scale: float = 1):
        ImGui.CreateContext()
        self.io = ImGui.GetIO()
        # create texture before: ImGui.NewFrame()
        self.io.Fonts.GetTexDataAsRGBA32(
            (ctypes.c_void_p * 1)(),
            (ctypes.c_int * 1)(), (ctypes.c_int * 1)())
        self.io.DisplayFramebufferScale = ImGui.ImVec2(scale, scale)
        self.viewport = (1, 1)
        self.camera = Camera()
        self.scene: BaseScene = Scene()

        from cydeer.backends.opengl import Renderer
        self.impl_gl = Renderer()

    def onResize(self, w, h):
        if self.viewport == (w, h):
            return False
        self.camera.onResize(w, h)
        self.viewport = (w, h)
        return True

    def onLeftDown(self, x, y):
        self.io.MouseDown[0] = 1
        if not self.io.WantCaptureMouse:
            self.camera.onLeftDown(x, y)

        return False

    def onLeftUp(self, x, y):
        self.io.MouseDown[0] = 0
        if not self.io.WantCaptureMouse:
            self.camera.onLeftUp(x, y)

        return False

    def onMiddleDown(self, x, y):
        self.io.MouseDown[2] = 1
        if not self.io.WantCaptureMouse:
            self.camera.onMiddleDown(x, y)

        return False

    def onMiddleUp(self, x, y):
        self.io.MouseDown[2] = 0
        if not self.io.WantCaptureMouse:
            self.camera.onMiddleUp(x, y)

        return False

    def onRightDown(self, x, y):
        self.io.MouseDown[1] = 1
        if not self.io.WantCaptureMouse:
            self.camera.onRightDown(x, y)

        return False

    def onRightUp(self, x, y):
        self.io.MouseDown[1] = 0
        if not self.io.WantCaptureMouse:
            self.camera.onRightUp(x, y)

        return False

    def onMotion(self, x, y):
        self.io.MousePos = ImGui.ImVec2(x, y)
        if not self.io.WantCaptureMouse:
            self.camera.onMotion(x, y)

        return False

    def onWheel(self, d):
        self.io.MouseWheel = d
        if not self.io.WantCaptureMouse:
            self.camera.onWheel(d)

        return False

    def onKeyDown(self, keycode):
        logger.debug('onKeyDown: %d', keycode)

    def onUpdate(self, d):
        #logger.debug('onUpdate: delta %d ms', d)
        self.io.DeltaTime = d * 0.001
        return True

    def on_imgui(self):
        import cydeer as ImGui

        ImGui.ShowMetricsWindow()

        # open new window context
        ImGui.Begin("CustomGUI")
        # draw text label inside of current window
        ImGui.Text("cydeer !")
        # close current window context
        ImGui.End()

    def draw(self):
        state = self.camera.get_state()

        #
        # imgui
        #
        self.io.DisplaySize = ImGui.ImVec2(*self.viewport)

        # start new frame context
        ImGui.NewFrame()

        self.on_imgui()

        ImGui.EndFrame()

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
        ImGui.Render()
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
