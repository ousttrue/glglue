import ctypes
import math
from typing import Tuple

from glglue.ctypesmath.float3 import Float3


def dot(l, r):
    value = 0
    for ll, rr in zip(l, r):
        value += ll * rr
    return value


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

    def __eq__(self, rhs: 'Mat4') -> bool:
        return (self._11 == rhs._11 and self._12 == rhs._12 and self._13 == rhs._13 and self._14 == rhs._14
                and self._21 == rhs._21 and self._22 == rhs._22 and self._23 == rhs._23 and self._24 == rhs._24
                and self._31 == rhs._31 and self._32 == rhs._32 and self._33 == rhs._33 and self._34 == rhs._34
                and self._41 == rhs._41 and self._42 == rhs._42 and self._43 == rhs._43 and self._44 == rhs._44
                )

    def __mul__(self, rhs: 'Mat4') -> 'Mat4':
        m = Mat4()

        def row(row):
            match row:
                case 1:
                    return self._11, self._12, self._13, self._14
                case 2:
                    return self._21, self._22, self._23, self._24
                case 3:
                    return self._31, self._32, self._33, self._34
                case 4:
                    return self._41, self._42, self._43, self._44
                case _:
                    raise RuntimeError()

        def col(col):
            match col:
                case 1:
                    return rhs._11, rhs._21, rhs._31, rhs._41
                case 2:
                    return rhs._12, rhs._22, rhs._32, rhs._42
                case 3:
                    return rhs._13, rhs._23, rhs._33, rhs._43
                case 4:
                    return rhs._14, rhs._24, rhs._34, rhs._44
                case _:
                    return RuntimeError()

        m._11 = dot(row(1), col(1))
        m._12 = dot(row(1), col(2))
        m._13 = dot(row(1), col(3))
        m._14 = dot(row(1), col(4))

        m._21 = dot(row(2), col(1))
        m._22 = dot(row(2), col(2))
        m._23 = dot(row(2), col(3))
        m._24 = dot(row(2), col(4))

        m._31 = dot(row(3), col(1))
        m._32 = dot(row(3), col(2))
        m._33 = dot(row(3), col(3))
        m._34 = dot(row(3), col(4))

        m._41 = dot(row(4), col(1))
        m._42 = dot(row(4), col(2))
        m._43 = dot(row(4), col(3))
        m._44 = dot(row(4), col(4))

        return m

    def transposed(self, *, no_translation=False) -> 'Mat4':
        if no_translation:
            return Mat4(
                self._11, self._21, self._31, 0,
                self._12, self._22, self._32, 0,
                self._13, self._23, self._33, 0,
                0, 0, 0, 1
            )
        else:
            return Mat4(
                self._11, self._21, self._31, self._41,
                self._12, self._22, self._32, self._42,
                self._13, self._23, self._33, self._43,
                self._14, self._24, self._34, self._44
            )

    def apply(self, x: float, y: float, z: float, *, translate=True) -> Float3:
        if translate:
            return Float3(
                x * self._11 + y * self._21 + z * self._31 + self._41,
                x * self._12 + y * self._22 + z * self._32 + self._42,
                x * self._13 + y * self._23 + z * self._33 + self._43
            )
        else:
            return Float3(
                x * self._11 + y * self._21 + z * self._31,
                x * self._12 + y * self._22 + z * self._32,
                x * self._13 + y * self._23 + z * self._33
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

    def inverse_rigidbody(self) -> 'Mat4':
        '''
        inverse only rotation + translation. no scale

        (R x T)^-1 = T^-1 * R^-1
        '''
        return Mat4.new_translation(-self._41, -self._42, -self._43) * self.transposed(no_translation=True)

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
        ww = w * w

        xy = x * y
        yz = y * z
        zx = z * x

        wx = w * x
        wy = w * y
        wz = w * z

        return Mat4(
            xx-yy-zz+ww, 2*xy+2*wz, 2*zx-2*wy, 0,
            2*xy-2*wz, -xx+yy-zz+ww, 2*yz+2*wx, 0,
            2*zx+2*wy, 2*yz-2*wx, -xx-yy+zz+ww, 0,
            0, 0, 0, 1
        )

    @staticmethod
    def new_axis_angle(axis, angle) -> 'Mat4':
        if angle == 0:
            return Mat4.new_identity()

        c = math.cos(angle)
        s = math.sin(angle)
        xx = axis.x * axis.x
        yy = axis.y * axis.y
        zz = axis.z * axis.z
        xy = axis.x * axis.y
        yz = axis.y * axis.z
        zx = axis.z * axis.x
        xs = axis.x * s
        ys = axis.y * s
        zs = axis.z * s
        return Mat4(
            c + xx * (1-c),  xy * (1-c) - zs, zx * (1-c) + ys, 0,
            xy * (1-c) + zs, c + yy * (1-c), yz * (1-c) - xs, 0,
            zx * (1-c) - ys, yz * (1-c) + xs, c + zz*(1-c), 0,
            0, 0, 0, 1
        )

    @staticmethod
    def new_coords(x: Float3, y: Float3, z: Float3, t: Float3):
        return Mat4(
            x.x, x.y, x.z, 0,
            y.x, y.y, y.z, 0,
            z.x, z.y, z.z, 0,
            t.x, t.y, t.z, 1,
        )


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
