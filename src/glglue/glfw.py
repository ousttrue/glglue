import glfw
import logging
from OpenGL import GL
from .basecontroller import BaseController

logger = logging.getLogger(__name__)


class LoopManager:
    def __init__(
            self, controller: BaseController, *,
            title: str = 'glfw',
            width: int = 1280,
            height: int = 720):
        self.controller = controller
        self.x = 0
        self.y = 0

        if not glfw.init():
            logger.error("Could not initialize OpenGL context")
            return

        # OS X supports only forward-compatible core profiles from 3.2
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 2)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL.GL_TRUE)

        # Create a windowed mode window and its OpenGL context
        self.window = glfw.create_window(
            width, height, title, None, None
        )
        if not self.window:
            logger.error("Could not initialize Window")
            return

        glfw.make_context_current(self.window)
        glfw.swap_interval(1)
        glfw.set_key_callback(self.window, self.keyboard_callback)
        glfw.set_cursor_pos_callback(self.window, self.cursor_calblack)
        glfw.set_mouse_button_callback(self.window, self.mouse_callback)
        glfw.set_window_size_callback(self.window, self.resize_callback)
        glfw.set_char_callback(self.window, self.char_callback)
        glfw.set_scroll_callback(self.window, self.scroll_callback)
        self.controller.onResize(width, height)

    def __del__(self):
        del self.controller
        glfw.terminate()

    def keyboard_callback(self, window, key, scancode, action, mods):
        pass
        # if action == glfw.PRESS:
        #     io.KeysDown[key] = True
        # elif action == glfw.RELEASE:
        #     io.KeysDown[key] = False

        # io.KeyCtrl = (
        #     io.KeysDown[glfw.KEY_LEFT_CONTROL] or
        #     io.KeysDown[glfw.KEY_RIGHT_CONTROL]
        # )

        # io.KeyAlt = (
        #     io.KeysDown[glfw.KEY_LEFT_ALT] or
        #     io.KeysDown[glfw.KEY_RIGHT_ALT]
        # )

        # io.KeyShift = (
        #     io.KeysDown[glfw.KEY_LEFT_SHIFT] or
        #     io.KeysDown[glfw.KEY_RIGHT_SHIFT]
        # )

        # io.KeySuper = (
        #     io.KeysDown[glfw.KEY_LEFT_SUPER] or
        #     io.KeysDown[glfw.KEY_RIGHT_SUPER]
        # )

    def char_callback(self, window, char):
        pass
        # if 0 < char < 0x10000:
        #     self.io.add_input_character(char)

    def resize_callback(self, window, width, height):
        self.controller.onResize(width, height)

    def cursor_calblack(self, window, x, y):
        self.controller.onMotion(x, y)
        self.x = x
        self.y = y

    def mouse_callback(self, window,  button, action, mods):
        match button, action:
            case glfw.MOUSE_BUTTON_LEFT, glfw.PRESS:
                self.controller.onLeftDown(self.x, self.y)
            case glfw.MOUSE_BUTTON_LEFT, glfw.RELEASE:
                self.controller.onLeftUp(self.x, self.y)
            case glfw.MOUSE_BUTTON_RIGHT, glfw.PRESS:
                self.controller.onRightDown(self.x, self.y)
            case glfw.MOUSE_BUTTON_RIGHT, glfw.RELEASE:
                self.controller.onRightUp(self.x, self.y)
            case glfw.MOUSE_BUTTON_MIDDLE, glfw.PRESS:
                self.controller.onMiddleDown(self.x, self.y)
            case glfw.MOUSE_BUTTON_MIDDLE, glfw.RELEASE:
                self.controller.onMiddleUp(self.x, self.y)

    def scroll_callback(self, window, x_offset, y_offset):
        self.controller.onWheel(-y_offset)

    def begin_frame(self):
        if glfw.window_should_close(self.window):
            return None
        glfw.poll_events()
        return glfw.get_time() * 1000

    def end_frame(self):
        glfw.swap_buffers(self.window)
