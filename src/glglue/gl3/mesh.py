from typing import List, Optional, Union
import glglue.ctypesmath
import glglue.gl3.shader
import glglue.gl3.vbo


class Submesh:
    def __init__(self, topology: int, offset: int, draw_count: int, vs: str, fs: str) -> None:
        self.shader: Optional[glglue.gl3.shader.Shader] = None
        self.topology = topology
        self.offset = offset
        self.draw_count = draw_count
        self.vs = vs
        self.fs = fs

    def draw(self, projection, view, m):
        if not self.shader:
            self.shader = glglue.gl3.shader.create_from(self.vs, self.fs)
        self.shader.use()
        self.shader.set_uniform('vp', view * projection)
        self.shader.set_uniform('m', m)


class Mesh:
    def __init__(self, name: str, vertices: Union[glglue.gl3.vbo.Planar, glglue.gl3.vbo.Interleaved], indices: Optional[glglue.gl3.vbo.TypedBytes] = None) -> None:
        self.name = name
        self.is_initialized = False
        self.vbo_list = []
        self.vbo_color = None
        self.ibo = None
        self.indices = indices
        self.vertices = vertices
        self.submeshes: List[Submesh] = []

    def add_submesh(self, topology, vs: str, fs: str):
        draw_count = self.vertices.count()
        if self.indices:
            draw_count = self.indices.count()
        self.submeshes.append(Submesh(topology, 0, draw_count, vs, fs))

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
            submesh.draw(projection, view, model)
            self.vao.draw(submesh.topology, submesh.offset, submesh.draw_count)


class Node:
    def __init__(self, name: str):
        self. name = name
        self.model_matrix = glglue.ctypesmath.Mat4.new_identity()
        self.children: List['Node'] = []
        self.meshes: List[Mesh] = []

    def update(self, delta):
        pass

    def draw(self, projection: glglue.ctypesmath.Mat4, view: glglue.ctypesmath.Mat4):
        for mesh in self.meshes:
            mesh.draw(projection, view, self.model_matrix)

        for child in self.children:
            child.draw(projection, view)
