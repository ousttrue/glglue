from typing import List, Any
from .vertices import VectorView


class Skin:
    def __init__(self, joints: List[Any], inverse_bind_matrices: VectorView) -> None:
        from .node import Node
        self.joints: List[Node] = joints
        self.bind_matrices = inverse_bind_matrices
