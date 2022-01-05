from typing import Optional
import ctypes
from OpenGL import GL
#
import pydear as ImGui
#
from ..ctypesmath import Camera, Float4
from .rendertarget import RenderTarget
from .samplecontroller import Scene


class RenderView:
    def __init__(self) -> None:
        self.camera = Camera()
        self.scene = Scene()
        self.render_target: Optional[RenderTarget] = None
        self.clear_color = (0.2, 0.2, 0.2, 1)
        self.light = Float4(1, 1, 1, 1)
        self.hovered = False

    def __del__(self):
        if self.render_target:
            del self.render_target
            self.render_target = None

    def _render(self, width: int, height: int) -> int:
        if self.render_target:
            if self.render_target.width != width or self.render_target.height != height:
                del self.render_target
                self.render_target = None
        if width <= 0 or height <= 0:
            return 0
        if not self.render_target:
            self.render_target = RenderTarget(width, height)

        #
        # update view camera
        #
        self.camera.onResize(width, height)

        #
        # render
        #
        with self.render_target.bind_context():
            GL.glViewport(0, 0, width, height)
            GL.glClearColor(*self.clear_color)
            GL.glClear(GL.GL_COLOR_BUFFER_BIT |
                       GL.GL_DEPTH_BUFFER_BIT)  # type: ignore

            state = self.camera.get_state(self.light)
            if self.scene:
                self.scene.draw(state)

        # <class 'numpy.uintc'>
        return int(self.render_target.texture)

    def draw(self, p_open: ctypes.Array):
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
            mouse_y = io.MousePos.y - y

            if ImGui.IsMouseDown(0):
                self.camera.onLeftDown(mouse_x, mouse_y)
            elif ImGui.IsMouseReleased(0):
                self.camera.onLeftUp(mouse_x, mouse_y)
            if ImGui.IsMouseDown(1):
                self.camera.onRightDown(mouse_x, mouse_y)
            elif ImGui.IsMouseReleased(1):
                self.camera.onRightUp(mouse_x, mouse_y)
            if ImGui.IsMouseDown(2):
                self.camera.onMiddleDown(mouse_x, mouse_y)
            elif ImGui.IsMouseReleased(2):
                self.camera.onMiddleUp(mouse_x, mouse_y)

            if self.hovered and io.MouseWheel:
                self.camera.onWheel(-int(io.MouseWheel))

            if ImGui.IsMouseDragging(0) or ImGui.IsMouseDragging(1) or ImGui.IsMouseDragging(2):
                self.camera.onMotion(mouse_x, mouse_y)

            texture = self._render(int(w), int(h))
            if texture:
                # ImGui.ImageButton(
                #     ctypes.c_void_p(texture), (w, h), (0.0, 0.0), (1.0, 1.0), 0, bg_col=ImGui.ImVec4(0, 0, 0, 1), tint_col=ImGui.ImVec4(1, 1, 1, 1))
                # https://gamedev.stackexchange.com/questions/140693/how-can-i-render-an-opengl-scene-into-an-imgui-window
                # Using a Child allow to fill all the space of the window.
                # It also alows customization
                ImGui.BeginChild(b"cameraview")
                # Because I use the texture from OpenGL, I need to invert the V from the UV.
                ImGui.Image(ctypes.c_void_p(texture), (w, h), (0, 1), (1, 0))
                self.hovered = ImGui.IsItemHovered()
                ImGui.EndChild()
        ImGui.End()
        ImGui.PopStyleVar()
