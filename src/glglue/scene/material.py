from typing import Optional
from typing import Optional
from .texture import Texture, CubeMap


class Material:
    def __init__(self, name: str, vs: str, fs: str) -> None:
        self.name = name
        self.vs = vs
        self.fs = fs
        self.color_texture: Optional[Texture] = None
        self.cubemap: Optional[CubeMap] = None
