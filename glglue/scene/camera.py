from typing import NamedTuple, Optional
import math
import logging
import glm
from glglue.scene.mouse_event import DragInterface
from glglue.frame_input import FrameInput

LOGGER = logging.getLogger(__name__)


kEpsilon = 1e-5


class Ray(NamedTuple):
    origin: glm.vec3
    dir: glm.vec3

    def intersect_triangle(
        self, v0: glm.vec3, v1: glm.vec3, v2: glm.vec3
    ) -> Optional[float]:
        """
        https://www.scratchapixel.com/lessons/3d-basic-rendering/ray-tracing-rendering-a-triangle/ray-triangle-intersection-geometric-solution
        """
        # compute plane's normal
        v0v1 = v1 - v0
        v0v2 = v2 - v0
        # no need to normalize
        N = glm.cross(v0v1, v0v2)  # N
        # area2 = N.get_length()

        # Step 1: finding P

        # check if ray and plane are parallel ?
        NdotRayDirection = glm.dot(N, self.dir)
        if math.fabs(NdotRayDirection) < kEpsilon:  # almost 0
            return  # they are parallel so they don't intersect !

        # compute d parameter using equation 2
        d = -glm.dot(N, v0)

        # compute t (equation 3)
        t = -(glm.dot(N, self.origin) + d) / NdotRayDirection
        # check if the triangle is in behind the ray
        if t < 0:
            return  # the triangle is behind

        # compute the intersection point using equation 1
        P = self.origin + self.dir * t

        # Step 2: inside-outside test
        # Vec3f C  # vector perpendicular to triangle's plane

        # edge 0
        edge0 = v1 - v0
        vp0 = P - v0
        C = glm.cross(edge0, vp0)
        if glm.dot(N, C) < 0:
            return  # P is on the right side

        # edge 1
        edge1 = v2 - v1
        vp1 = P - v1
        C = glm.cross(edge1, vp1)
        if glm.dot(N, C) < 0:
            return  # P is on the right side

        # edge 2
        edge2 = v0 - v2
        vp2 = P - v2
        C = glm.cross(edge2, vp2)
        if glm.dot(N, C) < 0:
            return  # P is on the right side

        return t  # this ray hits the triangle


class Perspective:
    def __init__(self, *, near=0.1, far=1000) -> None:
        self.matrix = glm.mat4(1.0)
        self.fov_y = math.pi * 30 / 180
        self.aspect = 1.0
        self.z_near = near
        self.z_far = far
        self.width = 1
        self.height = 1
        self.update_matrix()

    def update_matrix(self) -> None:
        self.matrix = glm.perspectiveRH(
            self.fov_y, self.aspect, self.z_near, self.z_far
        )

    def resize(self, w: int, h: int) -> bool:
        if self.width == w and self.height == h:
            return False
        self.width = w
        self.height = h
        self.aspect = float(w) / h
        self.update_matrix()
        return True


class View:
    def __init__(self, y=0, distance=5) -> None:
        self.gaze = glm.vec3(0, 0, 0)
        self.rotation = glm.quat()
        self.shift = glm.vec3(0, y, -distance)
        self.update_matrix()

    def update_matrix(self):
        g = glm.translate(-self.gaze)
        t = glm.translate(self.shift)
        r = glm.mat4(self.rotation)  # type: ignore
        self.matrix = t * r * g
        self.inverse = glm.inverse(self.matrix)

    def set_gaze(self, gaze: glm.vec3):
        self.gaze = gaze
        # self.matrix = t * r * g
        g = glm.translate(-self.gaze)
        # t = glm.translate(self.shift)
        r = glm.mat4(self.rotation)  # type: ignore
        t = self.matrix * glm.inverse(r * g)
        self.shift = t[3].xyz
        self.update_matrix()


class ScreenShift(DragInterface):
    def __init__(self, view: View, projection: Perspective) -> None:
        self.view = view
        self.projection = projection

    def reset(self, shift: glm.vec3):
        self.view.shift = shift
        self.update()

    def update(self) -> None:
        self.view.update_matrix()

    def begin(self, mouse_input: FrameInput):
        pass

    def drag(self, mouse_input: FrameInput, dx: int, dy: int):
        plane_height = math.tan(self.projection.fov_y * 0.5) * self.view.shift.z * 2
        self.view.shift.x -= dx / self.projection.height * plane_height
        self.view.shift.y += dy / self.projection.height * plane_height
        self.update()

    def end(self, mouse_input: FrameInput):
        pass

    def wheel(self, d: int):
        if d < 0:
            self.view.shift.z *= 1.1
            self.update()
        elif d > 0:
            self.view.shift.z *= 0.9
            self.update()


