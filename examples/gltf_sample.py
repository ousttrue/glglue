from PySide6 import QtWidgets, QtGui, QtCore
import pathlib
import logging
import glglue.gltf
import glglue.gltf_loader
import glglue.ktx2
import glglue.gl3.vbo
import glglue.gl3.shader
import glglue.gl3.texture
import glglue.scene.cubemap
from glglue.scene.texture import CubeMap


logger = logging.getLogger(__name__)
logging.basicConfig(format='%(levelname)s:%(name)s:%(message)s',
                    level=logging.DEBUG)


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
        loader = glglue.gltf_loader.GltfLoader(gltf)
        scene = loader.load()
        self.controller.drawables = [scene]
        self.glwidget.repaint()

    def load_cubemap(self, path: pathlib.Path):
        ktx2 = glglue.ktx2.parse_path(path)

        match ktx2.levelImages[0]:
            case glglue.ktx2.CubeMap() as cubemap_data:
                cubemap = glglue.scene.cubemap.create_cubemap(
                    CubeMap(*cubemap_data))
                self.controller.env.insert(0, cubemap)

        self.glwidget.repaint()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication([])
    window = Window()

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--load")
    parser.add_argument("-c", "--cubemap")
    parser.parse_args()

    args = parser.parse_args()
    if args.load:
        path = pathlib.Path(args.load)
        window.load(path)
    if args.cubemap:
        path = pathlib.Path(args.cubemap)
        window.load_cubemap(path)

    window.show()
    sys.exit(app.exec())
