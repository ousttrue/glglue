import glglue.gl3.vbo
import glglue.gl3.mesh
import ctypes
from OpenGL import GL
from .mesh import Mesh


VS = '''
# version 330
in vec3 aPosition;
in vec3 aColor;
out vec3 vColor;
uniform mediump mat4 vp;


void main ()
{
    gl_Position = vec4(aPosition, 1) * vp;
    vColor = aColor;
}
'''

FS = '''
# version 330
in vec3 vColor;
out vec4 fColor;
void main()
{
    fColor = vec4(vColor, 1);
}
'''


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
    mesh = Mesh(f'axis {size}', glglue.gl3.vbo.Planar([
        glglue.gl3.vbo.TypedBytes(memoryview(
            positions).tobytes(), ctypes.c_float, 3),
        glglue.gl3.vbo.TypedBytes(memoryview(
            colors).tobytes(), ctypes.c_float, 3),
    ]))
    material = glglue.gl3.mesh.Material('axis', VS, FS)
    mesh.add_submesh(material, [], GL.GL_LINES)
    return mesh
