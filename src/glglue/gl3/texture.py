from OpenGL import GL
from OpenGL.raw.GL.VERSION.GL_1_0 import glTexImage2D


import OpenGL.images
OpenGL.images.TYPE_TO_ARRAYTYPE[GL.GL_HALF_FLOAT] = GL.GL_UNSIGNED_SHORT


class Texture:
    def __init__(self) -> None:
        self.texture = GL.glGenTextures(1)

    def __del__(self) -> None:
        GL.glDeleteTextures(1, [self.texture])

    def bind(self):
        GL.glBindTexture(GL.GL_TEXTURE_2D, self.texture)

    def unbind(self):
        GL.glBindTexture(GL.GL_TEXTURE_2D, 0)

    def load(self, data: bytes, width: int, height: int):
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


class CubeMap:
    def __init__(self) -> None:
        self.texture = GL.glGenTextures(1)

    def bind(self):
        GL.glBindTexture(GL.GL_TEXTURE_CUBE_MAP, self.texture)

    def unbind(self):
        GL.glBindTexture(GL.GL_TEXTURE_CUBE_MAP, 0)

    def _load_cube_map_side(self, side_target, data: bytes, width: int, height: int):
        # copy image data into 'target' side of cube map
        GL.glTexImage2D(
            side_target,
            0,
            GL.GL_RGBA16F,
            width,
            height,
            0,
            GL.GL_RGBA,
            GL.GL_HALF_FLOAT,
            data)

    def load(self, xp, xn, yp, yn, zp, zn):
        self.bind()

        # load each image and copy into a side of the cube-map texture
        self._load_cube_map_side(
            GL.GL_TEXTURE_CUBE_MAP_POSITIVE_X, xp.data, xp.width, xp.height)
        self._load_cube_map_side(
            GL.GL_TEXTURE_CUBE_MAP_NEGATIVE_X, xp.data, xp.width, xp.height)
        self._load_cube_map_side(
            GL.GL_TEXTURE_CUBE_MAP_POSITIVE_Y, yp.data, yp.width, yp.height)
        self._load_cube_map_side(
            GL.GL_TEXTURE_CUBE_MAP_NEGATIVE_Y, yp.data, yp.width, yp.height)
        self._load_cube_map_side(
            GL.GL_TEXTURE_CUBE_MAP_POSITIVE_Z, zp.data, zp.width, zp.height)
        self._load_cube_map_side(
            GL.GL_TEXTURE_CUBE_MAP_NEGATIVE_Z, zp.data, zp.width, zp.height)

        # format cube map texture
        GL.glTexParameteri(GL.GL_TEXTURE_CUBE_MAP,
                           GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)
        GL.glTexParameteri(GL.GL_TEXTURE_CUBE_MAP,
                           GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)
        GL.glTexParameteri(GL.GL_TEXTURE_CUBE_MAP,
                           GL.GL_TEXTURE_WRAP_R, GL.GL_CLAMP_TO_EDGE)
        GL.glTexParameteri(GL.GL_TEXTURE_CUBE_MAP,
                           GL.GL_TEXTURE_WRAP_S, GL.GL_CLAMP_TO_EDGE)
        GL.glTexParameteri(GL.GL_TEXTURE_CUBE_MAP,
                           GL.GL_TEXTURE_WRAP_T, GL.GL_CLAMP_TO_EDGE)

        self.unbind()
