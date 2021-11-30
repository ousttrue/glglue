from typing import Optional, Union
import ctypes
from OpenGL import GL
from glglue.ctypesmath import *
import glglue.scene.vertices
import glglue.gl3.shader
import glglue.gl3.vbo


class LineVertex(ctypes.Structure):
    _fields_ = [
        ('position', Float3),
        ('color', Float4)
    ]


VS = '''
#version 330
in vec3 aPosition;
in vec4 aColor;
out vec4 vColor;
uniform mediump mat4 vp;

void main() {
  gl_Position = vec4(aPosition, 1) * vp;
  vColor = aColor;
}
'''

FS = '''
#version 330
in vec4 vColor;
out vec4 fColor;
void main() { fColor = vColor; }
'''


class Gizmo:
    def __init__(self) -> None:
        self.vp = Mat4.new_identity()
        self.lines = (LineVertex * 65535)()
        self.line_count = 0
        self.color = Float4(1, 1, 1, 1)
        #
        self.shader = None
        self.drawable = None

    def begin(self, camera_or_vp: Union[Camera, Mat4]):
        self.line_count = 0
        match camera_or_vp:
            case Camera() as camera:
                self.vp = camera.view.matrix * camera.projection.matrix
            case Mat4() as vp:
                self.vp = vp

    def end(self):
        # material
        if not self.shader:
            shader_source = glglue.gl3.shader.ShaderSource(
                VS, (), FS, ())
            self.shader = glglue.gl3.shader.create_from(shader_source)
        self.shader.use()
        self.shader.set_uniform('vp', self.vp)

        # vertices
        if self.drawable:
            self.drawable.vbo_list[0].update(memoryview(self.lines))
        else:
            typed = glglue.scene.vertices.VectorView(
                memoryview(self.lines), ctypes.c_float, 7)
            self.drawable = glglue.gl3.vbo.create(
                glglue.gl3.vbo.Interleaved(typed, [0, 12]), is_dynamic=True)
        self.drawable.draw(GL.GL_LINES, 0, self.line_count)

    def line(self, p0: Float3, p1: Float3, matrix: Mat4):
        p0 = matrix.apply(*p0)
        self.lines[self.line_count] = LineVertex(p0, self.color)
        self.line_count += 1

        p1 = matrix.apply(*p1)
        self.lines[self.line_count] = LineVertex(p1, self.color)
        self.line_count += 1

    def axis(self, size: float, matrix: Optional[Mat4] = None):
        if not matrix:
            matrix = Mat4.new_identity()
        origin = Float3(0, 0, 0)
        # X
        self.color = Float4(1, 0, 0, 1)
        self.line(origin, Float3(size, 0, 0), matrix)
        self.color = Float4(0.5, 0, 0, 1)
        self.line(origin, Float3(-size, 0, 0), matrix)
        # Y
        self.color = Float4(0, 1, 0, 1)
        self.line(origin, Float3(0, size, 0), matrix)
        self.color = Float4(0, 0.5, 0, 1)
        self.line(origin, Float3(0, -size, 0), matrix)
        # Z
        self.color = Float4(0, 0, 1, 1)
        self.line(origin, Float3(0, 0, size), matrix)
        self.color = Float4(0, 0, 0.5, 1)
        self.line(origin, Float3(0, 0, -size), matrix)

    def aabb(self, aabb: AABB, matrix: Optional[Mat4] = None):
        if not matrix:
            matrix = Mat4.new_identity()

        self.color = Float4(1, 1, 1, 1)
        match aabb:
            case AABB(Float3(nx, ny, nz), Float3(px, py, pz)):
                t0 = Float3(nx, py, nz)
                t1 = Float3(px, py, nz)
                t2 = Float3(px, py, pz)
                t3 = Float3(nx, py, pz)
                b0 = Float3(nx, ny, nz)
                b1 = Float3(px, ny, nz)
                b2 = Float3(px, ny, pz)
                b3 = Float3(nx, ny, pz)
                # top
                self.line(t0, t1, matrix)
                self.line(t1, t2, matrix)
                self.line(t2, t3, matrix)
                self.line(t3, t0, matrix)
                # bottom
                self.line(b0, b1, matrix)
                self.line(b1, b2, matrix)
                self.line(b2, b3, matrix)
                self.line(b3, b0, matrix)
                # side
                self.line(t0, b0, matrix)
                self.line(t1, b1, matrix)
                self.line(t2, b2, matrix)
                self.line(t3, b3, matrix)
