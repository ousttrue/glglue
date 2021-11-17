import ctypes
import array
from typing import List, NamedTuple
from OpenGL import GL


class VertexAttribute(NamedTuple):
    offset: int
    stride: int
    # Vec2, Vec3, Vec4 などの2, 3, 4
    component_count: int


class VBO:
    def __init__(self) -> None:
        self.vbo = GL.glGenBuffers(1)
        self.vertex_count = 0
        self.attributes: List[VertexAttribute] = []

    def __del__(self) -> None:
        GL.glDeleteBuffers(1, [self.vbo])

    def bind(self) -> None:
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.vbo)

    def unbind(self) -> None:
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)

    def set_vertex_attribute(self, data: bytes, stride: int, offsets: List[int]) -> None:
        ''' float2, 3, 4'''
        self.vertex_count = len(data) // stride
        self.bind()
        GL.glBufferData(GL.GL_ARRAY_BUFFER, len(data), data, GL.GL_STATIC_DRAW)
        if offsets:
            for i, offset in enumerate(offsets):
                end = stride
                if i < len(offsets)-1:
                    end = offsets[i+1]
                self.attributes.append(
                    VertexAttribute(offset, stride, (end-offset) // 4))
        else:
            self.attributes.append(VertexAttribute(0, stride, stride // 4))

    def set_slot(self, slot: int) -> None:
        self.bind()
        for a in self.attributes:
            GL.glEnableVertexAttribArray(slot)
            GL.glVertexAttribPointer(slot, a.component_count, GL.GL_FLOAT, GL.GL_FALSE,
                                     a.stride,  ctypes.c_void_p(a.offset))
            slot += 1

    def draw(self) -> None:
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, self.vertex_count)

    def draw_lines(self) -> None:
        GL.glDrawArrays(GL.GL_LINES, 0, self.vertex_count)


def create_vbo_from(src: ctypes.Array, *interleaved_offsets: int) -> VBO:
    vbo = VBO()
    match src:
        case ctypes.Array() as a:
            v = memoryview(a).cast('B').tobytes()
            vbo.set_vertex_attribute(
                v, ctypes.sizeof(a._type_), interleaved_offsets)
        case _:
            raise RuntimeError()
    return vbo


class IBO:
    def __init__(self) -> None:
        self.vbo = GL.glGenBuffers(1)
        self.index_count = 0
        self.index_type = 0
        self.topology = GL.GL_TRIANGLES

    def __del__(self) -> None:
        GL.glDeleteBuffers(1, [self.vbo])

    def bind(self) -> None:
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, self.vbo)

    def unbind(self) -> None:
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, 0)

    def set_indices(self, data: bytes, stride: int) -> None:
        self.index_count = len(data) // stride
        self.bind()
        if stride == 1:
            raise Exception("not implemented")
        elif stride == 2:
            self.index_type = GL.GL_UNSIGNED_SHORT
        elif stride == 4:
            self.index_type = GL.GL_UNSIGNED_INT
        GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER,
                        len(data), data, GL.GL_STATIC_DRAW)

    def draw(self) -> None:
        self.bind()
        GL.glDrawElements(self.topology, self.index_count,
                          self.index_type, None)


def create_ibo_from(src: array.array) -> IBO:
    ibo = IBO()
    match src:
        case array.array() as a:
            v = memoryview(a).cast('B')
            ibo.set_indices(v.tobytes(), a.itemsize)
        case _:
            raise RuntimeError()
    return ibo


class VAO:
    def __init__(self):
        self.vao = GL.glGenVertexArrays(1)

    def __del__(self) -> None:
        GL.glDeleteVertexArrays(1, [self.vao])

    def bind(self):
        GL.glBindVertexArray(self.vao)

    def unbind(self):
        GL.glBindVertexArray(0)


def create_vao_from(vbo: VBO, ibo: IBO) -> VAO:
    vao = VAO()

    vao.bind()
    vbo.bind()
    ibo.bind()
    vao.unbind()

    return vao
