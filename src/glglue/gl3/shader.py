from OpenGL.GL import (glCreateShader, glDeleteShader, glShaderSource,
                       glCompileShader, glGetShaderInfoLog, glGetShaderiv,
                       glCreateProgram, glDeleteProgram, glAttachShader,
                       glLinkProgram, glGetProgramiv, glUseProgram,
                       glGetUniformLocation, glUniformMatrix4fv, GL_TRUE,
                       GL_COMPILE_STATUS, GL_VERTEX_SHADER, GL_FRAGMENT_SHADER,
                       GL_LINK_STATUS)
from glglue import ctypesmath

VS = '''
#version 330
in vec3 aPosition;
uniform mediump mat4 m;
void main ()
{
    gl_Position = vec4(aPosition, 1) * m;
}
'''

FS = '''
#version 330
out vec4 FragColor;
void main()
{
    FragColor = vec4(1, 1, 1, 1);
}
'''


def load_shader(src: str, shader_type: int) -> int:
    shader = glCreateShader(shader_type)
    glShaderSource(shader, src)
    glCompileShader(shader)
    error = glGetShaderiv(shader, GL_COMPILE_STATUS)
    if error != GL_TRUE:
        info = glGetShaderInfoLog(shader)
        glDeleteShader(shader)
        raise Exception(info)
    return shader


class UniformMat4:
    def __init__(self, program: int, name: str) -> None:
        self.program = program
        self.name = name
        self.location = -1

    def set(self, value: ctypesmath.Mat4) -> None:
        if self.location < 0:
            self.location = glGetUniformLocation(self.program, self.name)
        glUniformMatrix4fv(self.location, 1, GL_TRUE, value.to_array())


class Shader:
    def __init__(self) -> None:
        self.program = glCreateProgram()
        self.uniforms = {
            'm': UniformMat4(self.program, 'm'),
            'vp': UniformMat4(self.program, 'vp'),
        }

    def __del__(self) -> None:
        glDeleteProgram(self.program)

    def compile(self, vs_src: str, fs_src: str) -> None:
        vs = load_shader(vs_src, GL_VERTEX_SHADER)
        if not vs:
            return
        fs = load_shader(fs_src, GL_FRAGMENT_SHADER)
        if not fs:
            return
        glAttachShader(self.program, vs)
        glAttachShader(self.program, fs)
        glLinkProgram(self.program)
        error = glGetProgramiv(self.program, GL_LINK_STATUS)
        glDeleteShader(vs)
        glDeleteShader(fs)
        if error != GL_TRUE:
            info = glGetShaderInfoLog(self.program)
            raise Exception(info)

    def use(self):
        glUseProgram(self.program)

    def unuse(self):
        glUseProgram(0)
