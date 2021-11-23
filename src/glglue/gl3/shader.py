from OpenGL import GL
from glglue import ctypesmath
from typing import Any, NamedTuple, List, Tuple
from .texture import Texture


def compile_shader(src: str, shader_type):
    shader = GL.glCreateShader(shader_type)
    GL.glShaderSource(shader, src)
    GL.glCompileShader(shader)
    error = GL.glGetShaderiv(shader, GL.GL_COMPILE_STATUS)
    if error != GL.GL_TRUE:
        info = GL.glGetShaderInfoLog(shader)
        GL.glDeleteShader(shader)
        raise Exception(info)
    return shader


class UniformMat4:
    def __init__(self, program, name: str) -> None:
        self.program = program
        self.name = name
        self.location = -1

    def set(self, value: ctypesmath.Mat4, transpose=True) -> None:
        if self.location < 0:
            self.location = GL.glGetUniformLocation(self.program, self.name)
        GL.glUniformMatrix4fv(
            self.location, 1, GL.GL_TRUE if transpose else GL.GL_FALSE, value.to_array())


class ShaderSource(NamedTuple):
    vs: str
    vs_macro: Tuple[str, ...]
    fs: str
    fs_macro: Tuple[str, ...]

    def get_vs(self) -> str:
        return ''.join(f'{x}\n' for x in self.vs_macro) + self.vs

    def get_fs(self) -> str:
        return ''.join(f'{x}\n' for x in self.fs_macro) + self.fs


class Shader:
    def __init__(self) -> None:
        self.program = GL.glCreateProgram()
        self.uniforms = {}

    def __del__(self) -> None:
        GL.glDeleteProgram(self.program)

    def compile(self, shader_source: ShaderSource):
        vs = compile_shader(shader_source.get_vs(), GL.GL_VERTEX_SHADER)
        if not vs:
            raise Exception('compile_shader: GL_VERTEX_SHADER')

        fs = compile_shader(shader_source.get_fs(), GL.GL_FRAGMENT_SHADER)
        if not fs:
            raise Exception('compile_shader: GL_FRAGMENT_SHADER')

        GL.glAttachShader(self.program, vs)
        GL.glAttachShader(self.program, fs)
        GL.glLinkProgram(self.program)
        error = GL.glGetProgramiv(self.program, GL.GL_LINK_STATUS)
        GL.glDeleteShader(vs)
        GL.glDeleteShader(fs)
        if error != GL.GL_TRUE:
            info = GL.glGetShaderInfoLog(self.program)
            raise Exception(info)

    def use(self):
        GL.glUseProgram(self.program)

    def unuse(self):
        GL.glUseProgram(0)

    def set_uniform(self, name: str, value: Any, transpose=True):
        u = self.uniforms.get(name)
        if not u:
            u = UniformMat4(self.program, name)
            self.uniforms[name] = u
        u.set(value, transpose)

    def set_texture(self, name: str, slot: int, texture: Texture):
        location = GL.glGetUniformLocation(self.program, name)
        texture.activate(location, slot)


def create_from(shader_source: ShaderSource) -> Shader:
    shader = Shader()
    shader.compile(shader_source)
    return shader
