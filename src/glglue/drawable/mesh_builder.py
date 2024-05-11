from typing import TypeVar, Generic, Type
import ctypes
import glm


class Float2(ctypes.Structure):
    _fields_ = [
        ("x", ctypes.c_float),
        ("y", ctypes.c_float),
    ]

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z


class Float3(ctypes.Structure):
    _fields_ = [
        ("x", ctypes.c_float),
        ("y", ctypes.c_float),
        ("z", ctypes.c_float),
    ]

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z


def calc_normal(p0: glm.vec3, p1: glm.vec3, p2: glm.vec3) -> glm.vec3:
    return glm.cross(glm.normalize(p0 - p1), glm.normalize(p2 - p1))  # type: ignore


T = TypeVar("T", bound=ctypes.Structure)


class MeshBuilder(Generic[T]):
    # https://stackoverflow.com/questions/67717984/how-to-add-python-type-hints-to-runtime-type
    def __init__(self, t: Type[T]) -> None:
        self.T = t
        self.vertices: list[T] = []

    def push_triangle(self, p0: T, p1: T, p2: T):
        self.vertices.append(p0)
        self.vertices.append(p1)
        self.vertices.append(p2)

    def push_quad(self, p0: T, p1: T, p2: T, p3: T):
        self.push_triangle(p0, p1, p2)
        self.push_triangle(p2, p3, p0)

    def create_vertices(self) -> ctypes.Array[T]:
        return (self.T * len(self.vertices))(*self.vertices)
