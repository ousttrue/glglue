from typing import NamedTuple, Optional
import math
from .float3 import Float3

kEpsilon = 1e-5


class Ray(NamedTuple):
    origin: Float3
    dir: Float3

    def intersect(self, v0: Float3, v1: Float3, v2: Float3) -> Optional[float]:
        '''
        https://www.scratchapixel.com/lessons/3d-basic-rendering/ray-tracing-rendering-a-triangle/ray-triangle-intersection-geometric-solution
        '''
        # compute plane's normal
        v0v1 = v1 - v0
        v0v2 = v2 - v0
        # no need to normalize
        N = Float3.cross(v0v1, v0v2)  # N
        # area2 = N.get_length()

        # Step 1: finding P

        # check if ray and plane are parallel ?
        NdotRayDirection = Float3.dot(N, self.dir)
        if math.fabs(NdotRayDirection) < kEpsilon:  # almost 0
            return  # they are parallel so they don't intersect !

        # compute d parameter using equation 2
        d = -Float3.dot(N, v0)

        # compute t (equation 3)
        t = -(Float3.dot(N, self.origin) + d) / NdotRayDirection
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
        C = Float3.cross(edge0, vp0)
        if Float3.dot(N, C) < 0:
            return  # P is on the right side

        # edge 1
        edge1 = v2 - v1
        vp1 = P - v1
        C = Float3.cross(edge1, vp1)
        if Float3.dot(N, C) < 0:
            return  # P is on the right side

        # edge 2
        edge2 = v0 - v2
        vp2 = P - v2
        C = Float3.cross(edge2, vp2)
        if Float3.dot(N, C) < 0:
            return  # P is on the right side

        return t  # this ray hits the triangle
