import glglue.frame_input
from OpenGL import GL
from glglue import glo
import ctypes


VS = """#version 330
in vec3 aPos;

void main() {
  gl_Position = vec4(aPos, 1);
}
"""

FS = """#version 330
out vec4 FragColor;
void main() { 
    FragColor = vec4(1.0, 1.0, 1.0, 1.0); 
}
"""


class Vec3(ctypes.Structure):
    _fields_ = [
        ("x", ctypes.c_float),
        ("y", ctypes.c_float),
        ("z", ctypes.c_float),
    ]


TRIANGLE = (Vec3 * 3)(
    Vec3(-1, -1, 0),
    Vec3(1, -1, 0),
    Vec3(0, 1, 0),
)


class CubeScene:
    def __init__(self) -> None:
        self.initialized = False

    def lazy_initialize(self):
        if self.initialized:
            return
        self.initialized = True
        # shader
        match glo.Shader.load(VS, FS):
            case str() as error:
                raise Exception(error)
            case glo.Shader() as shader:
                self.shader = shader

        # vbo
        self.vbo = glo.Vbo()
        self.vbo.set_vertices(TRIANGLE)
        self.vao = glo.Vao(
            self.vbo,
            [
                glo.VertexLayout(
                    glo.AttributeLocation.create(self.shader.program, "aPos"), 3, 12, 0
                )
            ],
        )

    def render(self, frame: glglue.frame_input.FrameInput):
        self.lazy_initialize()

        GL.glViewport(0, 0, frame.width, frame.height)

        # update camera

        r = float(frame.x) / float(frame.width)
        g = 1 if frame.left_down else 0
        if frame.height == 0:
            return
        b = float(frame.y) / float(frame.height)
        GL.glClearColor(r, g, b, 1.0)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)  # type: ignore

        self.shader.use()
        self.vao.draw(3)

        GL.glFlush()
