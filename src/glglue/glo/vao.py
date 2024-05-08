from typing import Iterable
from OpenGL import GL  # type: ignore
from .vbo import Vbo, Ibo
from .vertex_layout import VertexLayout
import ctypes


class Vao:
    def __init__(
        self,
        vbo: Vbo,
        layouts: Iterable[VertexLayout],
        ibo: Ibo | None = None,
        *,
        topology: int = GL.GL_TRIANGLES,  # type: ignore
    ) -> None:
        self.topology = topology
        self.vao: int = GL.glGenVertexArrays(1)
        self.vbo = vbo
        self.bind()
        vbo.bind()
        for layout in layouts:
            GL.glEnableVertexAttribArray(layout.attribute.location)  # type: ignore
            GL.glVertexAttribPointer(
                layout.attribute.location,
                layout.item_count,
                GL.GL_FLOAT,  # type: ignore
                GL.GL_FALSE,  # type: ignore
                layout.stride,
                ctypes.c_void_p(layout.byte_offset),
            )
        self.ibo = None
        if ibo:
            self.ibo = ibo
            ibo.bind()
        self.unbind()

    def __del__(self) -> None:
        GL.glDeleteVertexArrays(1, [self.vao])

    def bind(self) -> None:
        GL.glBindVertexArray(self.vao)  # type: ignore

    def unbind(self) -> None:
        GL.glBindVertexArray(0)  # type: ignore

    def draw(self, count: int, offset: int = 0, *, topology: int | None = None) -> None:
        if topology == None:
            topology = self.topology

        self.bind()
        if self.ibo:
            GL.glDrawElements(topology, count, self.ibo.format, ctypes.c_void_p(offset))  # type: ignore
        else:
            GL.glDrawArrays(topology, offset, count)  # type: ignore
        self.unbind()
