import ctypes
import math


class Float3(ctypes.Structure):
    _fields_ = [
        ('x', ctypes.c_float),
        ('y', ctypes.c_float),
        ('z', ctypes.c_float),
    ]
    __match_args__ = ('x', 'y', 'z')

    def copy(self) -> 'Float3':
        dst = type(self)()
        ctypes.pointer(dst)[0] = self
        return dst

    def get_length(self) -> float:
        return math.sqrt(Float3.dot(self, self))

    def normalized(self) -> 'Float3':
        f = 1 / self.get_length()
        return self * f

    @staticmethod
    def dot(lhs, rhs) -> float:
        match lhs, rhs:
            case Float3(lx, ly, lz), Float3(rx, ry, rz):
                return lx*rx + ly*ry + lz*rz
        raise NotImplementedError()

    @staticmethod
    def cross(lhs, rhs):
        match lhs, rhs:
            case Float3(lx, ly, lz), Float3(rx, ry, rz):
                return Float3(
                    ly * rz - lz * ry,
                    lz * rx - lx * rz,
                    lx * ry - ly * rx)
        raise NotImplementedError()

    def __str__(self) -> str:
        return f'({self.x:.3f}, {self.y:.3f}, {self.z:.3f})'

    def __iter__(self):
        yield from (self.x, self.y, self.z)

    def __eq__(self, rhs):
        match rhs:
            case Float3(x, y, z) | (x, y, z):
                return self.x == x and self.y == y and self.z == z
        return False

    def __neg__(self) -> 'Float3':
        return Float3(-self.x, -self.y, -self.z)

    def __add__(self, rhs) -> 'Float3':
        match rhs:
            case Float3(x, y, z) | (x, y, z):
                return Float3(self.x + x, self.y + y, self.z + z)
        raise RuntimeError()

    def __sub__(self, rhs) -> 'Float3':
        match rhs:
            case Float3(x, y, z) | (x, y, z):
                return Float3(self.x - x, self.y - y, self.z - z)
        raise RuntimeError()

    def __mul__(self, rhs: float) -> 'Float3':
        return Float3(self.x * rhs, self.y * rhs, self.z * rhs)

    @staticmethod
    def new_inifinity() -> 'Float3':
        return Float3(float('inf'), float('inf'), float('inf'))
