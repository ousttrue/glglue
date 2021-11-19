import math
import ctypes
import array
from OpenGL import GL
import glglue.gl3.vbo
from .mesh import Mesh


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


class Vertex(ctypes.Structure):
    _fields_ = [
        ('x', ctypes.c_float),
        ('y', ctypes.c_float),
        ('z', ctypes.c_float),
        ('r', ctypes.c_float),
        ('g', ctypes.c_float),
        ('b', ctypes.c_float),
    ]


def to_radian(degree):
    return degree / 180.0 * math.pi

# VELOCITY = 0.1
# def rotator():
#     x_rot = 0.0
#     y_rot = 0.0
#     def update(self, delta_ms):
#         y_rot += delta_ms * VELOCITY
#         while y_rot > 360.0:
#             y_rot -= 360.0
#         x_rot += delta_ms * VELOCITY * 0.5
#         while x_rot > 360.0:
#             x_rot -= 360.0
#         self.m = glglue.ctypesmath.Mat4.new_rotation_y(to_radian(
#             self.y_rot)) * glglue.ctypesmath.Mat4.new_rotation_x(
#                 to_radian(self.x_rot))
#     return update


def create_cube(s: float) -> Mesh:
    vertices = (Vertex * 8)(
        Vertex(-s,
               -s,
               -s, 0, 0, 0),
        Vertex(s,
               -s,
               -s, 1, 0, 0),
        Vertex(s,
               s,
               -s, 0, 1, 0),
        Vertex(-s,
               s,
               -s, 0, 0, 1),
        Vertex(-s,
               -s,
               s, 0, 1, 1),
        Vertex(s,
               -s,
               s, 1, 0, 1),
        Vertex(s,
               s,
               s, 1, 1, 1),
        Vertex(-s,
               s,
               s, 1, 1, 0),
    )
    indices = array.array('H', [
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
    ])

    mesh = Mesh(f'cube {s}', glglue.gl3.vbo.Interleaved(
        glglue.gl3.vbo.TypedBytes(memoryview(vertices).tobytes(), GL.GL_FLOAT, 6), [0, 12]),
        glglue.gl3.vbo.TypedBytes.create(indices))
    mesh.add_submesh(GL.GL_TRIANGLES, CUBE_VS, CUBE_FS)
    return mesh
