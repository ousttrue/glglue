import math
import ctypes
import array
from OpenGL import GL
from .mesh import Mesh
from .material import Material
from .vertices import Interleaved, VectorView
import pkgutil


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
        0, 1, 2,
        2, 3, 0,
        0, 4, 5,
        5, 1, 0,
        1, 5, 6,
        6, 2, 1,
        2, 6, 7,
        7, 3, 2,
        3, 7, 4,
        4, 0, 3,
        4, 7, 6,
        6, 5, 4,
    ])

    mesh = Mesh(f'cube {s}', Interleaved(
        VectorView(memoryview(vertices), ctypes.c_float, 6), [0, 12]),
        VectorView.create(indices))
    vs = pkgutil.get_data('glglue', 'assets/cube.vs')
    if not vs:
        raise Exception()
    fs = pkgutil.get_data('glglue', 'assets/cube.fs')
    if not fs:
        raise Exception()
    material = Material('cube', vs.decode('utf-8'), fs.decode('utf-8'))
    mesh.add_submesh(material, [], GL.GL_TRIANGLES)
    return mesh
