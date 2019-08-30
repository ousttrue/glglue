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


class Camera:
    def __init__(self):
        self.projection = Perspective()
        self.view = Orbit()
        self.width = 1
        self.height = 1
        self.x = 0
        self.y = 0
        self.left = False
        self.middle = False
        self.right = False

    def onResize(self, w, h):
        self.width = w
        self.height = h
        self.projection.aspect = w / h
        self.projection.update_matrix()

    def onLeftDown(self, x: int, y: int) -> None:
        ''' mouse input '''
        self.left = True
        self.x = x
        self.y = y

    def onLeftUp(self, x: int, y: int) -> None:
        ''' mouse input '''
        self.left = False

    def onMiddleDown(self, x: int, y: int) -> None:
        ''' mouse input '''
        self.middle = True
        self.x = x
        self.y = y

    def onMiddleUp(self, x: int, y: int) -> None:
        ''' mouse input '''
        self.middle = False

    def onRightDown(self, x: int, y: int) -> None:
        ''' mouse input '''
        self.right = True
        self.x = x
        self.y = y

    def onRightUp(self, x: int, y: int) -> None:
        ''' mouse input '''
        self.right = False

    def onMotion(self, x: int, y: int) -> None:
        ''' mouse input '''
        dx = x - self.x
        self.x = x
        dy = y - self.y
        self.y = y

        if self.right:
            self.view.yaw -= dx * 0.01
            self.view.pitch -= dy * 0.01
            self.view.update_matrix()

        if self.middle:
            plane_height = math.tan(
                self.projection.fov_y * 0.5) * self.view.distance * 2
            self.view.x += dx / self.height * plane_height
            self.view.y -= dy / self.height * plane_height
            self.view.update_matrix()

    def onWheel(self, d: int) -> None:
        ''' mouse input '''
        if d > 0:
            self.view.distance *= 1.1
            self.view.update_matrix()
        elif d < 0:
            self.view.distance *= 0.9
            self.view.update_matrix()
