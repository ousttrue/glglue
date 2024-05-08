import ctypes
import struct
import pkgutil
from glglue import glo
from .mesh_builder import Float3, Vertex
from .drawable import Drawable


WHITE = Float3(1, 1, 1)


class StlTriangle(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("normal", Float3),
        ("position0", Float3),
        ("position1", Float3),
        ("position2", Float3),
        ("attributes", ctypes.c_ushort),
    ]


assert ctypes.sizeof(StlTriangle) == 50


class BinaryReader:
    def __init__(self, data: bytes) -> None:
        self.data = data
        self.pos = 0

    def read(self, size: int) -> bytes:
        if self.pos + size > len(self.data):
            raise RuntimeError()
        data = self.data[self.pos : self.pos + size]
        self.pos += size
        return data

    def read_uint32(self) -> int:
        data = self.read(4)
        return struct.unpack("I", data)[0]

    def read_float32(self) -> float:
        data = self.read(4)
        return struct.unpack("f", data)[0]


def load_teapot() -> ctypes.Array[Vertex]:
    # https://en.wikipedia.org/wiki/Utah_teapot#/media/File:Utah_teapot_(solid).stl
    data = pkgutil.get_data("glglue", "assets/Utah_teapot_(solid).stl")
    assert data

    # https://en.wikipedia.org/wiki/STL_%28file_format%29
    r = BinaryReader(data)

    # UINT8[80]    – Header                 -     80 bytes
    # UINT32       – Number of triangles    -      4 bytes
    _header = r.read(80)
    triangle_count = r.read_uint32()

    triangles_type = StlTriangle * triangle_count
    data = r.read(ctypes.sizeof(triangles_type))
    triangles = triangles_type.from_buffer_copy(data)

    vertices = (Vertex * (triangle_count * 3))()

    def push_triangle(i: int, t: StlTriangle, scale: float):
        p0x, p0y, p0z = t.position0
        p1x, p1y, p1z = t.position1
        p2x, p2y, p2z = t.position2
        nx, ny, nz = t.normal

        v0 = vertices[i]
        v0.position = Float3(p0x * scale, p0z * scale, -p0y * scale)
        v0.normal = Float3(nx, nz, -ny)
        v0.color = WHITE

        v1 = vertices[i + 1]
        v1.position = Float3(p1x * scale, p1z * scale, -p1y * scale)
        v1.normal = Float3(nx, nz, -ny)
        v1.color = WHITE

        v2 = vertices[i + 2]
        v2.position = Float3(p2x * scale, p2z * scale, -p2y * scale)
        v2.normal = Float3(nx, nz, -ny)
        v2.color = WHITE

    for i, t in enumerate(triangles):
        push_triangle(i * 3, t, 0.1)

    return vertices


def create(shader: glo.Shader, props: list[glo.UniformUpdater]) -> Drawable:
    vertices = load_teapot()

    vbo = glo.Vbo()
    vbo.set_vertices(memoryview(vertices))

    vao = glo.Vao(vbo, glo.VertexLayout.create_list(shader.program))

    drawable = Drawable(vao)
    drawable.push_submesh(shader, len(vertices), props)
    return drawable
