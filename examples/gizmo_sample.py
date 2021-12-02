#
# pip install pyside6
#
from PySide6 import QtWidgets, QtGui, QtCore
import logging
from glglue.ctypesmath.camera import FrameState
import glglue.gl3.samplecontroller
from glglue.gl3 import gizmo
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(levelname)s:%(name)s:%(message)s',
                    level=logging.DEBUG)


class Scene(glglue.gl3.samplecontroller.BaseScene):
    def __init__(self) -> None:
        self.gizmo = gizmo.Gizmo()

    def update(self, d: int):
        return True

    def draw(self, state: FrameState):
        self.gizmo.begin(state)
        self.gizmo.axis(10)

        if self.gizmo.bone('bone1', 1):
            logger.info('bone clicked')

        self.gizmo.end()


class Window(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        # setup opengl widget
        self.setWindowTitle('gizmo_sample')
        import glglue.gl3.samplecontroller
        self.controller = glglue.gl3.samplecontroller.SampleController()
        self.scene = Scene()
        self.controller.scene = self.scene  # type: ignore
        import glglue.pyside6
        import glglue.utils
        self.glwidget = glglue.pyside6.Widget(
            self, self.controller, glglue.utils.get_desktop_scaling_factor())
        self.setCentralWidget(self.glwidget)

        # render loop
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.glwidget.update)
        self.timer.start(33)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
