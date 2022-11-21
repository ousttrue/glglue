from typing import NamedTuple, Optional, Union, Tuple, cast, List, Callable
from OpenGL import GL
import glm
import logging

LOGGER = logging.getLogger(__name__)


def GetGLErrorStr(err):
    match (err):
        case GL.GL_NO_ERROR:
            return "No error"
        case GL.GL_INVALID_ENUM:
            return "Invalid enum"
        case GL.GL_INVALID_VALUE:
            return "Invalid value"
        case GL.GL_INVALID_OPERATION:
            return "Invalid operation"
        case GL.GL_STACK_OVERFLOW:
            return "Stack overflow"
        case GL.GL_STACK_UNDERFLOW:
            return "Stack underflow"
        case GL.GL_OUT_OF_MEMORY:
            return "Out of memory"
        case _:
            return "Unknown error"


def CheckGLError():
    while True:
        err = GL.glGetError()
        if GL.GL_NO_ERROR == err:
            break
        LOGGER.error(f"GL Error: {GetGLErrorStr(err)}")


class ShaderCompile:
    def __init__(self, shader_type):
        """
        GL.GL_VERTEX_SHADER
        GL.GL_FRAGMENT_SHADER
        """
        self.shader = GL.glCreateShader(shader_type)

    def compile(self, src: Union[str, bytes]) -> Tuple[bool, str]:
        GL.glShaderSource(self.shader, src, None)
        GL.glCompileShader(self.shader)
        result = GL.glGetShaderiv(self.shader, GL.GL_COMPILE_STATUS)
        if result == GL.GL_TRUE:
            return True, ""
        # error message
        info = GL.glGetShaderInfoLog(self.shader)
        return False, info.decode("ascii")

    def __del__(self):
        GL.glDeleteShader(self.shader)


class Shader:
    def __init__(self) -> None:
        self.program = cast(int, GL.glCreateProgram())

    def __del__(self):
        GL.glDeleteProgram(self.program)

    def __enter__(self):
        self.use()

    def __exit__(self, exc_type, exc_value, traceback):
        self.unuse()
        if exc_type:
            LOGGER.warning(f"{exc_type}: {exc_value}: {traceback}")

    def link(self, vs, fs) -> Tuple[bool, str]:
        GL.glAttachShader(self.program, vs)
        GL.glAttachShader(self.program, fs)
        GL.glLinkProgram(self.program)
        error = GL.glGetProgramiv(self.program, GL.GL_LINK_STATUS)
        if error == GL.GL_TRUE:
            return True, ""

        # error message
        info = GL.glGetProgramInfoLog(self.program)
        return False, info.decode("ascii")

    @staticmethod
    def load(
        vs_src: Union[str, bytes], fs_src: Union[str, bytes]
    ) -> Union["Shader", str]:
        vs = ShaderCompile(GL.GL_VERTEX_SHADER)
        success, info = vs.compile(vs_src)
        if not success:
            return "vs: " + info
        fs = ShaderCompile(GL.GL_FRAGMENT_SHADER)
        success, info = fs.compile(fs_src)
        if not success:
            return "fs: " + info
        shader = Shader()
        success, info = shader.link(vs.shader, fs.shader)
        if not success:
            return "link: " + info
        return shader

    @staticmethod
    def load_from_pkg(pkg: str, name: str) -> Optional["Shader"]:
        import pkgutil

        vs = pkgutil.get_data(pkg, f"{name}.vs")
        assert vs
        fs = pkgutil.get_data(pkg, f"{name}.fs")
        assert fs
        match Shader.load(vs, fs):
            case Shader() as shader:
                return shader
            case str() as info:
                LOGGER.error(f"{pkg}#{name}: {info}")
            case _:
                raise RuntimeError()

    def create_props(self, camera, node=None) -> List[Callable[[], None]]:
        from .. import glo

        props: List[Callable[[], None]] = []

        model = UniformLocation.create(self.program, "uModel")
        if model:
            if node:

                def update_model():
                    model.set_mat4(glm.value_ptr(node.world_matrix))

            else:
                identity = glm.mat4(1)

                def update_model():
                    model.set_mat4(glm.value_ptr(identity))

            props.append(update_model)

        view = UniformLocation.create(self.program, "uView")
        if view:

            def update_view():
                view.set_mat4(glm.value_ptr(camera.view.matrix))

            props.append(update_view)

        projection = UniformLocation.create(self.program, "uProjection")
        if projection:

            def update_projection():
                projection.set_mat4(glm.value_ptr(camera.projection.matrix))

            props.append(update_projection)

        return props

    def use(self):
        GL.glUseProgram(self.program)

    def unuse(self):
        GL.glUseProgram(0)


class UniformLocation(NamedTuple):
    name: str
    location: int

    @staticmethod
    def create(program, name: str) -> "UniformLocation":
        location = GL.glGetUniformLocation(program, name)
        if location == -1:
            LOGGER.warn(f"{name}: -1")
        return UniformLocation(name, location)

    def set_int(self, value: int):
        GL.glUniform1i(self.location, value)

    def set_float2(self, value):
        GL.glUniform2fv(self.location, 1, value)

    def set_mat4(self, value, transpose: bool = False, count=1):
        GL.glUniformMatrix4fv(
            self.location, count, GL.GL_TRUE if transpose else GL.GL_FALSE, value
        )


class UniformBlockIndex(NamedTuple):
    name: str
    index: int

    @staticmethod
    def create(program, name: str) -> "UniformBlockIndex":
        index = GL.glGetUniformBlockIndex(program, name)
        return UniformBlockIndex(name, index)
