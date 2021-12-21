from typing import Iterable, Dict, Optional
import logging
import pathlib
import ctypes
#
import glglue.glfw
from glglue.gl3.cydeercontroller import CydeerController
from glglue.gl3.renderview import RenderView
from glglue.windowconfig import WindowConfig
import cydeer as ImGui
from cydeer.utils.dockspace import DockView

logger = logging.getLogger(__name__)

CONFIG_FILE = pathlib.Path("window.ini")


def cube():
    view = RenderView()
    return DockView(
        'cube', (ctypes.c_bool * 1)(True), view.draw)


def teapot():
    view = RenderView()
    from glglue.scene.teapot import create_teapot
    view.scene.drawables = [create_teapot()]
    return DockView(
        'teapot', (ctypes.c_bool * 1)(True), view.draw)


def skin():
    view = RenderView()


SCENES = {
    'cube': cube,
    'teapot': teapot,
}


class ImguiDocks:
    def __init__(self) -> None:
        self.metrics = DockView(
            'metrics', (ctypes.c_bool * 1)(True), ImGui.ShowMetricsWindow)
        self.selected = 'teapot'
        self.scenes: Dict[str, Optional[DockView]] = {
            k: None for k, v in SCENES.items()}

        def show_selector(p_open: ctypes.Array):
            # open new window context
            if ImGui.Begin("SceneSelector", p_open):
                for k, v in self.scenes.items():
                    if ImGui.Selectable(k, k == self.selected):
                        self.selected = k
                # draw text label inside of current window
                if ImGui.Button("Debug"):
                    logger.debug("debug message")
            # close current window context
            ImGui.End()
        self.hello = DockView(
            'hello', (ctypes.c_bool * 1)(True), show_selector)

        # logger
        from cydeer.utils.loghandler import ImGuiLogHandler
        log_handle = ImGuiLogHandler()
        log_handle.register_root()
        self.logger = DockView('log', (ctypes.c_bool * 1)
                               (True), log_handle.draw)

    def get_or_create(self, key: str) -> DockView:
        value = self.scenes.get(key)
        if value:
            return value

        # create RenderView
        logger.info(f"create: {key}")
        value = SCENES[key]()
        self.scenes[key] = value
        return value

    def __iter__(self) -> Iterable[DockView]:
        yield self.metrics
        yield self.hello
        yield self.get_or_create(self.selected)
        yield self.logger


class SampleController(CydeerController):
    def imgui_create_docks(self):
        return ImguiDocks()


if __name__ == "__main__":
    logging.basicConfig(
        format='%(levelname)s:%(name)s:%(message)s', level=logging.DEBUG)

    # imgui
    controller = SampleController()

    # glfw
    loop = glglue.glfw.LoopManager(
        controller,
        config=WindowConfig.load_json_from_path(CONFIG_FILE),
        title="cydeer")

    # main loop
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

    # save window config
    config = loop.get_config()
    config.save_json_to_path(CONFIG_FILE)
