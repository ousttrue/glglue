from PySide6 import QtWidgets, QtCore
import sys
import logging
import glglue.pyside6


LOGGER = logging.getLogger(__name__)


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__(None)
        self.menubar = self.menuBar()
        self.menubar.setNativeMenuBar(False)

        # status bar
        self.sb = self.statusBar()
        # self.sb.showMessage("")

        # central
        from .scene import SampleScene

        self.scene = SampleScene()

        self.glwidget = glglue.pyside6.Widget(self, render_gl=self.scene.render)
        self.setCentralWidget(self.glwidget)

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