class TurnTable(DragInterface):
    def __init__(self, view: View) -> None:
        self.view = view
        self.yaw = 0.0
        self.pitch = 0.0
        self.update()

    def update(self) -> None:
        yaw = glm.angleAxis(self.yaw, glm.vec3(0, 1, 0))
        pitch = glm.angleAxis(self.pitch, glm.vec3(1, 0, 0))
        self.view.rotation = pitch * yaw
        self.view.update_matrix()

    def begin(self, mouse_input: FrameInput):
        pass

    def drag(self, mouse_input: FrameInput, dx: int, dy: int):
        self.yaw += dx * 0.01
        self.pitch += dy * 0.01
        self.update()

    def end(self, mouse_input: FrameInput):
        pass


def get_arcball_vector(mouse_input: FrameInput):
    """
    https://en.wikibooks.org/wiki/OpenGL_Programming/Modern_OpenGL_Tutorial_Arcball
    """
    P = glm.vec3(
        mouse_input.mouse_x / mouse_input.width * 2 - 1.0,
        mouse_input.mouse_y / mouse_input.height * 2 - 1.0,
        0,
    )
    P.y = -P.y
    OP_squared = P.x * P.x + P.y * P.y
    if OP_squared <= 1:
        P.z = math.sqrt(1 - OP_squared)  # Pythagoras
    else:
        P = glm.normalize(P)  # nearest point
    return P


class ArcBall(DragInterface):
    def __init__(self, view: View, projection: Perspective) -> None:
        self.view = view
        self.projection = projection
        self.rotation = glm.quat()
        self.tmp_rotation = glm.quat()
        self.x = None
        self.y = None
        self.va = None

    def update(self) -> None:
        self.view.rotation = glm.normalize(self.tmp_rotation * self.rotation)
        self.view.update_matrix()

    def begin(self, mouse_input: FrameInput):
        x = mouse_input.mouse_x
        y = mouse_input.mouse_y
        self.rotation = self.view.rotation
        self.x = x
        self.y = y
        self.va = get_arcball_vector(mouse_input)

    def drag(self, mouse_input: FrameInput, dx: int, dy: int):
        x = mouse_input.mouse_x
        y = mouse_input.mouse_y
        if x == self.x and y == self.y:
            return
        self.x = x
        self.y = y
        vb = get_arcball_vector(mouse_input)
        angle = math.acos(min(1.0, glm.dot(self.va, vb))) * 2  # type: ignore
        axis = glm.cross(self.va, vb)  # type: ignore
        self.tmp_rotation = glm.angleAxis(angle, axis)
        self.update()

    def end(self, mouse_input: FrameInput):
        x = mouse_input.mouse_x
        y = mouse_input.mouse_y
        self.rotation = glm.normalize(self.tmp_rotation * self.rotation)
        self.tmp_rotation = glm.quat()
        self.update()


class Camera:
    def __init__(self, *, near=0.01, far=1000, distance: float = 5, y: float = 0):
        self.projection = Perspective(near=near, far=far)
        self.view = View(y=y, distance=distance)  # type: ignore

    def get_mouse_ray(self, x: int, y: int) -> Ray:
        return get_mouse_ray(
            x,
            y,
            self.projection.width,
            self.projection.height,
            self.view.inverse,
            self.projection.fov_y,
            self.projection.aspect,
        )


def get_mouse_ray(
    x: int, y: int, w: int, h: int, view_inverse: glm.mat4, fov_y: float, aspect: float
) -> Ray:
    origin = view_inverse[3].xyz
    half_fov = fov_y / 2
    dir = view_inverse * glm.vec4(
        (x / w * 2 - 1) * math.tan(half_fov) * (aspect),
        -(y / h * 2 - 1) * math.tan(half_fov),
        -1,
        0,
    )
    return Ray(origin, glm.normalize(dir.xyz))
