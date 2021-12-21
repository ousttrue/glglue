import logging
import pathlib
import ctypes
from glglue.gl3.cydeercontroller import CydeerController
from glglue.gl3.renderview import RenderView
from glglue.windowconfig import WindowConfig
import cydeer as ImGui
from cydeer.utils.dockspace import DockView

logger = logging.getLogger(__name__)

CONFIG_FILE = pathlib.Path("window.ini")


class SampleController(CydeerController):
    def imgui_create_docks(self):
        yield DockView(
            'metrics', (ctypes.c_bool * 1)(True), ImGui.ShowMetricsWindow)

        def show_hello(p_open: ctypes.Array):
            # open new window context
            if ImGui.Begin("CustomGUI", p_open):
                # draw text label inside of current window
                if ImGui.Button("Debug"):
                    logger.debug("debug message")
            # close current window context
            ImGui.End()
        yield DockView(
            'hello', (ctypes.c_bool * 1)(True), show_hello)

        #
        # 3D View
        #
        self.view = RenderView()
        yield DockView(
            '3d', (ctypes.c_bool * 1)(True), self.view.draw)

        is_point = (ctypes.c_bool * 1)(False)

        def show_env(p_open: ctypes.Array):
            if ImGui.Begin("env", p_open):
                ImGui.Checkbox("point or direction", is_point)
                if is_point[0]:
                    self.view.light.w = 1
                else:
                    self.view.light.w = 0
                ImGui.SliderFloat3(
                    'light position', self.view.light, -10, 10)
            ImGui.End()
        yield DockView(
            'env', (ctypes.c_bool * 1)(True), show_env)

        # logger
        from cydeer.utils.loghandler import ImGuiLogHandler
        log_handle = ImGuiLogHandler()
        log_handle.register_root()
        yield DockView('log', (ctypes.c_bool * 1)(True), log_handle.draw)


if __name__ == "__main__":
    logging.basicConfig(
        format='%(levelname)s:%(name)s:%(message)s', level=logging.DEBUG)

    controller = SampleController()
    from glglue.gl3.samplecontroller import Scene
    match controller.view.scene:
        case Scene() as scene:
            from glglue.scene.teapot import create_teapot
            scene.drawables = [create_teapot()]

    config = None
    if CONFIG_FILE.exists():
        import json
        config = WindowConfig(**json.loads(CONFIG_FILE.read_bytes()))

    import glglue.glfw
    loop = glglue.glfw.LoopManager(controller,
                                   config=config,
                                   title="cydeer")

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

    config = loop.get_config()
    with CONFIG_FILE.open('w') as w:
        import json
        json.dump(config._asdict(), w)
