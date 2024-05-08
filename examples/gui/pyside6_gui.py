from PySide6 import QtWidgets, QtCore
import sys
import logging
import glglue.pyside6
import glm

LOGGER = logging.getLogger(__name__)


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__(None)
        from glglue.scene.sample import SampleScene

        self.scene = SampleScene()

        self.glwidget = glglue.pyside6.Widget(self, render_gl=self.scene.render)
        self.setCentralWidget(self.glwidget)

        self.menubar = self.menuBar()
        self.menubar.setNativeMenuBar(False)

        # status bar
        self.sb = self.statusBar()
        # self.sb.showMessage("")

        # slider
        scene = QtWidgets.QWidget()
        vbox = QtWidgets.QVBoxLayout()

        def new_slider(init: int):
            slider = QtWidgets.QSlider()
            slider.setOrientation(QtCore.Qt.Orientation.Horizontal)
            slider.setRange(-100, 100)
            slider.setValue(init)
            return slider

        # cube
        cube_x = new_slider(-50)

        def on_cube_x(value: int):
            self.scene.cube_node.set_position(glm.vec3(value * 0.01, 0, 0))
            self.glwidget.repaint()

        cube_x.valueChanged.connect(on_cube_x)
        vbox.addWidget(cube_x)

        # teapot
        teapot_x = new_slider(50)

        def on_teapot_x(value: int):
            self.scene.teapot_node.set_position(glm.vec3(value * 0.01, 0, 0))
            self.glwidget.repaint()

        teapot_x.valueChanged.connect(on_teapot_x)
        vbox.addWidget(teapot_x)

        scene.setLayout(vbox)
        self.scene_dock = QtWidgets.QDockWidget("scene", self)
        self.scene_dock.setWidget(scene)
        self.addDockWidget(
            QtCore.Qt.DockWidgetArea.RightDockWidgetArea, self.scene_dock
        )
        self.menubar.addAction(self.scene_dock.toggleViewAction())  # type: ignore

        # logger
        self.logger = glglue.pyside6.QPlainTextEditLogger()
        self.logger_dock = QtWidgets.QDockWidget("logger", self)
        self.logger_dock.setWidget(self.logger)
        self.addDockWidget(
            QtCore.Qt.DockWidgetArea.BottomDockWidgetArea, self.logger_dock
        )
        self.menubar.addAction(self.logger_dock.toggleViewAction())  # type: ignore


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = Window()

    logging.basicConfig(
        level=logging.DEBUG,
        handlers=[
            glglue.pyside6.CustomLogger(window.logger),
        ],
    )

    LOGGER.debug("DEBUG")
    LOGGER.info("INFO!")
    LOGGER.fatal("ERROR!!")

    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
