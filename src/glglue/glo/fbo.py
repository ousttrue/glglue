from typing import Optional
from .texture import Texture
from OpenGL import GL
import logging
import ctypes

LOGGER = logging.getLogger(__name__)


class Fbo:
    def __init__(self, width, height, *, use_depth=True) -> None:
        self.texture = Texture(width, height)
        self.fbo = GL.glGenFramebuffers(1)
        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, self.fbo)
        GL.glFramebufferTexture2D(
            GL.GL_FRAMEBUFFER,
            GL.GL_COLOR_ATTACHMENT0,
            GL.GL_TEXTURE_2D,
            self.texture.handle,
            0,
        )
        GL.glDrawBuffers([GL.GL_COLOR_ATTACHMENT0])

        if use_depth:
            self.depth = GL.glGenRenderbuffers(1)
            GL.glBindRenderbuffer(GL.GL_RENDERBUFFER, self.depth)
            GL.glRenderbufferStorage(
                GL.GL_RENDERBUFFER, GL.GL_DEPTH_COMPONENT, width, height
            )
            GL.glFramebufferRenderbuffer(
                GL.GL_FRAMEBUFFER,
                GL.GL_DEPTH_ATTACHMENT,
                GL.GL_RENDERBUFFER,
                self.depth,
            )
        else:
            self.depth = 0

        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, 0)
        LOGGER.debug(f"fbo: {self.fbo}, texture: {self.texture}, depth: {self.depth}")

    def __del__(self):
        LOGGER.debug(f"fbo: {self.fbo}")
        GL.glDeleteFramebuffers(1, [self.fbo])

    def bind(self):
        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, self.fbo)

    def unbind(self):
        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, 0)


class FboRenderer:
    """
    https://qiita.com/edo_m18/items/95483cabf50494f53bb5
    """

    def __init__(self) -> None:
        self.fbo: Optional[Fbo] = None

    def clear(self, width, height, color):
        if width == 0 or height == 0:
            return 0

        if self.fbo:
            if self.fbo.texture.width != width or self.fbo.texture.height != height:
                del self.fbo
                self.fbo = None
        if not self.fbo:
            self.fbo = Fbo(width, height)

        self.fbo.bind()
        GL.glViewport(0, 0, width, height)
        GL.glScissor(0, 0, width, height)
        GL.glClearColor(
            color[0] * color[3], color[1] * color[3], color[2] * color[3], color[3]
        )
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)  # type: ignore
        GL.glClearDepth(1.0)
        GL.glDepthFunc(GL.GL_LESS)
        return ctypes.c_void_p(int(self.fbo.texture.handle))
