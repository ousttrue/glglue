from typing import (
    NamedTuple,
    Optional,
    Union,
    Tuple,
    cast,
    List,
    Callable,
    TypeAlias,
    Protocol,
)
from OpenGL import GL
import glm
import logging
from ..camera import Camera

LOGGER = logging.getLogger(__name__)


def GetGLErrorStr(err: int):
    match (err):
        case GL.GL_NO_ERROR:  # type: ignore
            return "No error"
        case GL.GL_INVALID_ENUM:  # type: ignore
            return "Invalid enum"
        case GL.GL_INVALID_VALUE:  # type: ignore
            return "Invalid value"
        case GL.GL_INVALID_OPERATION:  # type: ignore
            return "Invalid operation"
        case GL.GL_STACK_OVERFLOW:  # type: ignore
            return "Stack overflow"
        case GL.GL_STACK_UNDERFLOW:  # type: ignore
            return "Stack underflow"
        case GL.GL_OUT_OF_MEMORY:  # type: ignore
            return "Out of memory"
        case _:
            return "Unknown error"


def CheckGLError():
    while True:
        err: int = GL.glGetError()  # type: ignore
        if GL.GL_NO_ERROR == err:  # type: ignore
            break
        LOGGER.error(f"GL Error: {GetGLErrorStr(err)}")


class ShaderCompile:
    def __init__(self, shader_type: GL.GL_VERTEX_SHADER | GL.GL_FRAGMENT_SHADER):  # type: ignore
        self.shader: int = GL.glCreateShader(shader_type)  # type: ignore

    def compile(self, src: Union[str, bytes]) -> Tuple[bool, str]:
        GL.glShaderSource(self.shader, src, None)
        GL.glCompileShader(self.shader)  # type: ignore
        result = GL.glGetShaderiv(self.shader, GL.GL_COMPILE_STATUS)  # type: ignore
        if result == GL.GL_TRUE:  # type: ignore
            return True, ""
        # error message
        info = GL.glGetShaderInfoLog(self.shader)
        return False, info.decode("ascii")

    def __del__(self):
        GL.glDeleteShader(self.shader)  # type: ignore


UniformUpdater: TypeAlias = Callable[[], None]


class Node(Protocol):
    world_matrix: glm.mat4


class Shader:
    def __init__(self) -> None:
        self.program = cast(int, GL.glCreateProgram())

    def __del__(self):
        GL.glDeleteProgram(self.program)  # type: ignore

    def __enter__(self):
        self.use()

    def __exit__(self, exc_type, exc_value, traceback):  # type: ignore
        self.unuse()
        if exc_type:
            LOGGER.warning(f"{exc_type}: {exc_value}: {traceback}")

    def link(self, vs: int, fs: int) -> Tuple[bool, str]:
        GL.glAttachShader(self.program, vs)  # type: ignore
        GL.glAttachShader(self.program, fs)  # type: ignore
        GL.glLinkProgram(self.program)  # type: ignore
        error = GL.glGetProgramiv(self.program, GL.GL_LINK_STATUS)  # type: ignore
        if error == GL.GL_TRUE:  # type: ignore
            return True, ""

        # error message
        info = GL.glGetProgramInfoLog(self.program)
        return False, info.decode("ascii")

    @staticmethod
    def load(
        vs_src: Union[str, bytes], fs_src: Union[str, bytes]
    ) -> Union["Shader", str]:
        vs = ShaderCompile(GL.GL_VERTEX_SHADER)  # type: ignore
        success, info = vs.compile(vs_src)
        if not success:
            return "vs: " + info
        fs = ShaderCompile(GL.GL_FRAGMENT_SHADER)  # type: ignore
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

        vs = pkgutil.get_data(pkg, f"{name}.vert")
        assert vs
        fs = pkgutil.get_data(pkg, f"{name}.frag")
        assert fs
        match Shader.load(vs, fs):
            case Shader() as shader:
                return shader
            case str() as info:
                LOGGER.error(f"{pkg}#{name}: {info}")

    def create_props(
        self, camera: Camera, node: Node | None = None
    ) -> List[UniformUpdater]:

        props: List[Callable[[], None]] = []

        model = UniformLocation.create(self.program, "u_model")
        if model:
            if node:

                def update_model():
                    model.set_mat4(node.world_matrix)

            else:
                identity = glm.mat4(1)

                def update_model():
                    model.set_mat4(identity)

            props.append(update_model)

        view = UniformLocation.create(self.program, "u_view")
        if view:

            def update_view():
                view.set_mat4(camera.view.matrix)

            props.append(update_view)

        projection = UniformLocation.create(self.program, "u_projection")
        if projection:

            def update_projection():
                projection.set_mat4(camera.projection.matrix)

            props.append(update_projection)

        return props

    def use(self) -> None:
        GL.glUseProgram(self.program)  # type: ignore

    def unuse(self) -> None:
        GL.glUseProgram(0)  # type: ignore


class UniformLocation(NamedTuple):
    name: str
    location: int

    @staticmethod
    def create(program: int, name: str) -> "UniformLocation":
        location: int = GL.glGetUniformLocation(program, name)
        if location == -1:
            LOGGER.warn(f"{name}: -1")
        return UniformLocation(name, location)

    def set_int(self, value: int):
        GL.glUniform1i(self.location, value)  # type: ignore

    def set_float2(self, value: tuple[float, float]):
        GL.glUniform2fv(self.location, 1, value)

    def set_mat4(
        self,
        value: glm.mat4,
        transpose: bool = False,
        count: int = 1,
    ):
        GL.glUniformMatrix4fv(
            self.location, count, GL.GL_TRUE if transpose else GL.GL_FALSE, glm.value_ptr(value)  # type: ignore
        )


class UniformBlockIndex(NamedTuple):
    name: str
    block_index: int

    @staticmethod
    def create(program: int, name: str) -> "UniformBlockIndex":
        block_index = cast(int, GL.glGetUniformBlockIndex(program, name))  # type: ignore
        return UniformBlockIndex(name, block_index)
