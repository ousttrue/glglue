from typing import Dict, List
import pkgutil
from OpenGL import GL
import glglue.gltf
import glglue.gl3.vbo
from .scene.texture import Image32, Texture
from .scene.material import Material
from .scene.mesh import Mesh
from .scene.node import Node
from .scene.vertices import Planar


def get_shader(name: str) -> str:
    data = pkgutil.get_data('glglue', f'assets/{name}')
    if not data:
        raise Exception()
    return data.decode('utf-8')


VS = get_shader('gltf.vs')
FS = get_shader('gltf.fs')


class GltfLoader:
    def __init__(self, gltf: glglue.gltf.GltfData) -> None:
        self.gltf = gltf
        self.images: Dict[glglue.gltf.GltfImage, Image32] = {}
        self.textures: Dict[glglue.gltf.GltfTexture, Texture] = {}
        self.materials: Dict[glglue.gltf.GltfMaterial, Material] = {}
        self.meshes: Dict[glglue.gltf.GltfPrimitive, Mesh] = {}

    def _load_image(self, src: glglue.gltf.GltfImage):
        image = Image32.load(src.data)
        self.images[src] = image

    def _load_texture(self, src: glglue.gltf.GltfTexture):
        texture = Texture(src.name, self.images[src.image])
        self.textures[src] = texture

    def _load_material(self, src: glglue.gltf.GltfMaterial):
        material = Material(src.name, VS, FS)
        if src.base_color_texture:
            material.color_texture = self.textures[src.base_color_texture]
        self.materials[src] = material

    def _load_mesh(self, name: str, src: glglue.gltf.GltfPrimitive):
        macro = ['#version 330']
        attributes: List[glglue.gl3.vbo.TypedBytes] = [
            glglue.gl3.vbo.TypedBytes(*src.position)]
        # if prim.normal:
        #     attributes.append(glglue.gl3.vbo.TypedBytes(*prim.normal))
        #     macro += f'#define HAS_NORMAL 1\n'
        if src.uv:
            attributes.append(glglue.gl3.vbo.TypedBytes(*src.uv))
            macro.append('#define HAS_UV 1')
        indices = None
        if src.indices:
            indices = glglue.gl3.vbo.TypedBytes(*src.indices)

        mesh = Mesh(name, Planar(attributes), indices)
        mesh.add_submesh(self.materials[src.material], macro, GL.GL_TRIANGLES)
        self.meshes[src] = mesh

    def _load(self, src: List[glglue.gltf.GltfNode], dst: Node):
        for gltf_node in src:
            node = Node(gltf_node.name)
            dst.children.append(node)

            if gltf_node.mesh:
                for gltf_prim in gltf_node.mesh.primitives:
                    mesh = self.meshes[gltf_prim]
                    node.meshes.append(mesh)

            self._load(gltf_node.children, node)

    def load(self) -> Node:
        for image in self.gltf.images:
            self._load_image(image)
        for texture in self.gltf.textures:
            self._load_texture(texture)
        for material in self.gltf.materials:
            self._load_material(material)
        for mesh in self.gltf.meshes:
            for i, prim in enumerate(mesh.primitives):
                self._load_mesh(f'{mesh.name}:{i}', prim)

        scene = Node('__scene__')
        self._load(self.gltf.scene, scene)
        return scene
