import glglue.frame_input
from OpenGL import GL
from glglue import glo
from glglue.camera.mouse_camera import MouseCamera
import logging

LOGGER = logging.getLogger(__name__)


class SampleScene:
    def __init__(self) -> None:
        self.initialized = False
        self.mouse_camera = MouseCamera()
        self.drawable = None

    def lazy_initialize(self):
        if self.initialized:
            return
        self.initialized = True

        # shader
        shader = glo.Shader.load_from_pkg("glglue", "assets/mesh")
        if shader:
            props = shader.create_props(self.mouse_camera.camera)
            # from glglue.drawable import cube
            # self.drawable = cube.create(shader, props)
            from glglue.drawable import teapot

            self.drawable = teapot.create(shader, props)

    def render(self, frame: glglue.frame_input.FrameInput):
        self.lazy_initialize()
        assert self.drawable

        # update camera
        self.mouse_camera.process(frame)

        # https://learnopengl.com/Advanced-OpenGL/Depth-testing
        GL.glEnable(GL.GL_DEPTH_TEST)  # type: ignore
        GL.glDepthFunc(GL.GL_LESS)  # type: ignore

        # https://learnopengl.com/Advanced-OpenGL/Face-culling
        # GL.glEnable(GL.GL_CULL_FACE)

        # clear
        GL.glViewport(0, 0, frame.width, frame.height)  # type: ignore
        r = 0
        if frame.mouse_left:
            LOGGER.debug("LEFT_MOUSE")
            g = 0.1
        else:
            g = 0
        if frame.height == 0:
            return
        b = 0
        GL.glClearColor(r, g, b, 1.0)  # type: ignore
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)  # type: ignore

        # render
        self.drawable.draw()

        # flush
        GL.glFlush()
