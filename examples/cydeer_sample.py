import logging
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    logging.basicConfig(
        format='%(levelname)s:%(name)s:%(message)s', level=logging.DEBUG)

    from glglue.gl3.cydeercontroller import CydeerController
    controller = CydeerController()
    from glglue.scene.teapot import create_teapot
    controller.view.scene.drawables = [create_teapot()]

    import glglue.glfw
    loop = glglue.glfw.LoopManager(controller,
                                  width=640,
                                  height=480,
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
