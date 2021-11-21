'''
https://github.com/KhronosGroup/glTF/blob/main/specification/2.0/
'''
from ctypes.wintypes import RGB
from typing import NamedTuple, Optional, Tuple, List, Dict, Any, Type
import struct
import ctypes
import re
from enum import Enum
import json
import pathlib
from dataclasses import dataclass

from OpenGL.error import Error


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
    Ktx2 = "image/ktx2"

    @staticmethod
    def from_name(name: str):
        match pathlib.Path(name).suffix.lower():
            case ".png":
                return MimeType.Png
            case ".jpg":
                return MimeType.Jpg
            case ".ktx2":
                return MimeType.Ktx2
            case _:
                raise GltfError(f'unknown image: {name}')


def get_accessor_type(gltf_accessor) -> Tuple[Type[ctypes._SimpleCData], int]:
    return COMPONENT_TYPE_TO_ELEMENT_TYPE[gltf_accessor['componentType']], TYPE_TO_ELEMENT_COUNT[gltf_accessor['type']]


CTYPES_FORMAT_MAP: Dict[Type[ctypes._SimpleCData], str] = {
    ctypes.c_byte: 'b',
    ctypes.c_ubyte: 'B',
    ctypes.c_short: 'h',
    ctypes.c_ushort: 'H',
    ctypes.c_uint: 'I',
    ctypes.c_float: 'f',
}


class TypedBytes(NamedTuple):
    data: bytes
    element_type: Type[ctypes._SimpleCData]
    element_count: int = 1

    def get_stride(self) -> int:
        return ctypes.sizeof(self.element_type) * self.element_count

    def get_count(self) -> int:
        return len(self.data) // self.get_stride()

    def get_item(self, i: int):
        begin = i * self.element_count
        return memoryview(self.data).cast(CTYPES_FORMAT_MAP[self.element_type])[begin:begin+self.element_count]


DATA_URI = re.compile(r'^data:([^;]*);base64,(.*)')


class GltfBufferReader:
    def __init__(self, gltf, path: Optional[pathlib.Path], bin: Optional[bytes]):
        self.gltf = gltf
        self.bin = bin
        self.path = path
        self.uri_cache: Dict[str, bytes] = {}

    def uri_bytes(self, uri: str) -> bytes:
        data = self.uri_cache.get(uri)
        if not data:
            if uri.startswith('data:'):
                m = DATA_URI.match(uri)
                if not m:
                    raise RuntimeError()
                import base64
                data = base64.urlsafe_b64decode(m[2])
            elif self.path:
                import urllib.parse
                path = self.path.parent / urllib.parse.unquote(uri)
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
        buffer_view_index = gltf_accessor.get('bufferView')
        offset = gltf_accessor.get('byteOffset', 0)
        count = gltf_accessor['count']
        element_type, element_count = get_accessor_type(gltf_accessor)
        length = ctypes.sizeof(element_type) * element_count*count
        if buffer_view_index:
            bin = self.buffer_view_bytes(buffer_view_index)
            bin = bin[offset:offset+length]
            return TypedBytes(bin, element_type, element_count)
        else:
            # zefo filled
            return TypedBytes(b'\0' * length, element_type, element_count)


class GltfImage(NamedTuple):
    name: str
    data: bytes
    mime: MimeType


class GltfTexture(NamedTuple):
    name: str
    image: GltfImage


class RGB(NamedTuple):
    r: float
    g: float
    b: float


class RGBA(NamedTuple):
    r: float
    g: float
    b: float
    a: float


class AlphaMode(Enum):
    OPAQUE = 'OPAQUE'
    MASK = 'MASK'
    BLEND = 'BLEND'


class GltfMaterial(NamedTuple):
    name: str
    base_color_texture: Optional[GltfTexture]
    base_color_factor: RGBA
    metallic_roughness_texture: Optional[GltfTexture]
    metallic_factor: float
    roughness_factor: float
    emissive_texture: Optional[GltfTexture]
    emissive_factor: RGB
    normal_texture: Optional[GltfTexture]
    occlusion_texture: Optional[GltfTexture]
    alpha_mode: AlphaMode
    alpha_cutoff: float
    double_sided: bool

    @staticmethod
    def default() -> 'GltfMaterial':
        return GltfMaterial('__default__', None, RGBA(1, 1, 1, 1), None, 0, 1, None, RGB(0, 0, 0), None, None, AlphaMode.OPAQUE, 0.5, False)


