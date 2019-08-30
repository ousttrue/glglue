from OpenGL.GL import (glGenBuffers, glDeleteBuffers, glBindBuffer,
                       glBufferData, GL_STATIC_DRAW, GL_ARRAY_BUFFER,
                       glEnableVertexAttribArray, glVertexAttribPointer,
                       glDrawArrays, glDrawElements, GL_FLOAT,
                       GL_UNSIGNED_SHORT, GL_UNSIGNED_INT, GL_FALSE,
                       GL_TRIANGLES, GL_LINES, GL_ELEMENT_ARRAY_BUFFER)


class VBO:
    def __init__(self) -> None:
        self.vbo = glGenBuffers(1)
        self.component_count = 0  # Vec2, Vec3, Vec4 などの2, 3, 4
        self.vertex_count = 0

    def __del__(self) -> None:
        glDeleteBuffers(1, [self.vbo])

    def bind(self) -> None:
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)

    def unbind(self) -> None:
        glBindBuffer(GL_ARRAY_BUFFER, 0)

    def set_vertex_attribute(self, component_count: int, data: bytes) -> None:
        ''' float2, 3, 4'''
        self.component_count = component_count
        stride = 4 * self.component_count
        self.vertex_count = len(data) // stride
        self.bind()
        glBufferData(GL_ARRAY_BUFFER, len(data), data, GL_STATIC_DRAW)

    def set_slot(self, slot: int) -> None:
        self.bind()
        glEnableVertexAttribArray(slot)
        glVertexAttribPointer(slot, self.component_count, GL_FLOAT, GL_FALSE,
                              0, None)

    def draw(self) -> None:
        glDrawArrays(GL_TRIANGLES, 0, self.vertex_count)

    def draw_lines(self) -> None:
        glDrawArrays(GL_LINES, 0, self.vertex_count)


class IBO:
    def __init__(self) -> None:
        self.vbo = glGenBuffers(1)
        self.index_count = 0
        self.index_type = 0

    def __del__(self) -> None:
        glDeleteBuffers(1, [self.vbo])

    def bind(self) -> None:
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.vbo)

    def unbind(self) -> None:
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)

    def set_indices(self, data: bytes, index_count: int) -> None:
        self.index_count = index_count
        self.bind()
        stride = len(data) // index_count
        if stride == 1:
            raise Exception("not implemented")
        elif stride == 2:
            self.index_type = GL_UNSIGNED_SHORT
        elif stride == 4:
            self.index_type = GL_UNSIGNED_INT
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(data), data, GL_STATIC_DRAW)

    def draw(self) -> None:
        self.bind()
        glDrawElements(GL_TRIANGLES, self.index_count, self.index_type, None)
