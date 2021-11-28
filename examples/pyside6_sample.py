#
# pip install pyside6
#
from PySide6 import QtWidgets, QtGui
import logging

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

        # logger
        self.log_handler = glglue.pyside6.QPlainTextEditLogHandler(self)
        logging.getLogger('').addHandler(self.log_handler)
        self.dock_bottom = QtWidgets.QDockWidget("logger", self)
        self.addDockWidget(QtGui.Qt.BottomDockWidgetArea, self.dock_bottom)
        self.dock_bottom.setWidget(self.log_handler)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
