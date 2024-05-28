from typing import Any, NamedTuple
import ctypes
import glglue.drawable
import glglue.frame_input
from OpenGL import GL  # type: ignore
from glglue import glo, drawable, camera

import logging

LOGGER = logging.getLogger(__name__)


class GizmoContext(NamedTuple):
    verticies: ctypes.Array[drawable.line_builder.Vertex]
    submesh: drawable.Submesh
    color: drawable.line_builder.Float3 = drawable.line_builder.Float3(1, 1, 1)

    def set_color(self, color: drawable.line_builder.Float3) -> None:
        self.color.x = color.x
        self.color.y = color.y
        self.color.z = color.z

    def draw_line(
        self, s: drawable.line_builder.Float3, e: drawable.line_builder.Float3
    ) -> None:
        self.verticies[self.submesh.draw_count].position = s
        self.verticies[self.submesh.draw_count].color = self.color
        self.submesh.draw_count += 1
        self.verticies[self.submesh.draw_count].position = e
        self.verticies[self.submesh.draw_count].color = self.color
        self.submesh.draw_count += 1


class Gizmos:
    def __init__(self):
        self.drawable: drawable.Drawable | None = None
        self.vertices = (drawable.line_builder.Vertex * 65535)()

    def __enter__(self) -> GizmoContext:
        assert self.drawable
        submesh = self.drawable.submeshes[0]
        submesh.draw_count = 0
        return GizmoContext(self.vertices, submesh)

    def __exit__(self, ex_type: type, ex_value: Exception, trace: Any):
        assert self.drawable
        self.drawable.vao.vbo.update(memoryview(self.vertices))

    def make_drawable(
        self, shader: glo.Shader, props: list[glo.UniformUpdater], n: int = 5
    ) -> drawable.Drawable:
        vbo = glo.Vbo()
        vbo.set_vertices(memoryview(self.vertices), is_dynamic=True)

        vao = glo.Vao(
            vbo, glo.VertexLayout.create_list(shader.program), topology=GL.GL_LINES
        )

        self.drawable = drawable.Drawable(vao)
        self.drawable.push_submesh(shader, 0, props)
        return self.drawable


class SampleScene:
    def __init__(self) -> None:
        self.gizmos = Gizmos()
        self.initialized = False
        self.mouse_camera = camera.mouse_camera.MouseCamera()
        self.drawables: list[drawable.Drawable] = []

    def render(self, frame: glglue.frame_input.FrameInput):
        if not self.initialized:
            self.initialized = True

            line_shader = glo.Shader.load_from_pkg("glglue", "assets/line")
            self.drawables.append(
                drawable.axes.create(
                    line_shader,
                    line_shader.create_props(self.mouse_camera.camera),
                )
            )
            self.drawables.append(
                drawable.grid.create(
                    line_shader,
                    line_shader.create_props(self.mouse_camera.camera),
                )
            )

            self.drawables.append(
                self.gizmos.make_drawable(
                    line_shader, line_shader.create_props(self.mouse_camera.camera)
                )
            )

        self.begin_render(frame)

        with self.gizmos as gizmos:
            gizmos.set_color(drawable.line_builder.Float3(1, 0, 0))
            gizmos.draw_line(
                drawable.line_builder.Float3(0, 0, 0),
                drawable.line_builder.Float3(1, 1, 1),
            )

        # render
        for d in self.drawables:
            d.draw()

        self.end_render()

    def begin_render(self, frame: glglue.frame_input.FrameInput):
        # update camera
        self.mouse_camera.process(frame)

        # https://learnopengl.com/Advanced-OpenGL/Depth-testing
        GL.glEnable(GL.GL_DEPTH_TEST)  # type: ignore
        GL.glDepthFunc(GL.GL_LESS)  # type: ignore

        # https://learnopengl.com/Advanced-OpenGL/Face-culling
        # GL.glEnable(GL.GL_CULL_FACE)

        # clear
        GL.glViewport(0, 0, frame.width, frame.height)  # type: ignore
        r = 0
        if frame.mouse_left:
            LOGGER.debug("LEFT_MOUSE")
            g = 0.1
        else:
            g = 0
        if frame.height == 0:
            return
        b = 0
        GL.glClearColor(r, g, b, 1.0)  # type: ignore
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)  # type: ignore

    def end_render(self):
        # flush
        GL.glFlush()
