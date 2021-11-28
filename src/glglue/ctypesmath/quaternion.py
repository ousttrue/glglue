import ctypes


class Quaternion(ctypes.Structure):
    _fields_ = [
        ('x', ctypes.c_float),
        ('y', ctypes.c_float),
        ('z', ctypes.c_float),
        ('w', ctypes.c_float),
    ]
    __match_args__ = ('x', 'y', 'z', 'w')

    def __eq__(self, rhs) -> bool:
        match rhs:
            case Quaternion(x, y, z) | (x, y, z):
                return self.x == x and self.y == y and self.z == z
        return False

    def __add__(self, rhs) -> 'Quaternion':
        match rhs:
            case Quaternion(x, y, z) | (x, y, z):
                return Quaternion(self.x + x, self.y + y, self.z + z)
        raise RuntimeError()
