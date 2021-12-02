import ctypes
from OpenGL import GL
from glglue.ctypesmath import *
import glglue.scene.vertices
import glglue.gl3.shader
import glglue.gl3.vbo
import logging
logger = logging.getLogger(__name__)


class Vertex(ctypes.Structure):
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
        # state
        self.state = FrameState(Float4(0, 0, 1, 1), 0, 0, False,
                                False, False, Mat4.new_identity(), Mat4.new_identity(), Ray(Float3(0, 0, 0), Float3(0, 0, 1)))
        self.matrix = Mat4.new_identity()
        self.color = Float4(1, 1, 1, 1)
        # event
        self.click_left = False
        self.click_middle = False
        self.click_right = False
        # lines
        self.lines = (Vertex * 65535)()
        self.line_count = 0
        self.line_shader = None
        self.line_drawable = None
        # triangles
        self.triangles = (Vertex * 65535)()
        self.triangle_count = 0
        self.triangle_shader = None
        self.triangle_drawable = None

        # hover selectable
        self.hover = None
        self.hover_last = None

    def begin(self, state: FrameState):
        # clear
        self.line_count = 0
        self.triangle_count = 0
        self.matrix = Mat4.new_identity()
        self.color = Float4(1, 1, 1, 1)
        # update
        self.click_left = self.state.mouse_left_down and not state.mouse_left_down
        self.click_right = self.state.mouse_right_down and not state.mouse_right_down
        self.click_middle = self.state.mouse_middle_down and not state.mouse_middle_down
        self.state = state

        self.hover_last = self.hover
        self.hover = None

    def end(self):
        # material
        if not self.line_shader:
            shader_source = glglue.gl3.shader.ShaderSource(
                VS, (), FS, ())
            self.line_shader = glglue.gl3.shader.create_from(shader_source)
        self.line_shader.use()
        vp = self.state.camera_view * self.state.camera_projection
        self.line_shader.set_uniform('vp', vp)

        self._draw_triangles()
        self._draw_lines()

    def _draw_lines(self):
        if self.line_drawable:
            self.line_drawable.vbo_list[0].update(memoryview(self.lines))
        else:
            typed = glglue.scene.vertices.VectorView(
                memoryview(self.lines), ctypes.c_float, 7)
            self.line_drawable = glglue.gl3.vbo.create(
                glglue.gl3.vbo.Interleaved(typed, [0, 12]), is_dynamic=True)
        self.line_drawable.draw(GL.GL_LINES, 0, self.line_count)

    def _draw_triangles(self):
        if self.triangle_drawable:
            self.triangle_drawable.vbo_list[0].update(
                memoryview(self.triangles))
        else:
            typed = glglue.scene.vertices.VectorView(
                memoryview(self.triangles), ctypes.c_float, 7)
            self.triangle_drawable = glglue.gl3.vbo.create(
                glglue.gl3.vbo.Interleaved(typed, [0, 12]), is_dynamic=True)

        GL.glDisable(GL.GL_DEPTH_TEST)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
        GL.glEnable(GL.GL_BLEND)
        self.triangle_drawable.draw(GL.GL_TRIANGLES, 0, self.triangle_count)
        GL.glDisable(GL.GL_BLEND)
        GL.glEnable(GL.GL_DEPTH_TEST)

    def line(self, p0: Float3, p1: Float3):
        p0 = self.matrix.apply(*p0)
        self.lines[self.line_count] = Vertex(p0, self.color)
        self.line_count += 1

        p1 = self.matrix.apply(*p1)
        self.lines[self.line_count] = Vertex(p1, self.color)
        self.line_count += 1

    def triangle(self, p0: Float3, p1: Float3, p2: Float3, *, intersect=False):
        p0 = self.matrix.apply(*p0)
        p1 = self.matrix.apply(*p1)
        p2 = self.matrix.apply(*p2)

        self.triangles[self.triangle_count] = Vertex(p0, self.color)
        self.triangle_count += 1

        self.triangles[self.triangle_count] = Vertex(p1, self.color)
        self.triangle_count += 1

        self.triangles[self.triangle_count] = Vertex(p2, self.color)
        self.triangle_count += 1

        if intersect:
            return self.state.ray.intersect(p0, p1, p2)

    def quad(self, p0: Float3, p1: Float3, p2: Float3, p3: Float3):
        self.triangle(p0, p1, p2)
        self.triangle(p2, p3, p0)

    def axis(self, size: float):
        origin = Float3(0, 0, 0)
        # X
        self.color = Float4(1, 0, 0, 1)
        self.line(origin, Float3(size, 0, 0))
        self.color = Float4(0.5, 0, 0, 1)
        self.line(origin, Float3(-size, 0, 0))
        # Y
        self.color = Float4(0, 1, 0, 1)
        self.line(origin, Float3(0, size, 0))
        self.color = Float4(0, 0.5, 0, 1)
        self.line(origin, Float3(0, -size, 0))
        # Z
        self.color = Float4(0, 0, 1, 1)
        self.line(origin, Float3(0, 0, size))
        self.color = Float4(0, 0, 0.5, 1)
        self.line(origin, Float3(0, 0, -size))

    def aabb(self, aabb: AABB):
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
                self.line(t0, t1)
                self.line(t1, t2)
                self.line(t2, t3)
                self.line(t3, t0)
                # bottom
                self.line(b0, b1)
                self.line(b1, b2)
                self.line(b2, b3)
                self.line(b3, b0)
                # side
                self.line(t0, b0)
                self.line(t1, b1)
                self.line(t2, b2)
                self.line(t3, b3)

    def bone(self, key, length: float, is_selected: bool = False) -> bool:
        '''
        return True if mouse clicked
        '''
        s = length * 0.1
        # head-tail
        #      0, -1(p1)
        # (p2)  |
        # -1, 0 |
        #     --+--->
        #       |    1, 0(p0)
        #       v
        #      0, +1(p3)
        self.color = Float4(1, 0.0, 1, 1)
        h = Float3(0, 0, 0)
        t = Float3(0, length, 0)
        # self.line(h, t, bone.world_matrix)
        p0 = Float3(s, s, 0)
        p1 = Float3(0, s, -s)
        p2 = Float3(-s, s, 0)
        p3 = Float3(0, s, s)

        self.line(p0, p1)
        self.line(p1, p2)
        self.line(p2, p3)
        self.line(p3, p0)

        # self.line(p2, p0, bone.world_matrix)
        self.color = Float4(1, 0, 0, 1)
        self.line(h, p0)
        self.line(p0, t)
        self.color = Float4(0.1, 0, 0, 1)
        if is_selected:
            self.color = Float4(0.1, 1, 0, 1)
        self.line(h, p2)
        self.line(p2, t)

        # self.line(p1, p3, bone.world_matrix)
        self.color = Float4(0, 0, 1, 1)
        self.line(h, p3)
        self.line(p3, t)
        self.color = Float4(0, 0, 0.1, 1)
        if is_selected:
            self.color = Float4(0, 1, 0.1, 1)
        self.line(h, p1)
        self.line(p1, t)

        # triangles
        clicked = False
        self.color = Float4(0.5, 0.5, 0.5, 0.2)
        if is_selected:
            self.color = Float4(0.7, 0.7, 0, 0.7)
        elif self.hover_last == key:
            self.color = Float4(0, 0.7, 0, 0.7)
            if self.click_left:
                clicked = True

        triangles = (
            (p0, h, p1),
            (p1, h, p2),
            (p2, h, p3),
            (p3, h, p0),
            (p0, t, p1),
            (p1, t, p2),
            (p2, t, p3),
            (p3, t, p0),
        )

        any_hit = False
        for t in triangles:
            hit = self.triangle(*t, intersect=(not any_hit))
            if hit:
                self.hover = key
                any_hit = True

        return clicked
