from typing import NamedTuple, Iterable, List
from OpenGL import GL
import logging

LOGGER = logging.getLogger(__name__)


class AttributeLocation(NamedTuple):
    name: str
    location: int

    @staticmethod
    def create(program, name: str) -> "AttributeLocation":
        location = GL.glGetAttribLocation(program, name)
        assert location != -1
        return AttributeLocation(name, location)


type_map = {
    GL.GL_FLOAT: (GL.GL_FLOAT, 1),
    GL.GL_FLOAT_VEC2: (GL.GL_FLOAT, 2),
    GL.GL_FLOAT_VEC3: (GL.GL_FLOAT, 3),
    GL.GL_FLOAT_VEC4: (GL.GL_FLOAT, 4),
    GL.GL_FLOAT_MAT2: (GL.GL_FLOAT, 4),
    GL.GL_FLOAT_MAT3: (GL.GL_FLOAT, 9),
    GL.GL_FLOAT_MAT4: (GL.GL_FLOAT, 16),
    GL.GL_FLOAT_MAT2x3: (GL.GL_FLOAT, 6),
    GL.GL_FLOAT_MAT2x4: (GL.GL_FLOAT, 8),
    GL.GL_FLOAT_MAT3x2: (GL.GL_FLOAT, 6),
    GL.GL_FLOAT_MAT3x4: (GL.GL_FLOAT, 12),
    GL.GL_FLOAT_MAT4x2: (GL.GL_FLOAT, 8),
    GL.GL_FLOAT_MAT4x3: (GL.GL_FLOAT, 12),
    GL.GL_INT: (GL.GL_INT, 1),
    GL.GL_INT_VEC2: (GL.GL_INT, 2),
    GL.GL_INT_VEC3: (GL.GL_INT, 3),
    GL.GL_INT_VEC4: (GL.GL_INT, 4),
    GL.GL_UNSIGNED_INT: (GL.GL_UNSIGNED_INT, 1),
    GL.GL_UNSIGNED_INT_VEC2: (GL.GL_UNSIGNED_INT, 2),
    GL.GL_UNSIGNED_INT_VEC3: (GL.GL_UNSIGNED_INT, 3),
    GL.GL_UNSIGNED_INT_VEC4: (GL.GL_UNSIGNED_INT, 4),
    GL.GL_DOUBLE: (GL.GL_DOUBLE, 1),
    GL.GL_DOUBLE_VEC2: (GL.GL_DOUBLE, 2),
    GL.GL_DOUBLE_VEC3: (GL.GL_DOUBLE, 3),
    GL.GL_DOUBLE_VEC4: (GL.GL_DOUBLE, 4),
    GL.GL_DOUBLE_MAT2: (GL.GL_DOUBLE, 4),
    GL.GL_DOUBLE_MAT3: (GL.GL_DOUBLE, 9),
    GL.GL_DOUBLE_MAT4: (GL.GL_DOUBLE, 16),
    GL.GL_DOUBLE_MAT2x3: (GL.GL_DOUBLE, 6),
    GL.GL_DOUBLE_MAT2x4: (GL.GL_DOUBLE, 8),
    GL.GL_DOUBLE_MAT3x2: (GL.GL_DOUBLE, 6),
    GL.GL_DOUBLE_MAT3x4: (GL.GL_DOUBLE, 12),
    GL.GL_DOUBLE_MAT4x2: (GL.GL_DOUBLE, 8),
    GL.GL_DOUBLE_MAT4x3: (GL.GL_DOUBLE, 12),
}


def byte_size(t, n):
    match t:
        case GL.GL_FLOAT:
            return 4 * n
        case _:
            raise NotImplemented()


def to_str(src) -> str:
    match src:
        case str():
            return src
        case bytes():
            return src.decode("ascii")
        case _:
            data = bytes(src)
            pos = data.index(0)
            if pos != -1:
                data = data[:pos]
            return data.decode("ascii")


class VertexLayout(NamedTuple):
    attribute: AttributeLocation
    item_count: int  # maybe float1, 2, 3, 4 and 16
    stride: int
    byte_offset: int

    @staticmethod
    def create_list(program) -> List["VertexLayout"]:
        count = GL.glGetProgramiv(program, GL.GL_ACTIVE_ATTRIBUTES)
        LOGGER.debug(f"Active Attributes: {count}")

        layouts: List[VertexLayout] = []
        stride = 0
        for i in range(count):
            name, size, type_ = GL.glGetActiveAttrib(program, i)
            # https://www.khronos.org/registry/OpenGL-Refpages/gl4/html/glGetActiveAttrib.xhtml
            attribute = AttributeLocation.create(program, to_str(name))
            match type_map.get(type_):
                case (t, n):
                    size = byte_size(t, n)
                    layouts.append(VertexLayout(attribute, n, 0, size))
                    stride += size
                case _:
                    raise RuntimeError()
        # not same with location order
        layouts.sort(key=lambda l: l.attribute.location)

        result = []
        offset = 0
        for layout in layouts:
            result.append(
                VertexLayout(layout.attribute, layout.item_count, stride, offset)
            )
            offset += layout.byte_offset
        return result
