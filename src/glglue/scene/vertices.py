from typing import NamedTuple, List, Type
import array
import ctypes


MAP = {
    'B': ctypes.c_uint8,
    'H': ctypes.c_int16,
    'I': ctypes.c_uint32,
}


class VectorView(NamedTuple):
    # only use memoryview.nbytes
    data: memoryview
    # base type
    element_type: Type[ctypes._SimpleCData]
    # vector element count. vec2, vec3, mat4...etc
    element_count: int = 1

    @staticmethod
    def create(src: array.array) -> 'VectorView':
        match src:
            case array.array() as a:
                return VectorView(memoryview(a), MAP[a.typecode])
        raise RuntimeError()

    def get_stride(self) -> int:
        return ctypes.sizeof(self.element_type) * self.element_count

    def get_count(self) -> int:
        return self.data.nbytes // self.get_stride()


class Planar(NamedTuple):
    attributes: List[VectorView]

    def count(self) -> int:
        return self.attributes[0].get_count()


class Interleaved(NamedTuple):
    vertices: VectorView
    offsets: List[int]

    def count(self) -> int:
        return self.vertices.get_count()
