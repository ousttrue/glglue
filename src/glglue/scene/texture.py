from typing import NamedTuple
import io
from PIL import Image
import logging
logging.getLogger('PIL').setLevel(logging.WARNING)


class Image32(NamedTuple):
    data: bytes
    width: int
    height: int

    @staticmethod
    def load(src: bytes) -> 'Image32':
        image = Image.open(io.BytesIO(src))
        if image.mode != 'RGBA':
            image = image.convert('RGBA')
        data = image.tobytes('raw')
        return Image32(data, image.width, image.height)


class Texture:
    def __init__(self, name: str, image: Image32) -> None:
        self.name = name
        self.image = image


class CubeMap(NamedTuple):
    xp: Image32
    xn: Image32
    yp: Image32
    yn: Image32
    zp: Image32
    zn: Image32
