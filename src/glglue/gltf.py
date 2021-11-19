from typing import NamedTuple, Optional, Tuple, Union, List
import struct
from enum import Enum
import json
import pathlib
from dataclasses import dataclass


class GltfError(RuntimeError):
    pass


class ElementType(Enum):
    Int8 = 5120
    UInt8 = 5121
    Int16 = 5122
    UInt16 = 5123
    UInt32 = 5125
    Float = 5126

    def get_byte_length(self):
        match self:
            case ElementType.Int8:
                return 1
            case ElementType.UInt8:
                return 1
            case ElementType.Int16:
                return 2
            case ElementType.UInt16:
                return 2
            case ElementType.UInt32:
                return 4
            case ElementType.Float:
                return 4
            case _:
                raise NotImplementedError()


TYPE_MAP = {
    'SCALAR': 1,
    'VEC2': 2,
    'VEC3': 3,
    'VEC4': 4,
    'MAT2': 4,
    'MAT3': 9,
    'MAT4': 16,
}


def get_accessor_type(gltf_accessor) -> Tuple[ElementType, int]:
    return ElementType(gltf_accessor['componentType']), TYPE_MAP[gltf_accessor['type']]


class TypedArray(NamedTuple):
    data: bytes
    element_type: ElementType
    element_count: int = 1

    def stride(self) -> int:
        return self.element_type.get_byte_length() * self.element_count

    def count(self) -> int:
        return len(self.data) // self.stride()


class GltfBufferReader:
    def __init__(self, gltf, bin: Union[None, bytes, pathlib.Path]):
        self.gltf = gltf
        match bin:
            case bytes():
                # glb
                self.bin = bin
            case pathlib.Path():
                # gltf. base path
                raise NotImplementedError()
            case None:
                # gltf only
                pass

    def _buffer_bytes(self, buffer_index: int) -> bytes:
        if self.bin and buffer_index == 0:
            # glb bin_chunk
            return self.bin

        raise NotImplementedError()

    def _buffer_view_bytes(self, buffer_view_index: int) -> bytes:
        gltf_buffer_view = self.gltf['bufferViews'][buffer_view_index]
        bin = self._buffer_bytes(gltf_buffer_view['buffer'])
        offset = gltf_buffer_view['byteOffset']
        length = gltf_buffer_view['byteLength']
        return bin[offset:offset+length]

    def read_accessor(self, accessor_index: int) -> TypedArray:
        gltf_accessor = self.gltf['accessors'][accessor_index]
        bin = self._buffer_view_bytes(gltf_accessor['bufferView'])
        offset = gltf_accessor['byteOffset']
        count = gltf_accessor['count']
        element_type, element_count = get_accessor_type(gltf_accessor)
        bin = bin[offset:offset+element_type.get_byte_length() *
                  element_count*count]
        return TypedArray(bin, element_type, element_count)


@dataclass
class GltfTexture:
    name: str


@dataclass
class GltfMaterial:
    name: str


@dataclass
class GltfPrimitive:
    '''
    https://github.com/KhronosGroup/glTF/blob/main/specification/2.0/schema/mesh.primitive.schema.json
    '''
    position: TypedArray
    normal: Optional[TypedArray] = None
    indices: Optional[TypedArray] = None


@dataclass
class GltfMesh:
    name: str
    primitives: List[GltfPrimitive]


@dataclass
class GltfNode:
    name: str


class GltfData:
    def __init__(self, gltf):
        self.gltf = gltf
        self.textures: List[GltfTexture] = []
        self.materials: List[GltfMaterial] = []
        self.meshes: List[GltfMesh] = []
        self.nodes: List[GltfNode] = []

    def __str__(self) -> str:
        return f'{len(self.materials)} materials, {len(self.meshes)} meshes, {len(self.nodes)} nodes'

    def _parse_material(self, i: int, gltf_material) -> GltfMaterial:
        return GltfMaterial(gltf_material.get('name', f'{i}'))

    def _parse_mesh(self, buffer_reader: GltfBufferReader, i: int, gltf_mesh) -> GltfMesh:
        mesh = GltfMesh(gltf_mesh.get('name', f'{i}'), [])

        for gltf_prim in gltf_mesh['primitives']:
            gltf_attributes = gltf_prim['attributes']

            match gltf_attributes['POSITION']:
                case int() as accessor:
                    positions = buffer_reader.read_accessor(accessor)
                case _:
                    raise GltfError()

            prim = GltfPrimitive(positions)

            match gltf_attributes.get('NORMAL'):
                case int() as accessor:
                    prim.normal = buffer_reader.read_accessor(accessor)

            match gltf_prim.get('indices'):
                case int() as accessor:
                    prim.indices = buffer_reader.read_accessor(accessor)

            mesh.primitives.append(prim)

        return mesh

    def _parse_node(self, i: int, gltf_node) -> GltfNode:
        return GltfNode(gltf_node.get('name', f'{i}'))

    def parse(self, buffer_reader: GltfBufferReader):
        # texture
        for gltf_texture in self.gltf.get('textures', []):
            print(gltf_texture)

        # material
        maetrials = self.gltf.get('materials')
        if maetrials:
            for i, gltf_material in enumerate(maetrials):
                material = self._parse_material(i, gltf_material)
                self.materials.append(material)
        else:
            NotImplementedError('no material')

        # mesh
        for i, gltf_mesh in enumerate(self.gltf.get('meshes', [])):
            mesh = self._parse_mesh(buffer_reader, i, gltf_mesh)
            self.meshes.append(mesh)

        # node
        for i, gltf_node in enumerate(self.gltf.get('nodes', [])):
            node = self._parse_node(i, gltf_node)
            self.nodes.append(node)

        # skinning
        for i, gltf_skin in enumerate(self.gltf.get('skins', [])):
            pass


def parse_gltf(json_chunk: bytes, bin: Union[None, bytes, pathlib.Path]) -> GltfData:
    gltf = json.loads(json_chunk)
    data = GltfData(gltf)
    buffer_reader = GltfBufferReader(gltf, bin)
    data.parse(buffer_reader)

    return data


class GlbError(RuntimeError):
    pass


class BytesReader:
    def __init__(self, data: bytes):
        self.data = data
        self.pos = 0

    def is_end(self) -> bool:
        return self.pos >= len(self.data)

    def read(self, size: int) -> bytes:
        if (self.pos + size) > len(self.data):
            raise IOError()
        data = self.data[self.pos:self.pos+size]
        self.pos += size
        return data

    def read_int(self) -> int:
        data = self.read(4)
        return struct.unpack('i', data)[0]


def parse_glb(data: bytes) -> Tuple[Optional[bytes], Optional[bytes]]:
    '''
    https://www.khronos.org/registry/glTF/specs/2.0/glTF-2.0.html#glb-file-format-specification
    '''
    r = BytesReader(data)
    if r.read_int() != 0x46546C67:
        raise GlbError('invalid magic')

    version = r.read_int()
    if version != 2:
        raise GlbError(f'unknown version: {version}')

    length = r.read_int()

    json_chunk = None
    bin_chunk = None
    while r.pos < length:
        chunk_length = r.read_int()
        chunk_type = r.read_int()
        chunk_data = r.read(chunk_length)
        match chunk_type:
            case 0x4E4F534A:
                json_chunk = chunk_data
            case 0x004E4942:
                bin_chunk = chunk_data
            case _:
                raise NotImplementedError(f'unknown chunk: {chunk_type}')

    return json_chunk, bin_chunk
