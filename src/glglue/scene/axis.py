import ctypes
from OpenGL import GL
from .mesh import Mesh
from .material import Material
from .vertices import Planar, TypedBytes
import pkgutil


class Float3(ctypes.Structure):
    _fields_ = [
        ('x', ctypes.c_float),
        ('y', ctypes.c_float),
        ('z', ctypes.c_float),
    ]


def create_axis(size: float) -> Mesh:
    positions = (Float3 * 12)(
        Float3(0,
               0,
               0),
        Float3(size,
               0,
               0),
        Float3(0,
               0,
               0),
        Float3(-size,
               0,
               0),
        Float3(0,
               0,
               0),
        Float3(0,
               size,
               0),
        Float3(0,
               0,
               0),
        Float3(0,
               -size,
               0),
        Float3(0,
               0,
               0),
        Float3(0,
               0,
               size),
        Float3(0,
               0,
               0),
        Float3(0,
               0,
               -size),
    )
    colors = (Float3 * 12)(
        Float3(1,
               0,
               0),
        Float3(1,
               0,
               0),
        Float3(0.5,
               0,
               0),
        Float3(0.5,
               0,
               0),
        Float3(0,
               1,
               0),
        Float3(0,
               1,
               0),
        Float3(0,
               0.5,
               0),
        Float3(0,
               0.5,
               0),
        Float3(0,
               0,
               1),
        Float3(0,
               0,
               1),
        Float3(0,
               0,
               0.5),
        Float3(0,
               0,
               0.5),
    )
    mesh = Mesh(f'axis {size}', Planar([
        TypedBytes(memoryview(
            positions).tobytes(), ctypes.c_float, 3),
        TypedBytes(memoryview(
            colors).tobytes(), ctypes.c_float, 3),
    ]))
    vs = pkgutil.get_data('glglue', 'assets/axis.vs')
    if not vs:
        raise Exception()
    fs = pkgutil.get_data('glglue', 'assets/axis.fs')
    if not fs:
        raise Exception()
    material = Material('axis', vs.decode('utf-8'), fs.decode('utf-8'))
    mesh.add_submesh(material, [], GL.GL_LINES)
    return mesh
