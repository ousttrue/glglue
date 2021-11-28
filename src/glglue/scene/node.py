from typing import List, Union
from ..ctypesmath import *
from . import mesh


class Node:
    def __init__(self, name: str, transform: Union[TRS, Mat4]):
        self. name = name
        self.transform = transform
        self.children: List['Node'] = []
        self.meshes: List[mesh.Mesh] = []

    def update(self, delta):
        pass

    def get_local_matrix(self) -> Mat4:
        match self.transform:
            case Mat4() as m:
                return m
            case TRS() as trs:
                return trs.to_matrix()
            case _:
                raise RuntimeError()
