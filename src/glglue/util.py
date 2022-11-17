from typing import NamedTuple
from OpenGL import GL


def get_info():
    from OpenGL.GL import (
        glGetString,
        glGetIntegerv,
        GL_VENDOR,
        GL_VERSION,
        GL_SHADING_LANGUAGE_VERSION,
        GL_RENDERER,
        GL_MAJOR_VERSION,
        GL_MINOR_VERSION,
    )

    return {
        "major": glGetIntegerv(GL_MAJOR_VERSION),
        "minor": glGetIntegerv(GL_MINOR_VERSION),
        "vendor": glGetString(GL_VENDOR),
        "version": glGetString(GL_VERSION),
        "shader_language_version": glGetString(GL_SHADING_LANGUAGE_VERSION),
        "renderer": glGetString(GL_RENDERER),
    }


class GLContextHint(NamedTuple):
    major: int = 4
    minor: int = 5
    core_profile: bool = True
    compatible: bool = False


def get_desktop_scaling_factor():
    """
    for high DPI desktop
    """
    import platform

    if platform.platform().startswith("Windows"):
        from ctypes import windll

        desktop = windll.user32.GetDC(0)
        LogicalScreenHeight = windll.gdi32.GetDeviceCaps(desktop, 10)  # VERTRES
        PhysicalScreenHeight = windll.gdi32.GetDeviceCaps(
            desktop, 117
        )  # DESKTOPVERTRES
        return PhysicalScreenHeight / LogicalScreenHeight

    return 1


class DummyScene:
    def __init__(self) -> None:
        pass

    def resize(self, w, h):
        GL.glViewport(0, 0, w, h)

    def draw(self):
        GL.glClearColor(1, 0, 1, 1)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)
