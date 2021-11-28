import ctypes
import math
from typing import Tuple

from glglue.ctypesmath.float3 import Float3


class Mat4(ctypes.Structure):
    _fields_ = [("_11", ctypes.c_float), ("_12", ctypes.c_float),
                ("_13", ctypes.c_float), ("_14", ctypes.c_float),
                ("_21", ctypes.c_float), ("_22", ctypes.c_float),
                ("_23", ctypes.c_float), ("_24", ctypes.c_float),
                ("_31", ctypes.c_float), ("_32", ctypes.c_float),
                ("_33", ctypes.c_float), ("_34", ctypes.c_float),
                ("_41", ctypes.c_float), ("_42", ctypes.c_float),
                ("_43", ctypes.c_float), ("_44", ctypes.c_float)]

    def __str__(self) -> str:
        return f'[{self._11}, {self._12}, {self._13}, {self._14}]' + f'[{self._21}, {self._22}, {self._23}, {self._24}]' + f'[{self._31}, {self._32}, {self._33}, {self._34}]' + f'[{self._41}, {self._42}, {self._43}, {self._44}]'

    def __mul__(self, rhs: 'Mat4') -> 'Mat4':
        m = Mat4()
        m._11 = self._11 * rhs._11 + self._12 * rhs._21 + \
            self._13 * rhs._31 + self._14 * rhs._41
        m._12 = self._11 * rhs._12 + self._12 * rhs._22 + \
            self._13 * rhs._32 + self._14 * rhs._42
        m._13 = self._11 * rhs._13 + self._12 * rhs._23 + \
            self._13 * rhs._33 + self._14 * rhs._43
        m._14 = self._11 * rhs._14 + self._12 * rhs._24 + \
            self._13 * rhs._34 + self._14 * rhs._44

        m._21 = self._21 * rhs._11 + self._22 * rhs._21 + \
            self._23 * rhs._31 + self._24 * rhs._41
        m._22 = self._21 * rhs._12 + self._22 * rhs._22 + \
            self._23 * rhs._32 + self._24 * rhs._42
        m._23 = self._21 * rhs._13 + self._22 * rhs._23 + \
            self._23 * rhs._33 + self._24 * rhs._43
        m._24 = self._21 * rhs._14 + self._22 * rhs._24 + \
            self._23 * rhs._34 + self._24 * rhs._44

        m._31 = self._31 * rhs._11 + self._32 * rhs._21 + \
            self._33 * rhs._31 + self._34 * rhs._41
        m._32 = self._31 * rhs._12 + self._32 * rhs._22 + \
            self._33 * rhs._32 + self._34 * rhs._42
        m._33 = self._31 * rhs._13 + self._32 * rhs._23 + \
            self._33 * rhs._33 + self._34 * rhs._43
        m._34 = self._31 * rhs._14 + self._32 * rhs._24 + \
            self._33 * rhs._34 + self._34 * rhs._44

        m._41 = self._41 * rhs._11 + self._42 * rhs._21 + \
            self._43 * rhs._31 + self._44 * rhs._41
        m._42 = self._41 * rhs._12 + self._42 * rhs._22 + \
            self._43 * rhs._32 + self._44 * rhs._42
        m._43 = self._41 * rhs._13 + self._42 * rhs._23 + \
            self._43 * rhs._33 + self._44 * rhs._43
        m._44 = self._41 * rhs._14 + self._42 * rhs._24 + \
            self._43 * rhs._34 + self._44 * rhs._44
        return m

    def transposed(self) -> 'Mat4':
        return Mat4(
            self._11, self._21, self._31, self._41,
            self._12, self._22, self._32, self._42,
            self._13, self._23, self._33, self._43,
            self._14, self._24, self._34, self._44
        )

    def apply(self, x: float, y: float, z: float) -> Float3:
        return Float3(
            x * self._11 + y * self._21 + z * self._31 + self._41,
            x * self._12 + y * self._22 + z * self._32 + self._42,
            x * self._13 + y * self._23 + z * self._33 + self._43
        )

    def to_array(self):
        return (ctypes.c_float * 16).from_buffer(self)

    def perspective(self, fov_y: float, aspect: float, z_near: float,
                    z_far: float) -> None:
        fov_y *= 0.5
        cot = 1.0 / math.tan(fov_y)
        self._11 = cot / aspect
        self._12 = 0
        self._13 = 0
        self._14 = 0
        self._21 = 0
        self._22 = cot
        self._23 = 0
        self._24 = 0
        self._31 = 0
        self._32 = 0
        self._33 = -(z_far + z_near) / (z_far - z_near)
        self._34 = -1
        self._41 = 0
        self._42 = 0
        self._43 = -2 * z_far * z_near / (z_far - z_near)
        self._44 = 0

    @classmethod
    def new_perspective(cls, fov_y, aspect, z_near, z_far) -> 'Mat4':
        m = cls()
        m.perspective(fov_y, aspect, z_near, z_far)
        return m

    @classmethod
    def new_identity(cls):
        return cls(
            1.0,
            0.0,
            0.0,
            0.0,  #
            0.0,
            1.0,
            0.0,
            0.0,  #
            0.0,
            0.0,
            1.0,
            0.0,  #
            0.0,
            0.0,
            0.0,
            1.0  #
        )

    @staticmethod
    def new_scale(x: float, y: float, z: float) -> 'Mat4':
        return Mat4(
            x, 0, 0, 0,
            0, y, 0, 0,
            0, 0, z, 0,
            0, 0, 0, 1,
        )

    @staticmethod
    def new_translation(x: float, y: float, z: float) -> 'Mat4':
        return Mat4(
            1, 0, 0, 0,  #
            0, 1, 0, 0,  #
            0, 0, 1, 0,  #
            x, y, z, 1  #
        )

    @classmethod
    def new_rotation_z(cls, rad):
        s = math.sin(rad)
        c = math.cos(rad)
        return cls(
            c, s, 0, 0,  #
            -s, c, 0, 0,  #
            0, 0, 1, 0,  #
            0, 0, 0, 1  #
        )

    @classmethod
    def new_rotation_y(cls, rad):
        s = math.sin(rad)
        c = math.cos(rad)
        return cls(
            c, 0, -s, 0,  #
            0, 1, 0, 0,  #
            s, 0, c, 0,  #
            0, 0, 0, 1  #
        )

    @classmethod
    def new_rotation_x(cls, rad):
        s = math.sin(rad)
        c = math.cos(rad)
        return cls(
            1, 0, 0, 0,  #
            0, c, s, 0,  #
            0, -s, c, 0,  #
            0, 0, 0, 1  #
        )

    @staticmethod
    def new_from_quaternion(x: float, y: float, z: float, w: float) -> 'Mat4':
        xx = x * x
        yy = y * y
        zz = z * z

        xy = x * y
        yz = y * z
        zx = z * w

        wx = w * x
        wy = w * y
        wz = w * z

        return Mat4(
            1-2*yy-2*xx, 2*xy+2*wz, 2*zx-2*wy, 0,
            2*xy-2*wz, 1-2*xx-2*zz, 2*yz+2*wx, 0,
            2*zx+2*wy, 2*yz-2*wx, 1-2*xx-2*yy, 0,
            0, 0, 0, 1
        )
        # return Mat4(
        #     1-2*yy-2*xx, 2*xy-2*wz, 2*zx+2*wy, 0,
        #     2*xy+2*wz, 1-2*xx-2*zz, 2*yz-2*wx, 0 ,
        #     2*zx-2*wy, 2*yz+2*wx, 1-2*xx-2*yy, 0,
        #     0, 0, 0, 1
        # )


class Float4(ctypes.Structure):
    _fields_ = [("x", ctypes.c_float), ("y", ctypes.c_float),
                ("z", ctypes.c_float), ("w", ctypes.c_float)]

    def __mul__(self, m: Mat4) -> 'Float4':
        v = Float4()
        v.x = self.x * m._11 + self.y * m._21 + self.z * m._31 + self.w * m._41
        v.y = self.x * m._12 + self.y * m._22 + self.z * m._32 + self.w * m._42
        v.z = self.x * m._13 + self.y * m._23 + self.z * m._33 + self.w * m._43
        v.w = self.x * m._14 + self.y * m._24 + self.z * m._34 + self.w * m._44
        return v
