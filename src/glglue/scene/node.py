from typing import List
from ..ctypesmath.mat4 import Mat4
from . import mesh


class Node:
    def __init__(self, name: str):
        self. name = name
        self.model_matrix = Mat4.new_identity()
        self.children: List['Node'] = []
        self.meshes: List[mesh.Mesh] = []

    def update(self, delta):
        pass
