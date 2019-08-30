# encoding: utf-8
import sys
import math
import pathlib
import struct
from logging import getLogger
from OpenGL.GL import (glClear, glFlush, glEnable, glClearColor, glViewport,
                       GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT, GL_DEPTH_TEST)

if __name__ == '__main__':
    HERE = pathlib.Path(__file__).absolute().parent
    sys.path.insert(0, str(HERE.parent.parent))
import glglue.ctypesmath
import glglue.gl3

logger = getLogger(__name__)
VELOCITY = 0.1
CLEAR_COLOR = (0.6, 0.6, 0.4, 0.0)
CUBE_VS = '''
#version 330
in vec3 aPosition;
in vec3 aColor;
out vec3 vColor;
uniform mediump mat4 m;
uniform mediump mat4 vp;


void main ()
{
    gl_Position = vec4(aPosition, 1) * m * vp;
    vColor = aColor;
}
'''

CUBE_FS = '''
#version 330
in vec3 vColor;
out vec4 fColor;
void main()
{
    fColor = vec4(vColor, 1);
}
'''


def to_radian(degree):
    return degree / 180.0 * math.pi


class Cube:
    def __init__(self, s):
        self.x_rot = 0
        self.y_rot = 0
        self.m = glglue.ctypesmath.Mat4.new_identity()
        self.is_initialized = False
        self.vbo_position = None
        self.vbo_color = None
        self.ibo = None
        self.shader = None
        self.vertices = [
            -s,
            -s,
            -s,
            s,
            -s,
            -s,
            s,
            s,
            -s,
            -s,
            s,
            -s,
            -s,
            -s,
            s,
            s,
            -s,
            s,
            s,
            s,
            s,
            -s,
            s,
            s,
        ]
        self.colors = [
            0,
            0,
            0,
            1,
            0,
            0,
            0,
            1,
            0,
            0,
            0,
            1,
            0,
            1,
            1,
            1,
            0,
            1,
            1,
            1,
            1,
            1,
            1,
            0,
        ]
        self.indices = [
            0,
            1,
            2,
            2,
            3,
            0,
            0,
            4,
            5,
            5,
            1,
            0,
            1,
            5,
            6,
            6,
            2,
            1,
            2,
            6,
            7,
            7,
            3,
            2,
            3,
            7,
            4,
            4,
            0,
            3,
            4,
            7,
            6,
            6,
            5,
            4,
        ]

    def update(self, delta_ms):
        self.y_rot += delta_ms * VELOCITY
        while self.y_rot > 360.0:
            self.y_rot -= 360.0
        self.x_rot += delta_ms * VELOCITY * 0.5
        while self.x_rot > 360.0:
            self.x_rot -= 360.0
        self.m = glglue.ctypesmath.Mat4.new_rotation_y(to_radian(
            self.y_rot)) * glglue.ctypesmath.Mat4.new_rotation_x(
                to_radian(self.x_rot))

    def initialize(self):
        self.is_initialized = True
        self.vbo_position = glglue.gl3.VBO()
        self.vbo_position.set_vertex_attribute(
            3, struct.pack(f'{len(self.vertices)}f', *self.vertices))
        self.vbo_color = glglue.gl3.VBO()
        self.vbo_color.set_vertex_attribute(
            3, struct.pack(f'{len(self.colors)}f', *self.colors))
        self.ibo = glglue.gl3.IBO()
        self.ibo.set_indices(
            struct.pack(f'{len(self.indices)}H', *self.indices),
            len(self.indices))
        self.shader = glglue.gl3.Shader()
        self.shader.compile(CUBE_VS, CUBE_FS)

    def draw(self, projection, view):
        if not self.is_initialized:
            self.initialize()
        self.shader.use()
        self.shader.uniforms['vp'].set(view * projection)
        self.shader.uniforms['m'].set(self.m)
        self.vbo_position.set_slot(0)
        self.vbo_color.set_slot(1)
        self.ibo.draw()


class Coord:
    def __init__(self, size):
        self.is_initialized = False

    def initialize(self):
        pass

    def draw(self, projection, view):
        if not self.is_initialized:
            self.initialize()


class SampleController:
    def __init__(self):
        self.coord = Coord(1.0)
        self.cube = Cube(0.3)
        self.isInitialized = False
        self.projection = glglue.ctypesmath.Perspective()
        self.view = glglue.ctypesmath.Orbit()
        self.width = 1
        self.height = 1
        self.x = 0
        self.y = 0
        self.left = False
        self.middle = False
        self.right = False

    def onResize(self, w: int, h: int) -> None:
        glViewport(0, 0, w, h)
        self.width = w
        self.height = h
        self.projection.aspect = w / h
        self.projection.update_matrix()

    def onLeftDown(self, x: int, y: int) -> None:
        ''' mouse input '''
        self.left = True
        self.x = x
        self.y = y

    def onLeftUp(self, x: int, y: int) -> None:
        ''' mouse input '''
        self.left = False

    def onMiddleDown(self, x: int, y: int) -> None:
        ''' mouse input '''
        self.middle = True
        self.x = x
        self.y = y

    def onMiddleUp(self, x: int, y: int) -> None:
        ''' mouse input '''
        self.middle = False

    def onRightDown(self, x: int, y: int) -> None:
        ''' mouse input '''
        self.right = True
        self.x = x
        self.y = y

    def onRightUp(self, x: int, y: int) -> None:
        ''' mouse input '''
        self.right = False

    def onMotion(self, x: int, y: int) -> None:
        ''' mouse input '''
        dx = x - self.x
        self.x = x
        dy = y - self.y
        self.y = y

        if self.right:
            self.view.yaw += dx * 0.01
            self.view.pitch += dy * 0.01
            self.view.update_matrix()

        if self.middle:
            plane_height = math.tan(
                self.projection.fov_y * 0.5) * self.view.distance * 2
            self.view.x += dx / self.height * plane_height
            self.view.y -= dy / self.height * plane_height
            self.view.update_matrix()

    def onWheel(self, d: int) -> None:
        ''' mouse input '''
        if d > 0:
            self.view.distance *= 1.1
            self.view.update_matrix()
        elif d < 0:
            self.view.distance *= 0.9
            self.view.update_matrix()

    def onKeyDown(self, keycode: int) -> None:
        pass

    def onUpdate(self, d: int) -> None:
        '''
        milliseconds
        '''
        self.cube.update(d)

    def initialize(self):
        glEnable(GL_DEPTH_TEST)
        glClearColor(*CLEAR_COLOR)
        self.isInitialized = True

    def draw(self):
        if not self.isInitialized:
            self.initialize()
        # OpenGLバッファのクリア
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        self.coord.draw(self.projection.matrix, self.view.matrix)
        self.cube.draw(self.projection.matrix, self.view.matrix)

        glFlush()


if __name__ == "__main__":
    import glglue.glut
    glglue.glut.mainloop(SampleController(),
                         width=480,
                         height=480,
                         title=b"glut")
