import glglue.frame_input
from OpenGL import GL
from glglue import glo
from glglue.camera.mouse_camera import MouseCamera


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
        match glo.Shader.load_from_pkg("glglue", "assets/mesh"):
            case str() as error:
                raise Exception(error)
            case glo.Shader() as shader:
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
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glDepthFunc(GL.GL_LESS)

        # https://learnopengl.com/Advanced-OpenGL/Face-culling
        # GL.glEnable(GL.GL_CULL_FACE)

        # clear
        GL.glViewport(0, 0, frame.width, frame.height)
        r = 0
        g = 0.1 if frame.mouse_left else 0
        if frame.height == 0:
            return
        b = 0
        GL.glClearColor(r, g, b, 1.0)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)  # type: ignore

        # render
        self.drawable.draw()

        # flush
        GL.glFlush()
