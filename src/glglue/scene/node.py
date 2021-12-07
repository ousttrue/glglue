from typing import List, Optional, Union
from ..ctypesmath import *
from . import mesh


class Node:
    def __init__(self, name: str, transform: Union[TRS, Mat4]):
        self. name = name
        self.local_transform = transform
        self.world_matrix = Mat4.new_identity()
        self.children: List['Node'] = []
        self.meshes: List[mesh.Mesh] = []

    def update(self, delta):
        pass

    def get_local_matrix(self) -> Mat4:
        match self.local_transform:
            case Mat4() as m:
                return m
            case TRS() as trs:
                return trs.to_matrix()
            case _:
                raise RuntimeError()

    def expand_aabb(self, aabb: AABB, parent: Optional[Mat4] = None) -> AABB:
        if not parent:
            parent = Mat4.new_identity()
        m = self.get_local_matrix() * parent

        if self.meshes:
            local_aabb = AABB.new_empty()
            for mesh in self.meshes:
                local_aabb = local_aabb.expand(mesh.aabb)
            world_aabb = local_aabb.transform(m)
            aabb = aabb.expand(world_aabb)

        for child in self.children:
            aabb = child.expand_aabb(aabb, m)

        return aabb

    def calc_world(self, parent: Optional[Mat4] = None):
        if parent:
            self.world_matrix = self.get_local_matrix() * parent
        else:
            self.world_matrix = self.get_local_matrix()
        for child in self.children:
            child.calc_world(self.world_matrix)
