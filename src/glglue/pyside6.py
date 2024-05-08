import logging
from PySide6 import QtCore, QtGui, QtOpenGLWidgets, QtWidgets
import glglue.frame_input


class Widget(QtOpenGLWidgets.QOpenGLWidget):
    """
    https://doc.qt.io/qtforpython/PySide6/QtOpenGLWidgets/QOpenGLWidget.html
    """

    def __init__(
        self,
        parent: QtWidgets.QWidget | None,
        render_gl: glglue.frame_input.RenderFunc,
        core_profile: bool = True,
    ):
        super().__init__(parent)
        self.setMouseTracking(True)
        self.render_gl = render_gl
        if core_profile:
            format = QtGui.QSurfaceFormat()
            format.setDepthBufferSize(24)
            format.setStencilBufferSize(8)
            format.setVersion(3, 2)
            format.setProfile(QtGui.QSurfaceFormat.CoreProfile)  # type: ignore
            # self.setFormat(format)
            QtGui.QSurfaceFormat.setDefaultFormat(format)
            # must be called before the widget or its parent window gets shown
        self.render_width = 0
        self.render_height = 0
        self.mouse_x = 0
        self.mouse_y = 0
        self.left_down = False
        self.middle_down = False
        self.right_down = False
        self.wheel = 0

    def minimumSizeHint(self) -> QtCore.QSize:
        return QtCore.QSize(50, 50)

    def sizeHint(self) -> QtCore.QSize:
        return QtCore.QSize(150, 150)

    def paintGL(self) -> None:
        self.render_gl(
            glglue.frame_input.FrameInput(
                mouse_x=self.mouse_x,
                mouse_y=self.mouse_y,
                width=self.render_width,
                height=self.render_height,
                mouse_left=self.left_down,
                mouse_middle=self.middle_down,
                mouse_right=self.right_down,
                mouse_wheel=self.wheel,
            )
        )
        self.wheel = 0

    def resizeGL(self, w: int, h: int) -> None:
        ratio = QtGui.QGuiApplication.primaryScreen().devicePixelRatio()
        self.render_width = int(w * ratio)
        self.render_height = int(h * ratio)
        self.repaint()

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        match event.button():
            case QtCore.Qt.LeftButton:  # type: ignore
                self.left_down = True
                self.repaint()
            case QtCore.Qt.MiddleButton:  # type: ignore
                self.middle_down = True
                self.repaint()
            case QtCore.Qt.RightButton:  # type: ignore
                self.right_down = True
                self.repaint()
            case _:
                pass

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        match event.button():
            case QtCore.Qt.LeftButton:  # type: ignore
                self.left_down = False
                self.repaint()
            case QtCore.Qt.MiddleButton:  # type: ignore
                self.middle_down = False
                self.repaint()
            case QtCore.Qt.RightButton:  # type: ignore
                self.right_down = False
                self.repaint()
            case _:
                pass

    def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:
        self.mouse_x = event.x()
        self.mouse_y = event.y()
        self.repaint()

    def wheelEvent(self, event: QtGui.QWheelEvent) -> None:
        self.wheel = event.angleDelta().y()
        self.repaint()


class QPlainTextEditLogger(QtWidgets.QPlainTextEdit):
    def __init__(self, parent: QtWidgets.QWidget | None = None):
        super().__init__(parent)
        self.setReadOnly(True)
        self.log_handler = CustomLogger(self)


class CustomLogger(logging.Handler):
    """
    CRITICAL: int
    FATAL: int
    ERROR: int
    WARNING: int
    WARN: int
    INFO: int
    DEBUG: int
    """

    def __init__(self, widget: QPlainTextEditLogger):
        super().__init__()
        self.widget = widget

    def emit(self, record: logging.LogRecord) -> None:
        msg = self.format(record)

        match record.levelno:
            case logging.DEBUG:
                msg = f'<font color="gray">{msg}</font><br>'
            case logging.WARNING:
                msg = f'<font color="orange">{msg}</font><br>'
            case logging.ERROR | logging.FATAL | logging.CRITICAL:
                msg = f'<font color="red">{msg}</font><br>'
            case _:
                msg = f"{msg}<br>"

        # self.widget.textCursor().movePosition(
        #     QtGui.QTextCursor.Start, QtGui.QTextCursor.KeepAnchor
        # )
        cursor = self.widget.textCursor()
        cursor.setPosition(0)
        self.widget.setTextCursor(cursor)
        self.widget.textCursor().insertHtml(msg)
