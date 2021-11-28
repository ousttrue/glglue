import ctypes
from typing import List, NamedTuple, Optional, Union
from OpenGL import GL
from ..scene.vertices import Planar, Interleaved, TypedBytes


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

    def set_vertex_attribute(self, data: bytes, stride: int, offsets: List[int], is_dynamic: bool) -> None:
        ''' float2, 3, 4'''
        self.stride = stride
        self.vertex_count = len(data) // stride
        self.bind()
        GL.glBufferData(GL.GL_ARRAY_BUFFER, len(data), data,
                        GL.GL_DYNAMIC_DRAW if is_dynamic else GL.GL_STATIC_DRAW)
        self.unbind()
        if offsets:
            for i, offset in enumerate(offsets):
                end = stride
                if i < len(offsets)-1:
                    end = offsets[i+1]
                self.attributes.append(
                    VertexAttribute(offset, stride, (end-offset) // 4))
        else:
            self.attributes.append(VertexAttribute(0, stride, stride // 4))

    def update(self, data: bytes) -> None:
        self.bind()
        GL.glBufferSubData(GL.GL_ARRAY_BUFFER, 0, len(data), data)
        self.unbind()

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


def create_vbo_from(src: Union[Planar, Interleaved], is_dynamic=False) -> List[VBO]:
    vbo_list = []
    match src:
        case Planar(attributes):
            for a in attributes:
                vbo = VBO()
                vbo.set_vertex_attribute(
                    a.data, a.stride(), [], is_dynamic)
                vbo_list.append(vbo)
        case Interleaved(vertices, offsets):
            vbo = VBO()
            vbo.set_vertex_attribute(
                vertices.data, vertices.stride(), offsets, is_dynamic)
            vbo_list.append(vbo)
        case _:
            raise RuntimeError()
    return vbo_list


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
        self.unbind()

    def draw(self) -> None:
        self.bind()
        GL.glDrawElements(self.topology, self.index_count,
                          self.index_type, None)


def create_ibo_from(src: TypedBytes) -> IBO:
    ibo = IBO()
    ibo.set_indices(src.data, src.stride())
    return ibo


class VAO:
    '''
    https://wlog.flatlib.jp/item/1629
    '''

    def __init__(self, index_format=None):
        self.vao = GL.glGenVertexArrays(1)
        self.index_format = index_format

    def __del__(self) -> None:
        GL.glDeleteVertexArrays(1, [self.vao])

    def bind(self):
        GL.glBindVertexArray(self.vao)

    def unbind(self):
        GL.glBindVertexArray(0)

    def draw(self, topology, offset: int, draw_count: int):
        self.bind()
        if self.index_format:
            GL.glDrawElements(topology, draw_count,
                              self.index_format, ctypes.c_void_p(offset))
        else:
            GL.glDrawArrays(topology, offset, draw_count)
        self.unbind()


def create_vao_from(ibo: Optional[IBO], vbo_list: List[VBO]) -> VAO:
    if ibo:
        vao = VAO(ibo.index_type)
    else:
        vao = VAO()
    vao.bind()
    if ibo:
        ibo.bind()

    if len(vbo_list) == 1 and len(vbo_list[0].attributes) > 1:
        # interleaved
        vbo = vbo_list[0]
        vbo.bind()
        for i, a in enumerate(vbo.attributes):
            GL.glEnableVertexAttribArray(i)
            GL.glVertexAttribPointer(i, a.component_count, GL.GL_FLOAT, GL.GL_FALSE,
                                     a.stride,  ctypes.c_void_p(a.offset))
    else:
        # planar
        for i, vbo in enumerate(vbo_list):
            vbo.bind()
            vbo.set_slot(i)

    vao.unbind()
    return vao


class Drawable(NamedTuple):
    vbo_list: List[VBO]
    ibo: Optional[IBO]
    vao: VAO

    def draw(self, topology, offset: int, draw_count: int):
        self.vao.draw(topology, offset, draw_count)


def create(vertices: Union[Planar, Interleaved], indices: Optional[TypedBytes] = None, *, is_dynamic=False):
    vbo_list = create_vbo_from(vertices, is_dynamic=is_dynamic)
    ibo = None
    if indices:
        ibo = create_ibo_from(indices)
    vao = create_vao_from(ibo, vbo_list)
    return Drawable(vbo_list, ibo, vao)
