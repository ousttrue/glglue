from typing import NamedTuple
import glm
from glglue import glo
import ctypes
from .mesh_builder import MeshBuilder, Float3, calc_normal
from .drawable import Drawable

"""
OpenGL default is ccw

+->
|
v
  4 5
  +-+
 / /
+-+
7 6
  0 1
  +-+
 / /
+-+
3 2
"""
S = 0.6
POSITIONS = [
    glm.vec3(-S, -S, -S),
    glm.vec3(S, -S, -S),
    glm.vec3(S, -S, S),
    glm.vec3(-S, -S, S),
    glm.vec3(-S, S, -S),
    glm.vec3(S, S, -S),
    glm.vec3(S, S, S),
    glm.vec3(-S, S, S),
]


class Face(NamedTuple):
    indices: tuple[int, int, int, int]
    color: tuple[float, float, float]


# CCW
QUADS = [
    Face((7, 3, 2, 6), (0.5, 0.5, 1)),  # front
    Face((5, 1, 0, 4), (0.5, 0.5, 1)),  # back
    Face((6, 2, 1, 5), (1, 0.5, 0.5)),  # right
    Face((4, 0, 3, 7), (1, 0.5, 0.5)),  # left
    Face((4, 7, 6, 5), (0.5, 1, 0.5)),  # top
    Face((0, 1, 2, 3), (0.5, 1, 0.5)),  # bottom
]


class Vertex(ctypes.Structure):
    _fields_ = [
        ("position", Float3),
        ("normal", Float3),
        ("color", Float3),
    ]


def create(shader: glo.Shader, props: list[glo.UniformUpdater]) -> Drawable:
    builder = MeshBuilder(Vertex)
    for (i0, i1, i2, i3), rgb in QUADS:
        p0 = POSITIONS[i0]
        p1 = POSITIONS[i1]
        p2 = POSITIONS[i2]
        p3 = POSITIONS[i3]
        n = Float3(*calc_normal(p0, p1, p2))
        builder.push_quad(
            Vertex(Float3(*p0), n, rgb),
            Vertex(Float3(*p1), n, rgb),
            Vertex(Float3(*p2), n, rgb),
            Vertex(Float3(*p3), n, rgb),
        )
    vertices = builder.create_vertices()

    vbo = glo.Vbo()
    vbo.set_vertices(memoryview(vertices))

    vao = glo.Vao(vbo, glo.VertexLayout.create_list(shader.program))

    drawable = Drawable(vao)
    drawable.push_submesh(shader, len(vertices), props)
    return drawable