class GltfPrimitive(NamedTuple):
    material: GltfMaterial
    position: TypedBytes
    normal: Optional[TypedBytes]
    uv0: Optional[TypedBytes]
    uv1: Optional[TypedBytes]
    uv2: Optional[TypedBytes]
    tangent: Optional[TypedBytes]
    color: Optional[TypedBytes]
    joints: Optional[TypedBytes]
    weights: Optional[TypedBytes]
    indices: Optional[TypedBytes]


class GltfMesh(NamedTuple):
    name: str
    primitives: Tuple[GltfPrimitive, ...]


class Mat4(NamedTuple):
    m11: float
    m12: float
    m13: float
    m14: float
    m21: float
    m22: float
    m23: float
    m24: float
    m31: float
    m32: float
    m33: float
    m34: float
    m41: float
    m42: float
    m43: float
    m44: float


class Vec3(NamedTuple):
    x: float
    y: float
    z: float


class Vec4(NamedTuple):
    x: float
    y: float
    z: float
    w: float


@dataclass
class GltfNode:
    name: str
    children: List['GltfNode']
    mesh: Optional[GltfMesh] = None
    matrix: Optional[Mat4] = None
    translation: Optional[Vec3] = Vec3(0, 0, 0)
    rotation: Optional[Vec4] = Vec4(0, 0, 0, 1)
    scale: Optional[Vec3] = Vec3(1, 1, 1)


