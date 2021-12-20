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


class Vertex(ctypes.Structure):
    _fields_ = [
        ('position', Float3),
        ('normal', Float3),
    ]


class Builder:
    def __init__(self) -> None:
        self.vertices = []

    def push_triangle(self, v0, v1, v2, n):
        self.vertices.append(Vertex(Float3(*v0), Float3(*n)))
        self.vertices.append(Vertex(Float3(*v1), Float3(*n)))
        self.vertices.append(Vertex(Float3(*v2), Float3(*n)))

    def build(self) -> Mesh:
        vertices = (Vertex * len(self.vertices))(*self.vertices)
        mesh = Mesh('teapot', Interleaved(
            VectorView(memoryview(vertices), ctypes.c_float, 6), [0, 12]))

        vs = pkgutil.get_data('glglue', 'assets/teapot.vs')
        if not vs:
            raise Exception()
        fs = pkgutil.get_data('glglue', 'assets/teapot.fs')
        if not fs:
            raise Exception()
        material = Material('teapot', vs.decode('utf-8'), fs.decode('utf-8'))

        mesh.add_submesh(material, [], GL.GL_TRIANGLES)

        return mesh


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


def create_teapot() -> Mesh:

    # https://en.wikipedia.org/wiki/Utah_teapot#/media/File:Utah_teapot_(solid).stl
    import pkgutil
    data = pkgutil.get_data('glglue', 'assets/Utah_teapot_(solid).stl')
    if not data:
        raise RuntimeError()

    # https://en.wikipedia.org/wiki/STL_%28file_format%29
    r = BinaryReader(data)

    # UINT8[80]    – Header                 -     80 bytes
    # UINT32       – Number of triangles    -      4 bytes

    header = r.read(80)
    triangle_count = r.read_uint32()

    b = Builder()
    for _ in range(triangle_count):
        nx = r.read_float32()
        ny = r.read_float32()
        nz = r.read_float32()
        p0x = r.read_float32() * 0.1
        p0y = r.read_float32() * 0.1
        p0z = r.read_float32() * 0.1
        p1x = r.read_float32() * 0.1
        p1y = r.read_float32() * 0.1
        p1z = r.read_float32() * 0.1
        p2x = r.read_float32() * 0.1
        p2y = r.read_float32() * 0.1
        p2z = r.read_float32() * 0.1
        _attribute = r.read(2)
        # zup to yup
        b.push_triangle(
            (p0x, p0z, -p0y),
            (p1x, p1z, -p1y),
            (p2x, p2z, -p2y),
            (nx, nz, -ny))

    return b.build()
