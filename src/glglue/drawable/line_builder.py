from typing import List
import ctypes
import glm


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


class Vertex(ctypes.Structure):
    _fields_ = [
        ("position", Float3),
        ("color", Float3),
    ]


class LineBuilder:
    def __init__(self) -> None:
        self.vertices: List[Vertex] = []

    def push_line(self, p0: glm.vec3, p1: glm.vec3, color: glm.vec3):
        self.vertices.append(
            Vertex(
                Float3(p0.x, p0.y, p0.z),
                Float3(color.x, color.y, color.z),
            )
        )
        self.vertices.append(
            Vertex(
                Float3(p1.x, p1.y, p1.z),
                Float3(color.x, color.y, color.z),
            )
        )

    def create_vertices(self) -> ctypes.Array[Vertex]:
        vertices = (Vertex * len(self.vertices))(*self.vertices)
        return vertices
