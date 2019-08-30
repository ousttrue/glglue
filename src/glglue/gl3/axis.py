import struct
import glglue


VS = '''
#version 330
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
#version 330
in vec3 vColor;
out vec4 fColor;
void main()
{
    fColor = vec4(vColor, 1);
}
'''

class Axis:
    def __init__(self, size):
        self.is_initialized = False
        self.positions = [
            0,
            0,
            0,
            size,
            0,
            0,
            0,
            0,
            0,
            -size,
            0,
            0,
            0,
            0,
            0,
            0,
            size,
            0,
            0,
            0,
            0,
            0,
            -size,
            0,
            0,
            0,
            0,
            0,
            0,
            size,
            0,
            0,
            0,
            0,
            0,
            -size,
        ]
        self.colors = [
            1,
            0,
            0,
            1,
            0,
            0,
            0.5,
            0,
            0,
            0.5,
            0,
            0,
            0,
            1,
            0,
            0,
            1,
            0,
            0,
            0.5,
            0,
            0,
            0.5,
            0,
            0,
            0,
            1,
            0,
            0,
            1,
            0,
            0,
            0.5,
            0,
            0,
            0.5,
        ]

    def initialize(self):
        self.is_initialized = True
        self.vbo_position = glglue.gl3.VBO()
        self.vbo_position.set_vertex_attribute(
            3, struct.pack(f'{len(self.positions)}f', *self.positions))
        self.vbo_color = glglue.gl3.VBO()
        self.vbo_color.set_vertex_attribute(
            3, struct.pack(f'{len(self.colors)}f', *self.colors))
        self.shader = glglue.gl3.Shader()
        self.shader.compile(VS, FS)

    def draw(self, projection, view):
        if not self.is_initialized:
            self.initialize()
        self.shader.use()
        self.shader.uniforms['vp'].set(view * projection)
        self.vbo_position.set_slot(0)
        self.vbo_color.set_slot(1)
        self.vbo_position.draw_lines()
