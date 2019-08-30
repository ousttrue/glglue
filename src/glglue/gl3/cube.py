import struct
import math
import glglue

VELOCITY = 0.1

CUBE_VS = '''
#version 330
in vec3 aPosition;
in vec3 aColor;
out vec3 vColor;
uniform mediump mat4 m;
uniform mediump mat4 vp;


void main ()
{
    gl_Position = vec4(aPosition, 1) * m * vp;
    vColor = aColor;
}
'''

CUBE_FS = '''
#version 330
in vec3 vColor;
out vec4 fColor;
void main()
{
    fColor = vec4(vColor, 1);
}
'''


def to_radian(degree):
    return degree / 180.0 * math.pi


class Cube:
    def __init__(self, s):
        self.x_rot = 0
        self.y_rot = 0
        self.m = glglue.ctypesmath.Mat4.new_identity()
        self.is_initialized = False
        self.vbo_position = None
        self.vbo_color = None
        self.ibo = None
        self.shader = None
        self.vertices = [
            -s,
            -s,
            -s,
            s,
            -s,
            -s,
            s,
            s,
            -s,
            -s,
            s,
            -s,
            -s,
            -s,
            s,
            s,
            -s,
            s,
            s,
            s,
            s,
            -s,
            s,
            s,
        ]
        self.colors = [
            0,
            0,
            0,
            1,
            0,
            0,
            0,
            1,
            0,
            0,
            0,
            1,
            0,
            1,
            1,
            1,
            0,
            1,
            1,
            1,
            1,
            1,
            1,
            0,
        ]
        self.indices = [
            0,
            1,
            2,
            2,
            3,
            0,
            0,
            4,
            5,
            5,
            1,
            0,
            1,
            5,
            6,
            6,
            2,
            1,
            2,
            6,
            7,
            7,
            3,
            2,
            3,
            7,
            4,
            4,
            0,
            3,
            4,
            7,
            6,
            6,
            5,
            4,
        ]

    def update(self, delta_ms):
        self.y_rot += delta_ms * VELOCITY
        while self.y_rot > 360.0:
            self.y_rot -= 360.0
        self.x_rot += delta_ms * VELOCITY * 0.5
        while self.x_rot > 360.0:
            self.x_rot -= 360.0
        self.m = glglue.ctypesmath.Mat4.new_rotation_y(to_radian(
            self.y_rot)) * glglue.ctypesmath.Mat4.new_rotation_x(
                to_radian(self.x_rot))

    def initialize(self):
        self.is_initialized = True
        self.vbo_position = glglue.gl3.VBO()
        self.vbo_position.set_vertex_attribute(
            3, struct.pack(f'{len(self.vertices)}f', *self.vertices))
        self.vbo_color = glglue.gl3.VBO()
        self.vbo_color.set_vertex_attribute(
            3, struct.pack(f'{len(self.colors)}f', *self.colors))
        self.ibo = glglue.gl3.IBO()
        self.ibo.set_indices(
            struct.pack(f'{len(self.indices)}H', *self.indices),
            len(self.indices))
        self.shader = glglue.gl3.Shader()
        self.shader.compile(CUBE_VS, CUBE_FS)

    def draw(self, projection, view):
        if not self.is_initialized:
            self.initialize()
        self.shader.use()
        self.shader.uniforms['vp'].set(view * projection)
        self.shader.uniforms['m'].set(self.m)
        self.vbo_position.set_slot(0)
        self.vbo_color.set_slot(1)
        self.ibo.draw()
