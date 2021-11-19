from PySide6 import QtWidgets, QtGui, QtCore
import pathlib
import logging
import glglue.gltf
from typing import List, Optional
import os

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(levelname)s:%(name)s:%(message)s',
                    level=logging.DEBUG)


class Node:
    def __init__(self, name: str):
        self.name = name
        self.children: List['Node'] = []
        self.parent: Optional['Node'] = None

    def add_child(self, child: 'Node'):
        child.parent = self
        self.children.append(child)

    def update(self, delta):
        pass

    def draw(self, projection, view):
        pass


def _load_node(src: List[glglue.gltf.GltfNode], dst: Node):
    for gltf_node in src:
        node = Node(gltf_node.name)
        dst.add_child(node)

        # mesh
        if gltf_node.mesh:
            pass

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
