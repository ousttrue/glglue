from typing import Dict, Union, NamedTuple, List, Tuple

from ..scene.node import Node
from ..scene.mesh import Mesh
from ..scene.material import Material
from ..ctypesmath.mat4 import Mat4
import glglue.gl3.vbo
import glglue.gl3.shader


class Renderer:
    def __init__(self) -> None:
        self.shaders: Dict[glglue.gl3.shader.ShaderSource,
                           glglue.gl3.shader.Shader] = {}
        self.meshes: Dict[Mesh, glglue.gl3.vbo.Drawable] = {}

    def _get_or_create_shader(self, src: Material, macro: Tuple[str, ...]) -> glglue.gl3.shader.Shader:
        shader_source = glglue.gl3.shader.ShaderSource(
            src.vs, macro, src.fs, macro)
        shader = self.shaders.get(shader_source)
        if not shader:
            shader = glglue.gl3.shader.create_from(shader_source)
            self.shaders[shader_source] = shader
        return shader

    def _get_or_create_mesh(self, src: Mesh) -> glglue.gl3.vbo.Drawable:
        drawable = self.meshes.get(src)
        if not drawable:
            drawable = glglue.gl3.vbo.create(src.vertices, src.indices)
            # dm = DrawableMacro(mesh, macro)
            self.meshes[src] = drawable
        return drawable

    def _draw_mesh(self, mesh: Mesh, projection: Mat4, view: Mat4, model: Mat4):
        drawable = self._get_or_create_mesh(mesh)

        for submesh in mesh.submeshes:

            shader = self._get_or_create_shader(
                submesh.material, tuple(submesh.macro))

            shader.use()
            shader.set_uniform('vp', view * projection)
            shader.set_uniform('m', model)            

            drawable.draw(submesh.topology, submesh.offset, submesh.draw_count)

    def _draw_node(self, node: Node, projection: Mat4, view: Mat4, parent: Mat4):
        m = node.model_matrix * parent

        for mesh in node.meshes:
            self._draw_mesh(mesh, projection, view, m)

        for child in node.children:
            self._draw_node(child, projection, view, m)

    def draw(self, root: Union[Node, Mesh], projection: Mat4, view: Mat4):
        match root:
            case Node() as node:
                self._draw_node(node, projection, view, Mat4.new_identity())
            case Mesh() as mesh:
                self._draw_mesh(mesh, projection, view, Mat4.new_identity())
