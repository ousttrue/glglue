from glglue.sample.imguicontroller import ImGuiController
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    format='%(levelname)s:%(name)s:%(message)s', level=logging.DEBUG)


class CustomGUI(ImGuiController):
    def on_imgui(self):
        import imgui

        # open new window context
        imgui.begin("CustomGUI", True)
        # draw text label inside of current window
        imgui.text("imgui !")
        # close current window context
        imgui.end()


if __name__ == "__main__":
    controller = CustomGUI()

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
