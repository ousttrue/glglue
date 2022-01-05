from typing import Iterable
import ctypes
import pkgutil
import struct
from OpenGL import GL
from .mesh import Mesh, Material
from .vertices import Interleaved, VectorView


class Float3(ctypes.Structure):
    _fields_ = [
        ('x', ctypes.c_float),
        ('y', ctypes.c_float),
        ('z', ctypes.c_float),
    ]

    def __iter__(self) -> Iterable[float]:
        yield self.x
        yield self.y
        yield self.z


class StlTriangle(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('normal', Float3),
        ('position0', Float3),
        ('position1', Float3),
        ('position2', Float3),
        ('attributes', ctypes.c_ushort),
    ]


assert ctypes.sizeof(StlTriangle) == 50


class Vertex(ctypes.Structure):
    _fields_ = [
        ('position', Float3),
        ('normal', Float3),
    ]


class BinaryReader:
    def __init__(self, data: bytes) -> None:
        self.data = data
        self.pos = 0

    def read(self, size: int) -> bytes:
        if self.pos + size > len(self.data):
            raise RuntimeError()
        data = self.data[self.pos:self.pos+size]
        self.pos += size
        return data

    def read_uint32(self) -> int:
        data = self.read(4)
        return struct.unpack('I', data)[0]

    def read_float32(self) -> float:
        data = self.read(4)
        return struct.unpack('f', data)[0]


class Builder:
    def __init__(self, triangle_count: int):
        self.vertices = (Vertex * (triangle_count * 3))()

    def push_triangle(self, i: int, t: StlTriangle, scale: float):
        p0x, p0y, p0z = t.position0
        p1x, p1y, p1z = t.position1
        p2x, p2y, p2z = t.position2
        nx, ny, nz = t.normal
        v0 = self.vertices[i]
        v0.position = Float3(p0x*scale, p0z*scale, -p0y*scale)
        v0.normal = Float3(nx, nz, -ny)
        v1 = self.vertices[i+1]
        v1.position = Float3(p1x*scale, p1z*scale, -p1y*scale)
        v1.normal = Float3(nx, nz, -ny)
        v2 = self.vertices[i+2]
        v2.position = Float3(p2x*scale, p2z*scale, -p2y*scale)
        v2.normal = Float3(nx, nz, -ny)

    def build(self):
        mesh = Mesh('teapot', Interleaved(
            VectorView(memoryview(self.vertices), ctypes.c_float, 6), [0, 12]))

        vs = pkgutil.get_data('glglue', 'assets/teapot.vs')
        if not vs:
            raise Exception()
        fs = pkgutil.get_data('glglue', 'assets/teapot.fs')
        if not fs:
            raise Exception()
        material = Material('teapot', vs.decode('utf-8'), fs.decode('utf-8'))

        mesh.add_submesh(material, [], GL.GL_TRIANGLES)

        return mesh


def create_teapot() -> Mesh:

    # https://en.wikipedia.org/wiki/Utah_teapot#/media/File:Utah_teapot_(solid).stl
    data = pkgutil.get_data('glglue', 'assets/Utah_teapot_(solid).stl')
    if not data:
        raise RuntimeError()

    # https://en.wikipedia.org/wiki/STL_%28file_format%29
    r = BinaryReader(data)

    # UINT8[80]    – Header                 -     80 bytes
    # UINT32       – Number of triangles    -      4 bytes
    header = r.read(80)
    triangle_count = r.read_uint32()

    triangles_type = StlTriangle * triangle_count
    data = r.read(ctypes.sizeof(triangles_type))
    triangles = triangles_type.from_buffer_copy(data)

    b = Builder(triangle_count)
    for i, t in enumerate(triangles):
        b.push_triangle(i * 3, t, 0.1)

    return b.build()
