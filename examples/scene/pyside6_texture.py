# coding: utf-8
"""
pip install pyside6
"""
import logging
import ctypes
from PySide6 import QtWidgets
from glglue.scene.sample import SampleScene
from glglue.drawable.mesh_builder import MeshBuilder, Float2
from glglue import glo
from glglue.drawable import Drawable
from OpenGL import GL
import random
import uuid
from PIL import Image, ImageDraw


LOGGER = logging.getLogger(__name__)


VS = """#version 330
in vec2 a_pos;
in vec2 a_uv;
out vec2 v_uv;

void main() {
    gl_Position = vec4(a_pos, 0, 1);
    v_uv = a_uv; 
}
"""

FS = """#version 330
in vec2 v_uv;
out vec4 FragColor;
uniform sampler2D u_texture;

void main() {
    // FragColor = vec4(v_uv, 0, 1);
    vec4 texcel = texture(u_texture, v_uv);
    FragColor = texcel;
}
"""


class Vertex(ctypes.Structure):
    _fields_ = [
        ("position", Float2),
        ("uv", Float2),
    ]


def color_gird() -> Image.Image:
    run_id = uuid.uuid1()

    LOGGER.debug(f"Processing run_id: {run_id}")

    image = Image.new("RGBA", (1600, 1600))
    rectangle_width = 160
    rectangle_height = 160

    draw_image = ImageDraw.Draw(image)
    for i in range(10):
        for j in range(10):
            rectangle_x = i * 160
            rectangle_y = j * 160

            rectangle_shape = [
                (rectangle_x, rectangle_y),
                (rectangle_x + rectangle_width, rectangle_y + rectangle_height),
            ]
            draw_image.rectangle(
                rectangle_shape,
                fill=(
                    random.randint(0, 255),
                    random.randint(0, 255),
                    random.randint(0, 255),
                ),
            )
    return image


class TextureScene(SampleScene):
    def __init__(self):
        super().__init__()
        self.is_initialized = False
        self.drawable: Drawable | None = None

    def draw(self):
        if not self.is_initialized:
            self.is_initialized = True
            LOGGER.info("init")

            shader = glo.Shader.load(VS, FS)

            builder = MeshBuilder(Vertex)

            """
            3 2
            +-+
            |/|
            +-+
            0 1
            """
            size = 0.9
            builder.push_quad(
                Vertex(Float2(-size, -size), Float2(0, 1)),
                Vertex(Float2(size, -size), Float2(1, 1)),
                Vertex(Float2(size, size), Float2(1, 0)),
                Vertex(Float2(-size, size), Float2(0, 0)),
            )
            vertices = builder.create_vertices()
            assert len(vertices) == 6

            vbo = glo.Vbo()
            vbo.set_vertices(memoryview(vertices))

            vao = glo.Vao(
                vbo,
                glo.VertexLayout.create_list(shader.program),
            )

            image = color_gird()
            texture = glo.Texture(image.width, image.height, image.tobytes())

            self.drawable = Drawable(vao)

            def setup_texture():
                GL.glActiveTexture(GL.GL_TEXTURE0)
                texture.bind()

            self.drawable.push_submesh(shader, 6, [setup_texture])

        assert self.drawable
        self.drawable.draw()


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__(None)

        self.scene = TextureScene()

        import glglue.pyside6

        self.glwidget = glglue.pyside6.Widget(self, render_gl=self.scene.render)
        self.setCentralWidget(self.glwidget)


def main():
    import sys

    logging.basicConfig(level=logging.DEBUG)

    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
