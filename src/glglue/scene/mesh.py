from typing import List, Optional, Union
import glglue.ctypesmath
import glglue.gl3.shader
import glglue.gl3.vbo
from .material import Material
from .vertices import Planar, Interleaved, TypedBytes


class Submesh:
    def __init__(self, material: Material, macro: List[str], topology: int, offset: int, draw_count: int) -> None:
        self.material = material
        self.macro = macro
        self.shader: Optional[glglue.gl3.shader.Shader] = None

        self.topology = topology
        self.offset = offset
        self.draw_count = draw_count

    def activate(self, projection, view, m):
        if not self.shader:
            shader_source = glglue.gl3.shader.ShaderSource(
                self.material.vs, self.macro, self.material.fs, self.macro)
            self.shader = glglue.gl3.shader.create_from(shader_source)
        self.shader.use()
        self.shader.set_uniform('vp', view * projection)
        self.shader.set_uniform('m', m)


class Mesh:
    def __init__(self, name: str, vertices: Union[Planar, Interleaved], indices: Optional[TypedBytes] = None) -> None:
        self.name = name
        self.is_initialized = False
        self.vbo_list = []
        self.vbo_color = None
        self.ibo = None
        self.indices = indices
        self.vertices = vertices
        self.submeshes: List[Submesh] = []

    def add_submesh(self, material: Material, macro: List[str], topology):
        draw_count = self.vertices.count()
        if self.indices:
            draw_count = self.indices.count()
        self.submeshes.append(
            Submesh(material, macro, topology, 0, draw_count))

    def initialize(self):
        if self.is_initialized:
            return

        self.vbo_list = glglue.gl3.vbo.create_vbo_from(self.vertices)
        if self.indices:
            self.ibo = glglue.gl3.vbo.create_ibo_from(self.indices)
        self.vao = glglue.gl3.vbo.create_vao_from(self.ibo, self.vbo_list)
        self.is_initialized = True

    def update(self, delta):
        pass

    def draw(self, projection: glglue.ctypesmath.Mat4, view: glglue.ctypesmath.Mat4, model: glglue.ctypesmath.Mat4 = None):
        self.initialize()

        if not model:
            model = glglue.ctypesmath.Mat4.new_identity()

        for submesh in self.submeshes:
            submesh.activate(projection, view, model)
            self.vao.draw(submesh.topology, submesh.offset, submesh.draw_count)
