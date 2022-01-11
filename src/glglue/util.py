from typing import NamedTuple


def get_info():
    from OpenGL.GL import (glGetString, glGetIntegerv, GL_VENDOR, GL_VERSION,
                           GL_SHADING_LANGUAGE_VERSION, GL_RENDERER,
                           GL_MAJOR_VERSION, GL_MINOR_VERSION)
    return {
        'major': glGetIntegerv(GL_MAJOR_VERSION),
        'minor': glGetIntegerv(GL_MINOR_VERSION),
        'vendor': glGetString(GL_VENDOR),
        'version': glGetString(GL_VERSION),
        'shader_language_version': glGetString(GL_SHADING_LANGUAGE_VERSION),
        'renderer': glGetString(GL_RENDERER),
    }


class GLContextHint(NamedTuple):
    major: int = 4
    minor: int = 5
    core_profile: bool = True
    compatible: bool = False
