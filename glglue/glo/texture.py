from typing import Optional
from OpenGL import GL
import logging
logger = logging.getLogger(__name__)


class Texture:
    def __init__(self, width: int, height: int, data: Optional[bytes] = None, *, pixel_type=GL.GL_RGBA) -> None:
        self.width = width
        self.height = height
        # GL.GL_RGBA(32bit) or GL.GL_RED(8bit graysclale)
        self.pixel_type = pixel_type
        self.handle = GL.glGenTextures(1)
        logger.debug(f'Texture: {self.handle}')

        self.bind()

        GL.glPixelStorei(GL.GL_UNPACK_ALIGNMENT, 1)
        # GL.glPixelStorei(GL.GL_UNPACK_ROW_LENGTH, width)
        GL.glPixelStorei(GL.GL_UNPACK_SKIP_PIXELS, 0)
        GL.glPixelStorei(GL.GL_UNPACK_SKIP_ROWS, 0)

        GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, self.pixel_type,
                        width, height, 0, self.pixel_type, GL.GL_UNSIGNED_BYTE, data)
        GL.glTexParameteri(
            GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)
        GL.glTexParameteri(
            GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)
        self.unbind()

    def __del__(self):
        logger.debug(f'{self.handle}')
        GL.glDeleteTextures([self.handle])

    def update(self, x, y, w, h, data):
        self.bind()

        GL.glPixelStorei(GL.GL_UNPACK_ALIGNMENT, 1)
        GL.glPixelStorei(GL.GL_UNPACK_ROW_LENGTH, self.width)
        GL.glPixelStorei(GL.GL_UNPACK_SKIP_PIXELS, x)
        GL.glPixelStorei(GL.GL_UNPACK_SKIP_ROWS, y)

        GL.glTexSubImage2D(GL.GL_TEXTURE_2D, 0, x, y, w, h,
                           self.pixel_type, GL.GL_UNSIGNED_BYTE, data)

        GL.glPixelStorei(GL.GL_UNPACK_ALIGNMENT, 4)
        GL.glPixelStorei(GL.GL_UNPACK_ROW_LENGTH, 0)
        GL.glPixelStorei(GL.GL_UNPACK_SKIP_PIXELS, 0)
        GL.glPixelStorei(GL.GL_UNPACK_SKIP_ROWS, 0)

        self.unbind()

    def bind(self):
        GL.glBindTexture(GL.GL_TEXTURE_2D, self.handle)

    def unbind(self):
        GL.glBindTexture(GL.GL_TEXTURE_2D, 0)
