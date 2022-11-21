import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

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
                    width=self.get_width(),
                    height=self.get_height(),
                    mouse_left=self.left_down,
                    mouse_middle=self.middle_down,
                    mouse_right=self.right_down,
                    mouse_wheel=self.wheel,
                )
            )
            self.wheel = 0

        self.connect("render", on_draw)

        # motion
        motion_controller = Gtk.EventControllerMotion.new()

        def on_motion(c, x, y):
            self.mouse_x = x
            self.mouse_y = y
            self.queue_render()

        motion_controller.connect("motion", on_motion)
        self.add_controller(motion_controller)

        # left
        left_click_controller = Gtk.GestureClick()
        left_click_controller.set_button(1)

        def on_left_down(*args):
            self.left_down = True
            self.queue_render()

        def on_left_up(*args):
            self.left_down = False
            self.queue_render()

        left_click_controller.connect("pressed", on_left_down)
        left_click_controller.connect("released", on_left_up)
        self.add_controller(left_click_controller)

        # middle
        middle_click_controller = Gtk.GestureClick()
        middle_click_controller.set_button(2)

        def on_middle_down(*args):
            self.middle_down = True
            self.queue_render()

        def on_middle_up(*args):
            self.middle_down = False
            self.queue_render()

        middle_click_controller.connect("pressed", on_middle_down)
        middle_click_controller.connect("released", on_middle_up)
        self.add_controller(middle_click_controller)

        # right
        right_click_controller = Gtk.GestureClick()
        right_click_controller.set_button(3)

        def on_right_down(*args):
            self.right_down = True
            self.queue_render()

        def on_right_up(*args):
            self.right_down = False
            self.queue_render()

        right_click_controller.connect("pressed", on_right_down)
        right_click_controller.connect("released", on_right_up)
        self.add_controller(right_click_controller)

        # wheel
        wheel_controller = Gtk.EventControllerScroll()
        wheel_controller.set_flags(Gtk.EventControllerScrollFlags.VERTICAL)

        def on_wheel(c, x, y):
            self.wheel = -y
            self.queue_render()

        wheel_controller.connect("scroll", on_wheel)
        self.add_controller(wheel_controller)
