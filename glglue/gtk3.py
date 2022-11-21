import gi

gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")
from gi.repository import Gtk, Gdk

import glglue.frame_input


class GLArea(Gtk.GLArea):
    def __init__(self, render_callback: glglue.frame_input.RenderFunc) -> None:
        super().__init__()

        self.mouse_x = 0
        self.mouse_y = 0
        self.left_down = False
        self.middle_down = False
        self.right_down = False
        self.wheel = 0

        def on_draw(*args):
            render_callback(
                glglue.frame_input.FrameInput(
                    mouse_x=self.mouse_x,
                    mouse_y=self.mouse_y,
                    width=self.get_allocated_width(),
                    height=self.get_allocated_height(),
                    mouse_left=self.left_down,
                    mouse_middle=self.middle_down,
                    mouse_right=self.right_down,
                    mouse_wheel=self.wheel,
                )
            )
            self.wheel = 0

        self.connect("render", on_draw)
        self.set_double_buffered(False)

        # motion
        self.add_events(
            Gdk.EventMask.POINTER_MOTION_MASK
            | Gdk.EventMask.BUTTON_PRESS_MASK
            | Gdk.EventMask.BUTTON_RELEASE_MASK
            | Gdk.EventMask.SCROLL_MASK
        )

        def on_motion(w, e: Gdk.EventButton):
            self.mouse_x = e.x
            self.mouse_y = e.y
            self.queue_render()

        self.connect("motion-notify-event", on_motion)

        # button press
        def on_press(w, e: Gdk.EventButton):
            match e.button:
                case 1:
                    self.left_down = True
                case 2:
                    self.middle_down = True
                case 3:
                    self.right_down = True
            self.queue_render()

        self.connect("button-press-event", on_press)

        # button release
        def on_release(w, e: Gdk.EventButton):
            match e.button:
                case 1:
                    self.left_down = False
                case 2:
                    self.middle_down = False
                case 3:
                    self.right_down = False
            self.queue_render()

        self.connect("button-release-event", on_release)

        # wheel
        def on_wheel(w, e: Gdk.EventScroll):
            match e.direction:
                case Gdk.ScrollDirection.UP:
                    self.wheel = 1
                case Gdk.ScrollDirection.DOWN:
                    self.wheel = -1
            self.queue_render()

        self.connect("scroll-event", on_wheel)
