from typing import NamedTuple
from .float3 import Float3
from .quaternion import Quaternion
from .mat4 import Mat4, Float4
from .camera import Camera, FrameState
from .aabb import AABB
from .hittest import Ray


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
