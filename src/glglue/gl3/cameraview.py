from .rendertarget import RenderView
import ctypes
import cydeer as ImGui


class CameraView:
    def __init__(self) -> None:
        self.rendertarget = RenderView()

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
                self.rendertarget.camera.onLeftDown(mouse_x, mouse_y)
            elif ImGui.IsMouseReleased(0):
                self.rendertarget.camera.onLeftUp(mouse_x, mouse_y)
            if ImGui.IsMouseDown(1):
                self.rendertarget.camera.onRightDown(mouse_x, mouse_y)
            elif ImGui.IsMouseReleased(1):
                self.rendertarget.camera.onRightUp(mouse_x, mouse_y)
            if ImGui.IsMouseDown(2):
                self.rendertarget.camera.onMiddleDown(mouse_x, mouse_y)
            elif ImGui.IsMouseReleased(2):
                self.rendertarget.camera.onMiddleUp(mouse_x, mouse_y)

            if io.MouseWheel:
                self.rendertarget.camera.onWheel(-int(io.MouseWheel))

            if ImGui.IsMouseDragging(0) or ImGui.IsMouseDragging(1) or ImGui.IsMouseDragging(2):
                self.rendertarget.camera.onMotion(mouse_x, mouse_y)

            texture = self.rendertarget.render(int(w), int(h))
            if texture:
                # ImGui.ImageButton(
                #     ctypes.c_void_p(texture), (w, h), (0.0, 0.0), (1.0, 1.0), 0, bg_col=ImGui.ImVec4(0, 0, 0, 1), tint_col=ImGui.ImVec4(1, 1, 1, 1))
                # https://gamedev.stackexchange.com/questions/140693/how-can-i-render-an-opengl-scene-into-an-imgui-window
                # Using a Child allow to fill all the space of the window.
                # It also alows customization
                ImGui.BeginChild(b"cameraview")
                # Because I use the texture from OpenGL, I need to invert the V from the UV.
                ImGui.Image(ctypes.c_void_p(texture), (w, h), (0, 1), (1, 0))
                ImGui.EndChild()
        ImGui.End()
        ImGui.PopStyleVar()
