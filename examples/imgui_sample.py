# coding: utf-8
from logging import getLogger

logger = getLogger(__name__)

from logging import basicConfig, DEBUG

basicConfig(format='%(levelname)s:%(name)s:%(message)s', level=DEBUG)

if __name__ == "__main__":
    from glglue.sample.imguicontroller import ImGuiController
    controller = ImGuiController()

    import glglue.wgl
    loop = glglue.wgl.LoopManager(controller,
                                  width=640,
                                  height=480,
                                  title=b"imgui")

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
