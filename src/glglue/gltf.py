'''
https://github.com/KhronosGroup/glTF/blob/main/specification/2.0/
'''
from ctypes.wintypes import RGB
from typing import NamedTuple, Optional, Tuple, List, Dict, Any, Type
import struct
import ctypes
from enum import Enum
import json
import pathlib
from dataclasses import dataclass


class GltfError(RuntimeError):
    pass


COMPONENT_TYPE_TO_ELEMENT_TYPE = {
    5120: ctypes.c_char,
    5121: ctypes.c_byte,
    5122: ctypes.c_short,
    5123: ctypes.c_ushort,
    5125: ctypes.c_uint,
    5126: ctypes.c_float,
}

TYPE_TO_ELEMENT_COUNT = {
    'SCALAR': 1,
    'VEC2': 2,
    'VEC3': 3,
    'VEC4': 4,
    'MAT2': 4,
    'MAT3': 9,
    'MAT4': 16,
}


class MimeType(Enum):
    Jpg = "image/jpeg"
    Png = "image/png"

    @staticmethod
    def from_name(name: str):
        match pathlib.Path(name).suffix.lower():
            case ".png":
                return MimeType.Png
            case ".jpg":
                return MimeType.Jpg
            case _:
                raise GltfError(f'unknown image: {name}')


def get_accessor_type(gltf_accessor) -> Tuple[Type[ctypes._SimpleCData], int]:
    return COMPONENT_TYPE_TO_ELEMENT_TYPE[gltf_accessor['componentType']], TYPE_TO_ELEMENT_COUNT[gltf_accessor['type']]


class TypedBytes(NamedTuple):
    data: bytes
    element_type: Type[ctypes._SimpleCData]
    element_count: int = 1

    def stride(self) -> int:
        return ctypes.sizeof(self.element_type) * self.element_count

    def count(self) -> int:
        return len(self.data) // self.stride()


class GltfBufferReader:
    def __init__(self, gltf, path: Optional[pathlib.Path], bin: Optional[bytes]):
        self.gltf = gltf
        self.bin = bin
        self.path = path
        self.uri_cache: Dict[str, bytes] = {}

    def uri_bytes(self, uri: str) -> bytes:
        data = self.uri_cache.get(uri)
        if not data:
            if self.path:
                path = self.path.parent / uri
                data = path.read_bytes()
            else:
                raise NotImplementedError()
        self.uri_cache[uri] = data
        return data

    def _buffer_bytes(self, buffer_index: int) -> bytes:
        if self.bin and buffer_index == 0:
            # glb bin_chunk
            return self.bin

        gltf_buffer = self.gltf['buffers'][buffer_index]
        uri = gltf_buffer['uri']
        if not isinstance(uri, str):
            raise GltfError()

        return self.uri_bytes(uri)

    def buffer_view_bytes(self, buffer_view_index: int) -> bytes:
        gltf_buffer_view = self.gltf['bufferViews'][buffer_view_index]
        bin = self._buffer_bytes(gltf_buffer_view['buffer'])
        offset = gltf_buffer_view.get('byteOffset', 0)
        length = gltf_buffer_view['byteLength']
        return bin[offset:offset+length]

    def read_accessor(self, accessor_index: int) -> TypedBytes:
        gltf_accessor = self.gltf['accessors'][accessor_index]
        bin = self.buffer_view_bytes(gltf_accessor['bufferView'])
        offset = gltf_accessor.get('byteOffset', 0)
        count = gltf_accessor['count']
        element_type, element_count = get_accessor_type(gltf_accessor)
        bin = bin[offset:offset+ctypes.sizeof(element_type) *
                  element_count*count]
        return TypedBytes(bin, element_type, element_count)


@dataclass
class GltfImage:
    name: str
    data: bytes
    mime: MimeType


@dataclass
class GltfTexture:
    name: str
    image: GltfImage


class RGBA(NamedTuple):
    r: float
    g: float
    b: float
    a: float


class GltfMaterial(NamedTuple):
    name: str
    base_color_texture: Optional[GltfTexture]
    base_color_factor: RGBA
    metallic_factor: float


class GltfPrimitive(NamedTuple):
    material: GltfMaterial
    position: TypedBytes
    normal: Optional[TypedBytes]
    uv: Optional[TypedBytes]
    indices: Optional[TypedBytes]


class GltfMesh(NamedTuple):
    name: str
    primitives: Tuple[GltfPrimitive, ...]


@dataclass
class GltfNode:
    name: str
    children: List['GltfNode']
    mesh: Optional[GltfMesh]


