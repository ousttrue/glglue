from typing import Any
import glglue.frame_input
from OpenGL import GL  # type: ignore
from glglue import glo
from glglue.camera.mouse_camera import MouseCamera
from glglue.drawable import Drawable, axes, grid
import glm

import logging

LOGGER = logging.getLogger(__name__)


# @dataclasses.dataclass
# class Node:
#     name: str
#     world_matrix: glm.mat4 = glm.mat4(1.0)

#     def set_position(self, pos: glm.vec3) -> None:
#         self.world_matrix = glm.translate(pos)


class GizmoContext:
    def __init__(self):
        self.color = glm.vec3(1, 1, 1)

    def draw_line(self, s: glm.vec3, e: glm.vec3) -> None:
        pass


class Gizmos:
    def __init__(self):
        self.context = GizmoContext()

    def __enter__(self) -> GizmoContext:
        # print("enter")
        return self.context

    def __exit__(self, ex_type: type, ex_value: Exception, trace: Any):
        # print("exit: ", ex_type, ex_value, trace)
        pass


class SampleScene:
    def __init__(self) -> None:
        self.gizmos = Gizmos()
        self.initialized = False
        self.mouse_camera = MouseCamera()
        self.drawables: list[Drawable] = []

    def render(self, frame: glglue.frame_input.FrameInput):
        self.begin_render(frame)
        self.draw()
        self.end_render()

    def draw(self):
        if not self.initialized:
            self.initialized = True

            line_shader = glo.Shader.load_from_pkg("glglue", "assets/line")
            self.drawables.append(
                axes.create(
                    line_shader,
                    line_shader.create_props(self.mouse_camera.camera),
                )
            )
            self.drawables.append(
                grid.create(
                    line_shader,
                    line_shader.create_props(self.mouse_camera.camera),
                )
            )

        with self.gizmos as gizmos:
            gizmos.color = glm.vec3(1, 0, 0)
            gizmos.draw_line(glm.vec3(0, 0, 0), glm.vec3(1, 1, 1))

        # render
        for drawable in self.drawables:
            drawable.draw()

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
