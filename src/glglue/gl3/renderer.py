from typing import Dict, Union, Tuple


from ..scene.node import Node
from ..scene.mesh import Mesh
from ..scene.material import Material, Texture, CubeMap
from ..ctypesmath import Mat4, FrameState
import glglue.gl3.vbo
import glglue.gl3.shader
import glglue.gl3.texture
from OpenGL import GL


class Renderer:
    def __init__(self) -> None:
        self.textures: Dict[Texture, glglue.gl3.texture.Texture] = {}
        self.cubemaps: Dict[CubeMap, glglue.gl3.texture.CubeMap] = {}
        self.shaders: Dict[glglue.gl3.shader.ShaderSource,
                           glglue.gl3.shader.Shader] = {}
        self.meshes: Dict[Mesh, glglue.gl3.vbo.Drawable] = {}

    def _get_or_create_texture(self, src: Texture) -> glglue.gl3.texture.Texture:
        texture = self.textures.get(src)
        if not texture:
            texture = glglue.gl3.texture.Texture()
            image = src.image
            texture.load(image.data, image.width, image.height)
            self.textures[src] = texture
        return texture

    def _get_or_create_cubemap(self, src: CubeMap) -> glglue.gl3.texture.CubeMap:
        cubemap = self.cubemaps.get(src)
        if not cubemap:
            cubemap = glglue.gl3.texture.CubeMap()
            cubemap.load(*src)
            self.cubemaps[src] = cubemap
        return cubemap

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

            material = submesh.material
            if material.cubemap:

                shader.set_uniform('V', view, False)
                shader.set_uniform('P', projection, False)

                GL.glEnable(GL.GL_CULL_FACE)
                GL.glDepthMask(GL.GL_FALSE)
                cubemap = self._get_or_create_cubemap(material.cubemap)
                cubemap.bind()
                GL.glActiveTexture(GL.GL_TEXTURE0)
                drawable.draw(submesh.topology, submesh.offset,
                              submesh.draw_count)
                GL.glDepthMask(GL.GL_TRUE)

            else:

                shader.set_uniform('vp', view * projection)
                shader.set_uniform('m', model)

                if submesh.material.color_texture:
                    texture = self._get_or_create_texture(
                        submesh.material.color_texture)
                    shader.set_texture('COLOR_TEXTURE', 0, texture)

                drawable.draw(submesh.topology, submesh.offset,
                              submesh.draw_count)

    def _draw_node(self, node: Node, projection: Mat4, view: Mat4, parent: Mat4):
        m = node.get_local_matrix() * parent

        for mesh in node.meshes:
            self._draw_mesh(mesh, projection, view, m)

        for child in node.children:
            self._draw_node(child, projection, view, m)

    def draw(self, root: Union[Node, Mesh], state: FrameState):
        match root:
            case Node() as node:
                self._draw_node(node, state.camera_projection,
                                state.camera_view, Mat4.new_identity())
            case Mesh() as mesh:
                self._draw_mesh(mesh, state.camera_projection,
                                state.camera_view, Mat4.new_identity())