class GltfData:
    def __init__(self, gltf):
        self.gltf = gltf
        self.images: List[GltfImage] = []
        self.textures: List[GltfTexture] = []
        self.materials: List[GltfMaterial] = []
        self.meshes: List[GltfMesh] = []
        self.nodes: List[GltfNode] = []
        self.scene: List[GltfNode] = []

    def __str__(self) -> str:
        return f'{len(self.materials)} materials, {len(self.meshes)} meshes, {len(self.nodes)} nodes'

    def _parse_image(self, buffer_reader: GltfBufferReader, i: int, gltf_image) -> GltfImage:
        name = gltf_image.get('name')
        match gltf_image:
            case {'bufferView': buffer_view_index, 'mimeType': mime}:
                return GltfImage(name or f'{i}', buffer_reader.buffer_view_bytes(buffer_view_index), MimeType(mime))
            case {'uri': uri}:
                if uri.startswith('data:'):
                    raise NotImplementedError()
                else:
                    return GltfImage(uri, buffer_reader.uri_bytes(uri), MimeType.from_name(uri))
            case _:
                raise GltfError()

    def _parse_texture(self, i: int, gltf_texture) -> GltfTexture:
        texture = GltfTexture(gltf_texture.get(
            'name', f'{i}'), self.images[gltf_texture['source']])
        return texture

    def _parse_material(self, i: int, gltf_material) -> GltfMaterial:
        pbr = gltf_material.get('pbrMetallicRoughness')
        base_color_texture = None
        base_color_factor = RGBA(1, 1, 1, 1)
        metallic_factor = 0.0
        if pbr:
            match gltf_material.get('baseColorTexture'):
                case int() as texture_index:
                    base_color_texture = self.textures[texture_index]
            base_color_factor = RGBA(*pbr.get(
                'baseColorFactor', [1, 1, 1, 1]))
            metallic_factor = pbr.get('metallicFactor', 0.0)

        material = GltfMaterial(gltf_material.get(
            'name', f'{i}'), base_color_texture, base_color_factor, metallic_factor)
        return material

    def _parse_mesh(self, buffer_reader: GltfBufferReader, i: int, gltf_mesh) -> GltfMesh:
        primitives = []
        for gltf_prim in gltf_mesh['primitives']:
            gltf_attributes = gltf_prim['attributes']

            match gltf_attributes['POSITION']:
                case int() as accessor:
                    positions = buffer_reader.read_accessor(accessor)
                case _:
                    raise GltfError()

            normal = None
            match gltf_attributes.get('NORMAL'):
                case int() as accessor:
                    normal = buffer_reader.read_accessor(accessor)

            uv = None
            match gltf_attributes.get('TEXCOORD_0'):
                case int() as accessor:
                    uv = buffer_reader.read_accessor(accessor)

            indices = None
            match gltf_prim.get('indices'):
                case int() as accessor:
                    indices = buffer_reader.read_accessor(accessor)

            prim = GltfPrimitive(
                self.materials[gltf_prim['material']], positions, normal, uv, indices)
            primitives.append(prim)

        mesh = GltfMesh(gltf_mesh.get('name', f'{i}'), tuple(primitives))
        return mesh

    def _parse_node(self, i: int, gltf_node) -> GltfNode:
        node = GltfNode(gltf_node.get('name', f'{i}'), [], None)
        match gltf_node.get('mesh'):
            case int() as mesh_index:
                node.mesh = self.meshes[mesh_index]
        return node

    def parse(self, buffer_reader: GltfBufferReader):
        # image
        for i, gltf_image in enumerate(self.gltf.get('images', [])):
            image = self._parse_image(buffer_reader, i, gltf_image)
            self.images.append(image)

        # texture
        for i, gltf_texture in enumerate(self.gltf.get('textures', [])):
            texture = self._parse_texture(i, gltf_texture)
            self.textures.append(texture)

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
        for i, gltf_node in enumerate(self.gltf.get('nodes', [])):
            match gltf_node.get('children'):
                case [*children]:
                    for child_index in children:
                        self.nodes[i].children.append(self.nodes[child_index])

        # skinning
        for i, gltf_skin in enumerate(self.gltf.get('skins', [])):
            pass

        # scene
        self.scene += [self.nodes[node_index]
                       for node_index in self.gltf['scenes'][self.gltf['scene']]['nodes']]


def parse_gltf(json_chunk: bytes, *, path: Optional[pathlib.Path] = None, bin: Optional[bytes] = None) -> GltfData:
    gltf = json.loads(json_chunk)
    data = GltfData(gltf)
    buffer_reader = GltfBufferReader(gltf, path, bin)
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


def parse_path(path: pathlib.Path) -> GltfData:
    data = path.read_bytes()
    try:
        # first, try glb
        json, bin = parse_glb(data)
        if json and bin:
            return parse_gltf(json, path=path, bin=bin)
    except GlbError:
        pass

    # fallback to gltf
    return parse_gltf(data, path=path)
