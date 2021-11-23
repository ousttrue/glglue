'''
https://antongerdelan.net/opengl/cubemaps.html
'''
import array
import ctypes
import pkgutil
from typing import NamedTuple
from OpenGL import GL
from .vertices import Planar, TypedBytes
from .mesh import Mesh
from .material import Material
from .texture import CubeMap


def create_cubemap(cubemap: CubeMap, size: float = 10.0):
    vertices = array.array('f', [
        -size,  size, -size,
        -size, -size, -size,
        size, -size, -size,
        size, -size, -size,
        size,  size, -size,
        -size,  size, -size,

        -size, -size,  size,
        -size, -size, -size,
        -size,  size, -size,
        -size,  size, -size,
        -size,  size,  size,
        -size, -size,  size,

        size, -size, -size,
        size, -size,  size,
        size,  size,  size,
        size,  size,  size,
        size,  size, -size,
        size, -size, -size,

        -size, -size,  size,
        -size,  size,  size,
        size,  size,  size,
        size,  size,  size,
        size, -size,  size,
        -size, -size,  size,

        -size,  size, -size,
        size,  size, -size,
        size,  size,  size,
        size,  size,  size,
        -size,  size,  size,
        -size,  size, -size,

        -size, -size, -size,
        -size, -size,  size,
        size, -size, -size,
        size, -size, -size,
        -size, -size,  size,
        size, -size,  size
    ])

    mesh = Mesh(f'cubemap', Planar(
        [TypedBytes(memoryview(vertices).tobytes(), ctypes.c_float, 3)]))

    vs = pkgutil.get_data('glglue', 'assets/cubemap.vs')
    if not vs:
        raise Exception()
    fs = pkgutil.get_data('glglue', 'assets/cubemap.fs')
    if not fs:
        raise Exception()
    material = Material('cubemap', vs.decode('utf-8'), fs.decode('utf-8'))
    material.cubemap = cubemap
    mesh.add_submesh(material, [], GL.GL_TRIANGLES)
    return mesh
