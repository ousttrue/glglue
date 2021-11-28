from .float3 import *
from .quaternion import *
from .mat4 import *
from .camera import *
from .aabb import *
from typing import NamedTuple


class TRS(NamedTuple):
    trnslation: Float3
    rotation: Quaternion
    scale: Float3

    def to_matrix(self) -> Mat4:
        s = Mat4.new_scale(self.scale.x, self.scale.y, self.scale.z)
        r = Mat4.new_from_quaternion(
            self.rotation.x, self.rotation.y, self.rotation.z, self.rotation.w)
        t = Mat4.new_translation(
            self.trnslation.x, self.trnslation.y, self.trnslation.z)
        return s * r * t
