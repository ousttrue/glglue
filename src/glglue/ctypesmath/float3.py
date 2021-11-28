import ctypes


class Float3(ctypes.Structure):
    _fields_ = [
        ('x', ctypes.c_float),
        ('y', ctypes.c_float),
        ('z', ctypes.c_float),
    ]
    __match_args__ = ('x', 'y', 'z')

    def __eq__(self, rhs):
        match rhs:
            case Float3(x, y, z) | (x, y, z):
                return self.x == x and self.y == y and self.z == z
        return False

    def __add__(self, rhs) -> 'Float3':
        match rhs:
            case Float3(x, y, z) | (x, y, z):
                return Float3(self.x + x, self.y + y, self.z + z)
        raise RuntimeError()
