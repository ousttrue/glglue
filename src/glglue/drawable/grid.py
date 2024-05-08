from .. import glo
from .line_builder import LineBuilder
from .drawable import Drawable
import glm
from OpenGL import GL  # type: ignore


def create(shader: glo.Shader, props: list[glo.UniformUpdater], n: int = 5) -> Drawable:
    builder = LineBuilder()

    for x in range(-n, n + 1):
        builder.push_line(
            glm.vec3(x, 0, -n), glm.vec3(x, 0, n), glm.vec3(0.5, 0.5, 0.5)
        )
    for z in range(-n, n + 1):
        builder.push_line(
            glm.vec3(-n, 0, z), glm.vec3(n, 0, z), glm.vec3(0.5, 0.5, 0.5)
        )

    vertices = builder.create_vertices()

    vbo = glo.Vbo()
    vbo.set_vertices(memoryview(vertices))

    vao = glo.Vao(
        vbo, glo.VertexLayout.create_list(shader.program), topology=GL.GL_LINES
    )

    drawable = Drawable(vao)
    drawable.push_submesh(shader, len(vertices), props)
    return drawable
