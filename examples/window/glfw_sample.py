import logging
from OpenGL import GL
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    from glglue.gl3.samplecontroller import SampleController
    controller = SampleController()

    import glglue.glfw
    loop = glglue.glfw.LoopManager(controller, title='glfw sample')

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
