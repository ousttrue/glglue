from typing import NamedTuple
import io
from PIL import Image


class Image32(NamedTuple):
    data: bytes
    width: int
    height: int

    @staticmethod
    def load(data: bytes) -> 'Image32':
        image = Image.open(io.BytesIO(data))
        if image.mode != 'RGBA':
            image = image.convert('RGBA')
        return Image32(image.getdata(), image.width, image.height)


class Texture:
    def __init__(self, name: str, image: Image32) -> None:
        self.name = name
        self.image = image
