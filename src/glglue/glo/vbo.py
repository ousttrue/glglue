from OpenGL import GL
import logging
import ctypes

LOGGER = logging.getLogger(__name__)


class Vbo:
    def __init__(self):
        self.vbo: int = GL.glGenBuffers(1)

    def __del__(self) -> None:
        LOGGER.debug(f"delete vbo: {self.vbo}")
        GL.glDeleteBuffers(1, [self.vbo])

    def bind(self) -> None:
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.vbo)  # type: ignore

    def unbind(self) -> None:
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)  # type: ignore

    def set_vertices(self, vertices: memoryview, *, is_dynamic: bool = False) -> None:
        data = vertices.tobytes()
        self.bind()
        GL.glBufferData(  # type: ignore
            GL.GL_ARRAY_BUFFER,  # type: ignore
            len(data),
            data,
            GL.GL_DYNAMIC_DRAW if is_dynamic else GL.GL_STATIC_DRAW,  # type: ignore
        )
        self.unbind()

    def update(self, vertices: memoryview, offset: int = 0) -> None:
        data = vertices.tobytes()
        self.bind()
        GL.glBufferSubData(  # type: ignore
            GL.GL_ARRAY_BUFFER, offset, len(data), data  # type: ignore
        )
        self.unbind()


class Ibo:
    def __init__(self):
        self.vbo: int = GL.glGenBuffers(1)
        self.format = 0

    def __del__(self) -> None:
        LOGGER.debug(f"delete vbo: {self.vbo}")
        GL.glDeleteBuffers(1, [self.vbo])

    def bind(self) -> None:
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, self.vbo)  # type: ignore

    def unbind(self) -> None:
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, 0)  # type: ignore

    def set_bytes(
        self,
        indices: bytes,
        stride: int,
        *,
        is_dynamic: bool = False,
    ):
        match stride:
            case 2:
                self.format = GL.GL_UNSIGNED_SHORT  # type: ignore
            case 4:
                self.format = GL.GL_UNSIGNED_INT  # type: ignore
            case _:
                raise NotImplementedError()
        self.bind()
        GL.glBufferData(  # type: ignore
            GL.GL_ELEMENT_ARRAY_BUFFER,  # type: ignore
            len(indices),  # bytesize
            indices,
            GL.GL_DYNAMIC_DRAW if is_dynamic else GL.GL_STATIC_DRAW,  # type: ignore
        )
        self.unbind()

    def set_indices(
        self,
        indices: ctypes.Array[ctypes.c_ushort] | ctypes.Array[ctypes.c_uint],
        *,
        is_dynamic: bool = False,
    ):
        match indices._type_:
            case ctypes.c_ushort:
                self.set_bytes(bytes(indices), 2, is_dynamic=is_dynamic)
            case ctypes.c_uint:
                self.set_bytes(bytes(indices), 4, is_dynamic=is_dynamic)
            case _:
                raise NotImplementedError()

    def update(
        self,
        indices: ctypes.Array[ctypes.c_ushort] | ctypes.Array[ctypes.c_uint],
        offset: int = 0,
    ) -> None:
        self.bind()
        GL.glBufferSubData(  # type: ignore
            GL.GL_ELEMENT_ARRAY_BUFFER,  # type: ignore
            offset,
            ctypes.sizeof(indices),  # bytesize
            indices,  # type: ignore
        )
        self.unbind()
