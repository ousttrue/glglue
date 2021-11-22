'''
https://github.khronos.org/KTX-Specification/
'''
import pathlib
import struct
from typing import NamedTuple, List


class Const:
    # IDENTIFIER = bytes((0xAB,0x4B,0x54,0x58,0x20,0x32,0x30,0xBB,0x0D,0x0A,0x1A,0x0A))
    IDENTIFIER = b'\xABKTX 20\xBB\r\n\x1A\n'
    ENDIAN_COMPATIBLE = bytes((0x04, 0x03, 0x02, 0x01))
    ENDIAN_INCOMPATIBLE = bytes((0x01, 0x02, 0x03, 0x04))


class KtxError(RuntimeError):
    pass


class BytesReader:
    def __init__(self, data: bytes) -> None:
        self.data = data
        self.pos = 0

    def is_end(self) -> bool:
        return self.pos >= len(self.data)

    def get_padding_size(self, alignment: int) -> int:
        mod = self.pos % 8
        if mod == 0:
            return 0
        return alignment-mod

    def read(self, size: int) -> bytes:
        if self.pos+size > len(self.data):
            raise IOError()
        data = self.data[self.pos:self.pos+size]
        self.pos += size
        return data

    def read_int32(self) -> int:
        data = self.read(4)
        return struct.unpack('i', data)[0]

    def read_uint32(self) -> int:
        data = self.read(4)
        return struct.unpack('I', data)[0]

    def read_uint64(self) -> int:
        data = self.read(8)
        return struct.unpack('Q', data)[0]


class LevelIndex(NamedTuple):
    byteOffset: int
    byteLength: int
    uncompressedByteLength: int


class Ktx2(NamedTuple):
    vkFormat: int
    typeSize: int
    pixelWidth: int
    pixelHeight: int
    pixelDepth: int
    layerCount: int
    faceCount: int
    levelCount: int
    supercompressionScheme: int

    dfdByteOffset: int
    dfdByteLength: int
    kvdByteOffset: int
    kvdByteLength: int
    sgdByteOffset: int
    sgdByteLength: int

    levelIndices: List[LevelIndex]

    supercompressionGlobalData: bytes

    levelImages: List[bytes]


def parse_bytes(data: bytes) -> Ktx2:
    r = BytesReader(data)
    match r.read(12):
        case Const.IDENTIFIER:
            pass
        case _:
            raise KtxError('invalid identifier')

    vkFormat = r.read_uint32()
    typeSize = r.read_uint32()
    pixelWidth = r.read_uint32()
    pixelHeight = r.read_uint32()
    pixelDepth = r.read_uint32()
    layerCount = r.read_uint32()
    faceCount = r.read_uint32()
    levelCount = r.read_uint32()
    supercompressionScheme = r.read_uint32()

    # Index
    dfdByteOffset = r.read_uint32()
    dfdByteLength = r.read_uint32()
    kvdByteOffset = r.read_uint32()
    kvdByteLength = r.read_uint32()
    sgdByteOffset = r.read_uint64()
    sgdByteLength = r.read_uint64()

    # Level Index
    levelIndices = [LevelIndex(r.read_uint64(), r.read_uint64(), r.read_uint64())
                    for _ in range(levelCount)]

    # Data Format Descriptor
    # dfdTotalSize = r.read_uint32()
    # skip
    r.read(dfdByteLength)

    # Key/Value Data
    assert r.pos == kvdByteOffset
    # skip
    r.read(kvdByteLength)

    if (sgdByteLength > 0):
        padding = r.get_padding_size(8)
        # skip
        _ = r.read(padding)

    # Supercompression Global Data
    supercompressionGlobalData = r.read(sgdByteLength)

    # Mip Level Array
    if levelCount == 0:
        levelCount = 1
    levelImages = [r.read(levelIndices[i].byteLength)
                   for i in range(levelCount)]

    assert r.is_end()

    return Ktx2(
        vkFormat,
        typeSize,
        pixelWidth,
        pixelHeight,
        pixelDepth,
        layerCount,
        faceCount,
        levelCount,
        supercompressionScheme,
        dfdByteOffset,
        dfdByteLength,
        kvdByteOffset,
        kvdByteLength,
        sgdByteOffset,
        sgdByteLength,
        levelIndices,
        supercompressionGlobalData,
        levelImages)


def parse_path(path: pathlib.Path) -> Ktx2:
    return parse_bytes(path.read_bytes())
