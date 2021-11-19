from PySide6 import QtWidgets, QtGui, QtCore
import pathlib
import logging
import glglue.gltf
import glglue.gl3.mesh
import glglue.gl3.vbo
from typing import List
import os
from OpenGL import GL

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(levelname)s:%(name)s:%(message)s',
                    level=logging.DEBUG)


VS = '''
in vec3 aPosition;

#ifdef HAS_NORMAL
in vec3 aNormal;
#endif

uniform mediump mat4 m;
uniform mediump mat4 vp;

void main ()
{
    gl_Position = vec4(aPosition, 1) * m * vp;
}
'''

FS = '''
#version 330
out vec4 fColor;
void main()
{
    fColor = vec4(1, 1, 1, 1);
}
'''


class Node:
    def __init__(self, name: str):
        self.name = name
        self.children: List['Node'] = []
        self.meshes: List[glglue.gl3.mesh.Mesh] = []

    def add_child(self, child: 'Node'):
        self.children.append(child)

    def update(self, delta):
        pass

    def draw(self, projection, view):
        for mesh in self.meshes:
            mesh.draw(projection, view)

        for child in self.children:
            child.draw(projection, view)


def _typed_bytes(src: glglue.gltf.TypedBytes) -> glglue.gl3.vbo.TypedBytes:
    match src:
        case glglue.gltf.TypedBytes(data, glglue.gltf.ElementType.Float, count):
            return glglue.gl3.vbo.TypedBytes(data, GL.GL_FLOAT, count)
        case glglue.gltf.TypedBytes(data, glglue.gltf.ElementType.UInt16, count):
            return glglue.gl3.vbo.TypedBytes(data, GL.GL_UNSIGNED_SHORT, count)
        case _:
            raise NotImplementedError()


def _load_node(src: List[glglue.gltf.GltfNode], dst: Node):
    for gltf_node in src:
        node = Node(gltf_node.name)
        dst.add_child(node)

        # mesh
        if gltf_node.mesh:
            for prim in gltf_node.mesh.primitives:
                macro = '#version 330\n'
                attributes: List[glglue.gl3.vbo.TypedBytes] = [
                    _typed_bytes(prim.position)]
                if prim.normal:
                    attributes.append(_typed_bytes(prim.normal))
                    macro += f'#define HAS_NORMAL 1\n'
                indices = None
                if prim.indices:
                    indices = _typed_bytes(prim.indices)
                mesh = glglue.gl3.mesh.Mesh(
                    gltf_node.mesh.name, glglue.gl3.vbo.Planar(attributes), indices)
                mesh.add_submesh(GL.GL_TRIANGLES, macro + VS, FS)
                dst.meshes.append(mesh)

        _load_node(gltf_node.children, node)


def load_gltf(gltf: glglue.gltf.GltfData) -> Node:
    scene = Node('__scene__')
    _load_node(gltf.scene, scene)
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
        self.controller.drawables = [load_gltf(gltf)]
        self.glwidget.repaint()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = Window()

    match os.environ.get('GLTF_SAMPLE_MODELS'):
        case str() as dir:
            path = pathlib.Path(dir) / '2.0/Box/glTF-Binary/Box.glb'
            window.load(path)

    window.show()
    sys.exit(app.exec())
