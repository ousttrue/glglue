from typing import Optional
import contextlib
from OpenGL import GL
from glglue.ctypesmath.camera import Camera
from glglue.gl3.samplecontroller import BaseScene, Scene


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


class RenderView:
    def __init__(self) -> None:
        self.camera = Camera()
        self.scene: BaseScene = Scene()
        self.render_target: Optional[RenderTarget] = None
        self.clear_color = (0.2, 0.2, 0.2, 1)

    def __del__(self):
        if self.render_target:
            del self.render_target
            self.render_target = None

    def render(self, width: int, height: int) -> int:
        if self.render_target:
            if self.render_target.width != width or self.render_target.height != height:
                del self.render_target
                self.render_target = None
        if width == 0 or height == 0:
            return 0
        if not self.render_target:
            self.render_target = RenderTarget(width, height)

        #
        # update view camera
        #
        self.camera.onResize(width, height)

        #
        # render
        #
        with self.render_target.bind_context():
            GL.glViewport(0, 0, width, height)
            GL.glClearColor(*self.clear_color)
            GL.glClear(GL.GL_COLOR_BUFFER_BIT |
                       GL.GL_DEPTH_BUFFER_BIT)  # type: ignore

            state = self.camera.get_state()
            if self.scene:
                self.scene.draw(state)

        # <class 'numpy.uintc'>
        return int(self.render_target.texture)
