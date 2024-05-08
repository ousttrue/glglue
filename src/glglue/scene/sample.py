import glglue.frame_input
from OpenGL import GL  # type: ignore
from glglue import glo
from glglue.camera.mouse_camera import MouseCamera
from glglue.drawable import Drawable, cube, teapot, axes, grid
import glm
import dataclasses

import logging

LOGGER = logging.getLogger(__name__)


@dataclasses.dataclass
class Node:
    name: str
    world_matrix: glm.mat4 = glm.mat4(1.0)

    def set_position(self, pos: glm.vec3) -> None:
        self.world_matrix = glm.translate(pos)


class SampleScene:
    def __init__(self) -> None:
        self.initialized = False
        self.mouse_camera = MouseCamera()
        self.drawables: list[Drawable] = []
        self.cube_node = Node("cube")
        self.teapot_node = Node("teapot")

    def lazy_initialize(self):
        if self.initialized:
            return
        self.initialized = True

        # shader
        mesh_shader = glo.Shader.load_from_pkg("glglue", "assets/mesh")
        assert mesh_shader
        self.drawables.append(
            cube.create(
                mesh_shader,
                mesh_shader.create_props(self.mouse_camera.camera, self.cube_node),
            )
        )
        self.drawables.append(
            teapot.create(
                mesh_shader,
                mesh_shader.create_props(self.mouse_camera.camera, self.teapot_node),
            )
        )

        line_shader = glo.Shader.load_from_pkg("glglue", "assets/line")
        assert line_shader
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

    def render(self, frame: glglue.frame_input.FrameInput):
        self.lazy_initialize()

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

        # render
        for drawable in self.drawables:
            drawable.draw()

        # flush
        GL.glFlush()
