import glglue
import ctypes
from OpenGL import GL


VS = '''
#version 330
in vec3 aPosition;
in vec3 aColor;
out vec3 vColor;
uniform mediump mat4 vp;


void main ()
{
    gl_Position = vec4(aPosition, 1) * vp;
    vColor = aColor;
}
'''

FS = '''
#version 330
in vec3 vColor;
out vec4 fColor;
void main()
{
    fColor = vec4(vColor, 1);
}
'''


class Float3(ctypes.Structure):
    _fields_ = [
        ('x', ctypes.c_float),
        ('y', ctypes.c_float),
        ('z', ctypes.c_float),
    ]


class Axis:
    def __init__(self, size):
        self.is_initialized = False
        self.positions = (Float3 * 12)(
            Float3(0,
                   0,
                   0),
            Float3(size,
                   0,
                   0),
            Float3(0,
                   0,
                   0),
            Float3(-size,
                   0,
                   0),
            Float3(0,
                   0,
                   0),
            Float3(0,
                   size,
                   0),
            Float3(0,
                   0,
                   0),
            Float3(0,
                   -size,
                   0),
            Float3(0,
                   0,
                   0),
            Float3(0,
                   0,
                   size),
            Float3(0,
                   0,
                   0),
            Float3(0,
                   0,
                   -size),
        )
        self.colors = (Float3 * 12)(
            Float3(1,
                   0,
                   0),
            Float3(1,
                   0,
                   0),
            Float3(0.5,
                   0,
                   0),
            Float3(0.5,
                   0,
                   0),
            Float3(0,
                   1,
                   0),
            Float3(0,
                   1,
                   0),
            Float3(0,
                   0.5,
                   0),
            Float3(0,
                   0.5,
                   0),
            Float3(0,
                   0,
                   1),
            Float3(0,
                   0,
                   1),
            Float3(0,
                   0,
                   0.5),
            Float3(0,
                   0,
                   0.5),
        )

    def initialize(self):
        self.is_initialized = True
        self.vbo_position = glglue.gl3.vbo.create_vbo_from(self.positions)
        self.vbo_color = glglue.gl3.vbo.create_vbo_from(self.colors)
        self.vao = glglue.gl3.vbo.create_vao_from(
            GL.GL_LINES, None, self.vbo_position, self.vbo_color)
        self.shader = glglue.gl3.shader.create_from(VS, FS)

    def draw(self, projection, view):
        if not self.is_initialized:
            self.initialize()
        self.shader.use()
        self.shader.uniforms['vp'].set(view * projection)
        self.vao.draw()
