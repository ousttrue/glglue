import logging

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(levelname)s:%(name)s:%(message)s',
                    level=logging.DEBUG)

# pip install pyside6
from PySide6.QtWidgets import QMainWindow, QApplication
from OpenGL.GL import *


class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        # setup opengl widget
        import glglue.gl3
        self.controller = glglue.gl3.SampleController()
        import glglue.pyside6
        self.glwidget = glglue.pyside6.Widget(self, self.controller)
        self.setCentralWidget(self.glwidget)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
