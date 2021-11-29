from typing import List, Optional, Union
from .material import Material
from .vertices import Planar, Interleaved, VectorView
from glglue import ctypesmath


class Submesh:
    def __init__(self, material: Material, macro: List[str], topology: int, offset: int, draw_count: int) -> None:
        self.material = material
        self.macro = macro

        self.topology = topology
        self.offset = offset
        self.draw_count = draw_count


class Mesh:
    def __init__(self, name: str, vertices: Union[Planar, Interleaved], indices: Optional[VectorView] = None) -> None:
        self.name = name
        self.indices = indices
        self.vertices = vertices
        self.submeshes: List[Submesh] = []
        # without skinning.
        self.aabb = ctypesmath.AABB.new_empty()

    def update(self, delta):
        pass

    def add_submesh(self, material: Material, macro: List[str], topology):
        draw_count = self.vertices.count()
        if self.indices:
            draw_count = self.indices.get_count()
        self.submeshes.append(
            Submesh(material, macro, topology, 0, draw_count))

    def expand_aabb(self, aabb):
        return aabb.expand(self.aabb)
