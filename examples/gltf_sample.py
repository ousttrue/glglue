from PySide6 import QtWidgets, QtGui, QtCore
import pathlib
import logging
import glglue.gltf
import glglue.scene.material
import glglue.scene.mesh
import glglue.scene.node
import glglue.gl3.vbo
import glglue.gl3.shader
from typing import Dict, List
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
        # self.textures: Dict[glglue.gltf.GltfTexture, glglue.gl3.shader.T]= {}
        self.materials: Dict[glglue.gltf.GltfMaterial,
                             glglue.scene.material.Material] = {}
        self.meshes: Dict[glglue.gltf.GltfMesh,
                          List[glglue.scene.mesh.Mesh]] = {}

    def _load_material(self, src: glglue.gltf.GltfMaterial):
        material = glglue.scene.material.Material(src.name, VS, FS)
        # to bitmap
        # material.color_texture = src.base_color_texture
        # material.color = *src.base_color_factor
        self.materials[src] = material

    def _load_mesh(self, src: glglue.gltf.GltfMesh):
        meshes = []

        for prim in src.primitives:
            macro = ['#version 330']
            attributes: List[glglue.gl3.vbo.TypedBytes] = [
                glglue.gl3.vbo.TypedBytes(*prim.position)]
            # if prim.normal:
            #     attributes.append(glglue.gl3.vbo.TypedBytes(*prim.normal))
            #     macro += f'#define HAS_NORMAL 1\n'
            if prim.uv:
                attributes.append(glglue.gl3.vbo.TypedBytes(*prim.uv))
                macro.append('#define HAS_UV 1')
            indices = None
            if prim.indices:
                indices = glglue.gl3.vbo.TypedBytes(*prim.indices)
            mesh = glglue.scene.mesh.Mesh(
                src.name, glglue.gl3.vbo.Planar(attributes), indices)

            mesh.add_submesh(
                self.materials[prim.material], macro, GL.GL_TRIANGLES)
            meshes.append(mesh)

        self.meshes[src] = meshes

    def _load_node(self, src: List[glglue.gltf.GltfNode], dst: glglue.scene.node.Node):
        for gltf_node in src:
            node = glglue.scene.node.Node(gltf_node.name)
            dst.children.append(node)

            if gltf_node.mesh:
                dst.meshes += self.meshes[gltf_node.mesh]

            self._load_node(gltf_node.children, node)

    def load(self):
        # texture

        # material
        for gltf_material in self.gltf.materials:
            self._load_material(gltf_material)

        # mesh
        for gltf_mesh in self.gltf.meshes:
            self._load_mesh(gltf_mesh)

        # node
        scene = glglue.scene.node.Node('__scene__')
        self._load_node(self.gltf.scene, scene)
        return scene


def load_gltf(gltf: glglue.gltf.GltfData) -> glglue.scene.node.Node:
    loader = Loader(gltf)
    return loader.load()


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
        self.controller.drawables = [load_gltf(gltf)]
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
