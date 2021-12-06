import math
import logging
from typing import NamedTuple
from .mat4 import Mat4, Float4
from .float3 import Float3
from .hittest import Ray
logger = logging.getLogger(__name__)


class Perspective:
    def __init__(self) -> None:
        self.matrix = Mat4.new_identity()
        self.fov_y = math.pi * 30 / 180
        self.aspect = 1.0
        self.z_near = 0.1
        self.z_far = 1000
        self.update_matrix()

    def update_matrix(self) -> None:
        self.matrix.perspective(self.fov_y, self.aspect, self.z_near,
                                self.z_far)


class Orbit:
    def __init__(self) -> None:
        self.matrix = Mat4.new_identity()
        self.inverse = Mat4.new_identity()
        self.x = 0.0
        self.y = 0.0
        self.distance = 2.0
        self.yaw = 0.0
        self.pitch = 0.0
        self.update_matrix()

    def __str__(self) -> str:
        return f'({self.x:.3f}, {self.y:.3f}, {self.distance:.3f})'

    def update_matrix(self) -> None:
        t = Mat4.new_translation(self.x, self.y, -self.distance)
        yaw = Mat4.new_rotation_y(self.yaw)
        pitch = Mat4.new_rotation_x(self.pitch)
        self.matrix = yaw * pitch * t
        self.inverse = self.matrix.inverse_rigidbody()


class FrameState(NamedTuple):
    '''
    RenderInfo for frame
    '''
    viewport: Float4
    mouse_x: int
    mouse_y: int
    mouse_left_down: bool
    mouse_right_down: bool
    mouse_middle_down: bool
    camera_view: Mat4
    camera_projection: Mat4
    ray: Ray


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

    def onResize(self, w: int, h: int) -> bool:
        if self.width == w and self.height == h:
            return False
        self.width = w
        self.height = h
        self.projection.aspect = float(w) / h
        self.projection.update_matrix()
        return True

    def onLeftDown(self, x: int, y: int) -> bool:
        ''' 
        Mouse input. Returns whether redraw is required.
        '''
        if self.left:
            return False
        self.left = True
        self.x = x
        self.y = y
        return False

    def onLeftUp(self, x: int, y: int) -> bool:
        ''' 
        Mouse input. Returns whether redraw is required.
        '''
        self.left = False
        return False

    def onMiddleDown(self, x: int, y: int) -> bool:
        ''' 
        Mouse input. Returns whether redraw is required.
        '''
        if self.middle:
            return False
        self.middle = True
        self.x = x
        self.y = y
        return False

    def onMiddleUp(self, x: int, y: int) -> bool:
        ''' 
        Mouse input. Returns whether redraw is required.
        '''
        self.middle = False
        return False

    def onRightDown(self, x: int, y: int) -> bool:
        ''' 
        Mouse input. Returns whether redraw is required.
        '''
        if self.right:
            return False
        self.right = True
        self.x = x
        self.y = y
        return False

    def onRightUp(self, x: int, y: int) -> bool:
        ''' 
        Mouse input. Returns whether redraw is required.
        '''
        self.right = False
        return False

    def onMotion(self, x: int, y: int) -> bool:
        ''' 
        Mouse input. Returns whether redraw is required.
        '''
        dx = x - self.x
        self.x = x
        dy = y - self.y
        self.y = y

        redraw_is_required = False
        if self.right:
            self.view.yaw += dx * 0.01
            self.view.pitch += dy * 0.01
            self.view.update_matrix()
            redraw_is_required = True

        if self.middle:
            plane_height = math.tan(
                self.projection.fov_y * 0.5) * self.view.distance * 2
            self.view.x += dx / self.height * plane_height
            self.view.y -= dy / self.height * plane_height
            self.view.update_matrix()
            redraw_is_required = True

        return redraw_is_required

    def onWheel(self, d: int) -> bool:
        ''' 
        Mouse input. Returns whether redraw is required.
        '''
        if d > 0:
            self.view.distance *= 1.1
            self.view.update_matrix()
            return True
        elif d < 0:
            self.view.distance *= 0.9
            self.view.update_matrix()
            return True
        return False

    def fit(self, p0: Float3, p1: Float3):
        if math.isnan(p0.x) or math.isnan(p0.y) or math.isnan(p0.z) or math.isnan(p1.x) or math.isnan(p1.y) or math.isnan(p1.z):
            return
        if math.isinf(p0.x) or math.isinf(p0.y) or math.isinf(p0.z) or math.isinf(p1.x) or math.isinf(p1.y) or math.isinf(p1.z):
            return

        self.view.x = 0
        self.view.y = -(p1.y+p0.y)/2
        self.view.distance = (p1.y-p0.y) / \
            math.tan(self.projection.fov_y / 2)
        self.view.yaw = 0
        self.view.pitch = 0
        self.view.update_matrix()
        logger.info(self.view)

        if self.view.distance*2 > self.projection.z_far:
            self.projection.z_far = self.view.distance*2
            self.projection.update_matrix()

    def get_mouse_ray(self):
        origin = Float3(
            self.view.inverse._41,
            self.view.inverse._42,
            self.view.inverse._43)
        half_fov = self.projection.fov_y/2
        dir = Float3(
            (self.x/self.width * 2 - 1) *
            math.tan(half_fov) * (self.projection.aspect),
            -(self.y/self.height * 2 - 1) * math.tan(half_fov),
            -1)
        dir = self.view.inverse.apply(*dir, translate=False)

        return Ray(origin, dir.normalized())

    def get_state(self) -> FrameState:
        ray = self.get_mouse_ray()
        return FrameState(
            Float4(0, 0, self.width, self.height),
            self.x, self.y,
            self.left, self.right, self.middle,
            self.view.matrix, self.projection.matrix,
            ray
        )
