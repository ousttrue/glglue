# -*- coding: utf-8 -*-
from typing import Callable
import logging
from PySide6 import QtCore, QtGui, QtOpenGLWidgets, QtWidgets
import glglue.frame_input


class Widget(QtOpenGLWidgets.QOpenGLWidget):
    """
    https://doc.qt.io/qtforpython/PySide6/QtOpenGLWidgets/QOpenGLWidget.html
    """

    def __init__(
        self,
        parent,
        render_gl: glglue.frame_input.RenderFunc,
        core_profile=True,
    ):
        super().__init__(parent)
        self.setMouseTracking(True)
        self.render_gl = render_gl
        if core_profile:
            format = QtGui.QSurfaceFormat()
            format.setDepthBufferSize(24)
            format.setStencilBufferSize(8)
            format.setVersion(3, 2)
            format.setProfile(QtGui.QSurfaceFormat.CoreProfile)
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
        self.render_wheel = 0

    def minimumSizeHint(self):
        return QtCore.QSize(50, 50)

    def sizeHint(self):
        return QtCore.QSize(150, 150)

    def paintGL(self):
        self.render_gl(
            glglue.frame_input.FrameInput(
                mouse_x=self.mouse_x,
                mouse_y=self.mouse_y,
                width=self.render_width,
                height=self.render_height,
                mouse_left=self.left_down,
                mouse_middle=self.middle_down,
                mouse_right=self.right_down,
                mouse_wheel=self.render_wheel,
            )
        )
        self.render_wheel = 0

    def resizeGL(self, width, height):
        ratio = QtGui.QGuiApplication.primaryScreen().devicePixelRatio()
        self.render_width = int(width * ratio)
        self.render_height = int(height * ratio)
        self.repaint()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.left_down = True
            self.repaint()
        elif event.button() == QtCore.Qt.MiddleButton:
            self.middle_down = True
            self.repaint()
        elif event.button() == QtCore.Qt.RightButton:
            self.right_down = True
            self.repaint()

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.left_down = False
            self.repaint()
        elif event.button() == QtCore.Qt.MiddleButton:
            self.middle_down = False
            self.repaint()
        elif event.button() == QtCore.Qt.RightButton:
            self.right_down = False
            self.repaint()

    def mouseMoveEvent(self, event):
        self.mouse_x = event.x()
        self.mouse_y = event.y()
        self.repaint()

    def wheelEvent(self, event):
        self.wheel = event.angleDelta().y()


class CustomLogger(logging.Handler):
    def __init__(self, widget):
        super().__init__()
        self.widget = widget

    def emit(self, record):
        msg = self.format(record)

        if record.levelno == logging.DEBUG:
            msg = f'<font color="gray">{msg}</font><br>'
        elif record.levelno == logging.WARNING:
            msg = f'<font color="orange">{msg}</font><br>'
        elif record.levelno == logging.ERROR:
            msg = f'<font color="red">{msg}</font><br>'
        else:
            msg = f"{msg}<br>"

        self.widget.textCursor().movePosition(QtGui.QTextCursor.Start)
        self.widget.textCursor().insertHtml(msg)

    def write(self, m):
        pass


class QPlainTextEditLogger(QtWidgets.QPlainTextEdit):
    def __init__(self, parent):
        super().__init__(parent)
        self.setReadOnly(True)
        self.log_handler = CustomLogger(self)
