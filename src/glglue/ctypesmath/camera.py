import math
from .mat4 import Mat4


class Perspective:
    def __init__(self) -> None:
        self.matrix = Mat4.new_identity()
        self.fov_y = math.pi * 30 / 180
        self.aspect = 1
        self.z_near = 0.1
        self.z_far = 50
        self.update_matrix()

    def update_matrix(self) -> None:
        self.matrix.perspective(self.fov_y, self.aspect, self.z_near,
                                self.z_far)


class Orbit:
    def __init__(self) -> None:
        self.matrix = Mat4.new_identity()
        self.x = 0
        self.y = 0
        self.distance = 2
        self.yaw = 0
        self.pitch = 0
        self.update_matrix()

    def update_matrix(self) -> None:
        t = Mat4.new_translation(self.x, self.y, -self.distance)
        yaw = Mat4.new_rotation_y(self.yaw)
        pitch = Mat4.new_rotation_x(self.pitch)
        self.matrix = yaw * pitch * t
