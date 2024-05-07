from OpenGL import GL
import logging
import ctypes

LOGGER = logging.getLogger(__name__)


class Vbo:
    def __init__(self):
        self.vbo = GL.glGenBuffers(1)

    def __del__(self):
        LOGGER.debug(f"delete vbo: {self.vbo}")
        GL.glDeleteBuffers(1, [self.vbo])

    def bind(self):
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.vbo)

    def unbind(self):
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)

    def set_vertices(self, vertices, *, is_dynamic: bool = False):
        self.bind()
        GL.glBufferData(
            GL.GL_ARRAY_BUFFER,
            ctypes.sizeof(vertices),
            vertices,
            GL.GL_DYNAMIC_DRAW if is_dynamic else GL.GL_STATIC_DRAW,
        )
        self.unbind()

    def update(self, vertices, offset=0) -> None:
        self.bind()
        GL.glBufferSubData(
            GL.GL_ARRAY_BUFFER, offset, ctypes.sizeof(vertices), vertices
        )
        self.unbind()


class Ibo:
    def __init__(self):
        self.vbo = GL.glGenBuffers(1)
        self.format = 0

    def __del__(self):
        LOGGER.debug(f"delete vbo: {self.vbo}")
        GL.glDeleteBuffers(1, [self.vbo])

    def bind(self):
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, self.vbo)

    def unbind(self):
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, 0)

    def set_indices(self, indices: ctypes.Array, *, is_dynamic: bool = False):
        match indices._type_:
            case ctypes.c_ushort:
                self.format = GL.GL_UNSIGNED_SHORT
            case ctypes.c_uint:
                self.format = GL.GL_UNSIGNED_INT
            case _:
                raise NotImplementedError()
        self.bind()
        GL.glBufferData(
            GL.GL_ELEMENT_ARRAY_BUFFER,
            ctypes.sizeof(indices),
            indices,
            GL.GL_DYNAMIC_DRAW if is_dynamic else GL.GL_STATIC_DRAW,
        )
        self.unbind()

    def update(self, indices, offset=0) -> None:
        self.bind()
        GL.glBufferSubData(
            GL.GL_ELEMENT_ARRAY_BUFFER, offset, ctypes.sizeof(indices), indices
        )
        self.unbind()
