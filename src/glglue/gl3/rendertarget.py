import contextlib
from OpenGL import GL


class RenderTarget:
    def __init__(self, width: int, height: int) -> None:
        self.fbo = GL.glGenFramebuffers(1)
        self.width = width
        self.height = height
        # color
        self.texture = GL.glGenTextures(1)
        GL.glBindTexture(GL.GL_TEXTURE_2D, self.texture)
        GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGBA, width,
                        height, 0, GL.GL_RGBA, GL.GL_UNSIGNED_BYTE, None)
        GL.glTexParameteri(
            GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)
        GL.glTexParameteri(
            GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)
        # depth
        self.depth = GL.glGenRenderbuffers(1)
        GL.glBindRenderbuffer(GL.GL_RENDERBUFFER, self.depth)
        GL.glRenderbufferStorage(
            GL.GL_RENDERBUFFER, GL.GL_DEPTH_COMPONENT, width, height)

        # bind fbo with texture nd depth
        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, self.fbo)
        GL.glFramebufferTexture2D(
            GL.GL_FRAMEBUFFER, GL.GL_COLOR_ATTACHMENT0, GL.GL_TEXTURE_2D, self.texture, 0)
        GL.glFramebufferRenderbuffer(
            GL.GL_FRAMEBUFFER, GL.GL_DEPTH_ATTACHMENT, GL.GL_RENDERBUFFER, self.depth)
        GL.glDrawBuffers([GL.GL_COLOR_ATTACHMENT0])
        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, 0)

        # logger.debug(
        #     f'create fbo {self.fbo}, texture {self.texture}, {self.depth}: {width} x {height}')

    def __del__(self):
        # logger.debug(
        #     f'delte fbo {self.fbo}, texture {self.texture}, {self.depth}')
        if self.fbo:
            GL.glDeleteFramebuffers(1, [self.fbo])
            self.fbo = 0
        if self.texture:
            GL.glDeleteTextures([self.texture])
            self.texture = 0
        if self.depth:
            GL.glDeleteRenderbuffers(1, [self.depth])
            self.depth = 0

    def bind(self):
        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, self.fbo)

    def unbind(self):
        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, 0)

    @contextlib.contextmanager
    def bind_context(self):
        self.bind()
        try:
            yield
        finally:
            self.unbind()
