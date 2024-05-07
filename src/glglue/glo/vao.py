from typing import List, Iterable, Optional
from OpenGL import GL
from .vbo import Vbo, Ibo
from .vertex_layout import VertexLayout
import ctypes


class Vao:
    def __init__(
        self, vbo: Vbo, layouts: Iterable[VertexLayout], ibo: Optional[Ibo] = None
    ) -> None:
        self.vao = GL.glGenVertexArrays(1)
        self.vbo = vbo
        self.bind()
        vbo.bind()
        for layout in layouts:
            GL.glEnableVertexAttribArray(layout.attribute.location)
            GL.glVertexAttribPointer(
                layout.attribute.location,
                layout.item_count,
                GL.GL_FLOAT,
                GL.GL_FALSE,
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

    def bind(self):
        GL.glBindVertexArray(self.vao)

    def unbind(self):
        GL.glBindVertexArray(0)

    def draw(self, count: int, offset: int = 0, *, topology=GL.GL_TRIANGLES):
        self.bind()
        if self.ibo:
            GL.glDrawElements(topology, count, self.ibo.format, ctypes.c_void_p(offset))
        else:
            GL.glDrawArrays(topology, offset, count)
        self.unbind()
