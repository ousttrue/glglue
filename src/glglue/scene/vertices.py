from typing import NamedTuple, Type, List
import ctypes
import array


class TypedBytes(NamedTuple):
    data: bytes
    element_type: Type[ctypes._SimpleCData]
    element_count: int = 1

    @staticmethod
    def create(src: array.array) -> 'TypedBytes':
        match src:
            case array.array() as a:
                match a.typecode:
                    case 'H':
                        return TypedBytes(memoryview(a).tobytes(), ctypes.c_ushort)
        raise RuntimeError()

    def stride(self) -> int:
        return ctypes.sizeof(self.element_type) * self.element_count

    def count(self) -> int:
        return len(self.data) // self.stride()


class Planar(NamedTuple):
    attributes: List[TypedBytes]

    def count(self) -> int:
        return self.attributes[0].count()


class Interleaved(NamedTuple):
    vertices: TypedBytes
    offsets: List[int]

    def count(self) -> int:
        return self.vertices.count()
