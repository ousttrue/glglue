from OpenGL import GL  # type: ignore
from glglue.glo.shader import Shader, UniformUpdater
from glglue.glo.vao import Vao


class Submesh:
    def __init__(
        self,
        topology: int,
        *,
        draw_count: int = 0,
        shader: Shader | None = None,
        props: list[UniformUpdater] | None = None,
    ) -> None:
        self.topology = topology
        self.draw_count = draw_count
        self.shader = shader
        self.properties = props if props else []


class Drawable:
    def __init__(self, vao: Vao) -> None:
        self.vao = vao
        self.submeshes: list[Submesh] = []

    def push_submesh(
        self,
        shader: Shader,
        draw_count: int,
        properties: list[UniformUpdater],
        *,
        topology: int = GL.GL_TRIANGLES,  # type: ignore
    ):
        assert isinstance(shader, Shader)
        self.submeshes.append(
            Submesh(topology, shader=shader, draw_count=draw_count, props=properties)
        )

    def draw(self):
        self.vao.bind()
        offset = 0
        for submesh in self.submeshes:
            if submesh.shader:
                with submesh.shader:
                    for prop in submesh.properties:
                        prop()
                    self.vao.draw(submesh.draw_count, offset=offset)
            offset += submesh.draw_count
        self.vao.unbind()
