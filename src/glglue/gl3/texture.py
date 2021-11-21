from OpenGL import GL
from OpenGL.raw.GL.VERSION.GL_1_0 import glTexImage2D


class Texture:
    def __init__(self) -> None:
        self.texture = GL.glGenTextures(1)

    def __del__(self) -> None:
        GL.glDeleteTextures(1, [self.texture])

    def bind(self):
        GL.glBindTexture(GL.GL_TEXTURE_2D, self.texture)

    def unbind(self):
        GL.glBindTexture(GL.GL_TEXTURE_2D, 0)

    def set_image(self, data: bytes, width: int, height: int):
        self.bind()
        GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGBA, width,
                        height, 0, GL.GL_RGBA, GL.GL_UNSIGNED_BYTE, data)
        GL.glTexParameterf(
            GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)
        GL.glTexParameterf(
            GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)
        self.unbind()

    def activate(self, location: int, slot: int):
        self.bind()
        GL.glActiveTexture(GL.GL_TEXTURE0 + slot)  # type: ignore
        GL.glUniform1i(location, slot)
