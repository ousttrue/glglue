from typing import Optional
from .texture import Texture, CubeMap


class Material:
    def __init__(self, name: str, vs: str, fs: str) -> None:
        self.name = name
        self.vs = vs
        self.fs = fs
        self.color_texture: Optional[Texture] = None
        self.cubemap: Optional[CubeMap] = None

    @staticmethod
    def from_assets(name: str) -> 'Material':
        import pkgutil
        vs = pkgutil.get_data('glglue', f'assets/{name}.vs')
        if not vs:
            raise Exception()
        fs = pkgutil.get_data('glglue', f'assets/{name}.fs')
        if not fs:
            raise Exception()
        return Material(name, vs.decode('utf-8'), fs.decode('utf-8'))
