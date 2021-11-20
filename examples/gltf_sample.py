from PySide6 import QtWidgets, QtGui, QtCore
import pathlib
import logging
from glglue.ctypesmath.mat4 import Mat4
import glglue.gltf
from glglue.scene.texture import Texture, Image32
from glglue.scene.material import Material
from glglue.scene.mesh import Mesh
from glglue.scene.node import Node
from glglue.scene.vertices import Interleaved, Planar, TypedBytes
import glglue.gl3.vbo
import glglue.gl3.shader
from typing import Dict, List, NamedTuple, Optional
from OpenGL import GL

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(levelname)s:%(name)s:%(message)s',
                    level=logging.DEBUG)


VS = '''
in vec3 aPosition;

#ifdef HAS_UV
in vec2 aUV;
out vec2 vUV;
#endif

uniform mediump mat4 m;
uniform mediump mat4 vp;

void main ()
{
    gl_Position = vec4(aPosition, 1) * m * vp;
#ifdef HAS_UV
    vUV = aUV;
#endif
}
'''

FS = '''
#ifdef HAS_UV
in vec2 vUV;
#else
vec2 uUV = vec2(1, 1);
#endif

out vec4 fColor;
void main()
{
    fColor = vec4(vUV, 0, 1);
}
'''


class Loader:
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


class Window(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        # setup opengl widget
        import glglue.gl3.samplecontroller
        self.controller = glglue.gl3.samplecontroller.SampleController()
        import glglue.pyside6
        import glglue.utils
        self.glwidget = glglue.pyside6.Widget(
            self, self.controller, glglue.utils.get_desktop_scaling_factor())
        self.setCentralWidget(self.glwidget)

        # menu
        menu = self.menuBar()
        file_menu = menu.addMenu("&File")
        open_action = QtGui.QAction("&Open", self)
        open_action.triggered.connect(self.open_dialog)  # type: ignore
        file_menu.addAction(open_action)

    @QtCore.Slot()  # type: ignore
    def open_dialog(self):
        dialog = QtWidgets.QFileDialog(self, caption="open bvh")
        dialog.setFileMode(QtWidgets.QFileDialog.AnyFile)
        dialog.setNameFilters(
            ["gltf files (*.gltf;*.glb;*.zip;*.vrm)", "Any files (*)"])
        if not dialog.exec():
            return
        files = dialog.selectedFiles()
        if not files:
            return
        path = pathlib.Path(files[0])
        self.load(path)

    def load(self, path: pathlib.Path):
        gltf = glglue.gltf.parse_path(path)

        # create mesh
        loader = Loader(gltf)
        scene = loader.load()
        self.controller.drawables = [scene]
        self.glwidget.repaint()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.resize(1600, 1200)

    if len(sys.argv) > 1:
        path = pathlib.Path(sys.argv[1])
        window.load(path)

    window.show()
    sys.exit(app.exec())