class GltfData:
    def __init__(self, gltf, path: Optional[pathlib.Path], bin: Optional[bytes]):
        self.gltf = gltf
        self.path = path
        self.bin = bin
        self.images: List[GltfImage] = []
        self.textures: List[GltfTexture] = []
        self.materials: List[GltfMaterial] = []
        self.meshes: List[GltfMesh] = []
        self.nodes: List[GltfNode] = []
        self.scene: List[GltfNode] = []
        self.buffer_reader = GltfBufferReader(gltf, path, bin)

    def __str__(self) -> str:
        return f'{len(self.materials)} materials, {len(self.meshes)} meshes, {len(self.nodes)} nodes'

    def _parse_image(self, i: int, gltf_image) -> GltfImage:
        name = gltf_image.get('name')
        match gltf_image:
            case {'bufferView': buffer_view_index, 'mimeType': mime}:
                return GltfImage(name or f'{i}', self.buffer_reader.buffer_view_bytes(buffer_view_index), MimeType(mime))
            case {'uri': uri}:
                if uri.startswith('data:'):
                    m = DATA_URI.match(uri)
                    if not m:
                        raise RuntimeError()
                    return GltfImage(uri, self.buffer_reader.uri_bytes(uri), MimeType(m[1]))
                else:
                    return GltfImage(uri, self.buffer_reader.uri_bytes(uri), MimeType.from_name(uri))
            case _:
                raise GltfError()

    def _parse_texture(self, i: int, gltf_texture) -> GltfTexture:
        match gltf_texture:
            case {'source': image_index}:
                texture = GltfTexture(gltf_texture.get(
                    'name', f'{i}'), self.images[image_index])
                return texture
            case {'extensions': {
                'KHR_texture_basisu': {'source': image_index}
            }}:
                texture = GltfTexture(gltf_texture.get(
                    'name', f'{i}'), self.images[image_index])
                return texture
            case _:
                raise Exception()

    def _parse_material(self, i: int, gltf_material) -> GltfMaterial:
        name = f'{i}'
        base_color_texture = None
        base_color_factor = RGBA(1, 1, 1, 1)
        metallic_roughness_texture = None
        metallic_factor = 0.0
        roughness_factor = 0.0
        emissive_texture = None
        emissive_factor = RGB(0, 0, 0)
        normal_texture = None
        occlusion_texture = None
        alpha_mode = AlphaMode.OPAQUE
        alpha_cutoff = 0.5
        double_sided = False
        for k, v in gltf_material.items():
            match k:
                case 'name':
                    name = v
                case 'pbrMetallicRoughness':
                    for kk, vv in v.items():
                        match kk:
                            case 'baseColorTexture':
                                match vv:
                                    case {'index': texture_index}:
                                        base_color_texture = self.textures[texture_index]
                                    case _:
                                        raise GltfError()
                            case 'baseColorFactor':
                                base_color_factor = RGBA(*vv)
                            case 'metallicFactor':
                                metallic_factor = vv
                            case 'roughnessFactor':
                                roughness_factor = vv
                            case 'metallicRoughnessTexture':
                                match vv:
                                    case {'index': texture_index}:
                                        metallic_roughness_texture = self.textures[texture_index]
                            case _:
                                raise NotImplementedError()
                        pass
                case 'emissiveTexture':
                    match v:
                        case {'index': texture_index}:
                            emissive_texture = self.textures[texture_index]
                case 'emissiveFactor':
                    emissive_factor = RGB(*v)
                case 'alphaMode':
                    alpha_mode = AlphaMode(v)
                case 'alphaCutoff':
                    alpha_cutoff = v
                case 'doubleSided':
                    double_sided = v
                case 'normalTexture':
                    match v:
                        case {'index': texture_index}:
                            normal_texture = self.textures[texture_index]
                        case _:
                            raise GltfError()
                case 'occlusionTexture':
                    match v:
                        case {'index': texture_index}:
                            occlusion_texture = self.textures[texture_index]
                        case _:
                            raise GltfError()

                case 'extensions':
                    # TODO:
                    pass

                case _:
                    raise NotImplementedError()
        material = GltfMaterial(name, base_color_texture,
                                base_color_factor, metallic_roughness_texture, metallic_factor, roughness_factor,
                                emissive_texture, emissive_factor, normal_texture, occlusion_texture, alpha_mode, alpha_cutoff, double_sided)
        return material

    def _parse_mesh(self, i: int, gltf_mesh) -> GltfMesh:
        primitives = []
        for gltf_prim in gltf_mesh['primitives']:
            gltf_attributes = gltf_prim['attributes']
            positions = None
            normal = None
            uv0 = None
            uv1 = None
            uv2 = None
            tangent = None
            color = None
            joints = None
            weights = None
            for k, v in gltf_attributes.items():
                match k:
                    case 'POSITION':
                        positions = self.buffer_reader.read_accessor(v)
                    case 'NORMAL':
                        normal = self.buffer_reader.read_accessor(v)
                    case 'TEXCOORD_0':
                        uv0 = self.buffer_reader.read_accessor(v)
                    case 'TEXCOORD_1':
                        uv1 = self.buffer_reader.read_accessor(v)
                    case 'TEXCOORD_2':
                        uv2 = self.buffer_reader.read_accessor(v)
                    case 'TANGENT':
                        tangent = self.buffer_reader.read_accessor(v)
                    case 'COLOR_0':
                        color = self.buffer_reader.read_accessor(v)
                    case 'JOINTS_0':
                        joints = self.buffer_reader.read_accessor(v)
                    case 'WEIGHTS_0':
                        weights = self.buffer_reader.read_accessor(v)
                    case _:
                        raise NotImplementedError()
            if not positions:
                raise GltfError('no POSITIONS')

            indices = None
            match gltf_prim:
                case {'indices': accessor}:
                    indices = self.buffer_reader.read_accessor(accessor)

            match gltf_prim:
                case {'material': material_index}:
                    material = self.materials[material_index]
                case _:
                    # use default material
                    material = GltfMaterial.default()
            prim = GltfPrimitive(material, positions, normal,
                                 uv0, uv1, uv2,
                                 tangent, color,
                                 joints, weights,
                                 indices)
            primitives.append(prim)

        mesh = GltfMesh(gltf_mesh.get('name', f'{i}'), tuple(primitives))
        return mesh

    def _parse_node(self, i: int, gltf_node) -> GltfNode:
        node = GltfNode(f'{i}', [])
        for k, v in gltf_node.items():
            match k:
                case 'name':
                    node.name = v
                case 'mesh':
                    node.mesh = self.meshes[v]
                case 'children':
                    pass
                case 'matrix':
                    node.matrix = v
                case 'translation':
                    node.translation = Vec3(*v)
                case 'rotation':
                    node.rotation = Vec4(*v)
                case 'scale':
                    node.scale = Vec3(*v)
                case 'skin':
                    # TODO:
                    pass
                case 'camera':
                    # TODO:
                    pass
                case 'extensions':
                    # TODO:
                    pass
                case 'extras':
                    # TODO
                    pass
                case _:
                    raise NotImplementedError()
        return node

    def parse(self):
        # image
        for i, gltf_image in enumerate(self.gltf.get('images', [])):
            image = self._parse_image(i, gltf_image)
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
            mesh = self._parse_mesh(i, gltf_mesh)
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
                       for node_index in self.gltf['scenes'][self.gltf.get('scene', 0)]['nodes']]


def parse_gltf(json_chunk: bytes, *, path: Optional[pathlib.Path] = None, bin: Optional[bytes] = None) -> GltfData:
    gltf = json.loads(json_chunk)
    data = GltfData(gltf, path, bin)
    data.parse()

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
