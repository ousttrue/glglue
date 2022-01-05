import ctypes
import array
from OpenGL import GL
#
from .node import Node
from .mesh import Mesh
from .skin import Skin
from .material import Material
from .vertices import Interleaved, VectorView
from glglue.ctypesmath import Float3, Mat4


class Vertex(ctypes.Structure):
    _fields_ = [
        ('position', Float3),
        ('normal', Float3),
    ]


def create_skin() -> Node:
    green = Float3(0, 1, 0)
    red = Float3(1, 0, 0)
    s = 0.1
    h1 = s*2
    h2 = s*4
    h3 = s*6
    vertices = (Vertex * 16)(
        Vertex(Float3(-s, 0, s), red),
        Vertex(Float3(s, 0, s), red),
        Vertex(Float3(s, 0, -s), red),
        Vertex(Float3(-s, 0, -s), red),
        Vertex(Float3(-s, h1, s), red),
        Vertex(Float3(s, h1, s), red),
        Vertex(Float3(s, h1, -s), red),
        Vertex(Float3(-s, h1, -s), red),
        Vertex(Float3(-s, h2, s), green),
        Vertex(Float3(s, h2, s), green),
        Vertex(Float3(s, h2, -s), green),
        Vertex(Float3(-s, h2, -s), green),
        Vertex(Float3(-s, h3, s), green),
        Vertex(Float3(s, h3, s), green),
        Vertex(Float3(s, h3, -s), green),
        Vertex(Float3(-s, h3, -s), green),
    )
    indices = array.array('H')

    def push_quad(i0, i1, i2, i3):
        indices.append(i0)
        indices.append(i1)
        indices.append(i2)
        #
        indices.append(i2)
        indices.append(i3)
        indices.append(i0)
    '''
      +---+
     /   /|  15 14
    +---+ +12 13
    |   |/|  11 10
    +---+ + 8  9
    |   |/|   7  6
    +---+ + 4  5
    |   |/    3  2
    +---+   0  1
    '''
    push_quad(0, 4, 5, 1)
    push_quad(4, 8, 9, 5)
    push_quad(8, 12, 13, 9)

    push_quad(1, 5, 6, 2)
    push_quad(5, 9, 10, 6)
    push_quad(9, 13, 14, 10)

    push_quad(2, 6, 7, 3)
    push_quad(6, 10, 11, 7)
    push_quad(10, 14, 15, 11)

    push_quad(3, 7, 4, 0)
    push_quad(7, 11, 8, 4)
    push_quad(11, 15, 12, 8)

    mesh = Mesh(
        'skin',
        Interleaved(VectorView(memoryview(vertices),
                    ctypes.c_float, 6), [0, 12]),
        VectorView.create(indices))
    material = Material.from_assets('cube')

    mesh.add_submesh(material, [], GL.GL_TRIANGLES)

    bone0 = Node('bone0', Mat4.new_identity())
    bone1 = Node('bone1', Mat4.new_translation(0, h2, 0))
    bone0.children.append(bone1)
    bone0.meshes.append(mesh)

    # bone0.skin = Skin([bone0, bone1])

    return bone0
