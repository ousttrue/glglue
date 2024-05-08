from typing import NamedTuple
import glm
from glglue import glo
from .mesh_builder import MeshBuilder
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
VERTICES = [
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


def create(shader: glo.Shader, props: list[glo.UniformUpdater]) -> Drawable:
    builder = MeshBuilder()
    for (i0, i1, i2, i3), rgb in QUADS:
        builder.push_quad(
            VERTICES[i0], VERTICES[i1], VERTICES[i2], VERTICES[i3], glm.vec3(*rgb)
        )
    vertices = builder.create_vertices()

    vbo = glo.Vbo()
    vbo.set_vertices(memoryview(vertices))

    vao = glo.Vao(vbo, glo.VertexLayout.create_list(shader.program))

    drawable = Drawable(vao)
    drawable.push_submesh(shader, len(vertices), props)
    return drawable
