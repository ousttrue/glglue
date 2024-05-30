import time
import tkinter
from OpenGL import GL


import glglue.frame_input


class AppOgl(OpenGLFrame):

    def __init__(self, **kw):
        super().__init__(**kw)
        from glglue.scene.sample import SampleScene

        self.scene = SampleScene()

    def initgl(self):
        """Initalize gl states when the frame is created"""
        self.start = time.time()
        self.nframes = 0

    def redraw(self):
        """Render a single frame"""
        self.scene.render(
            glglue.frame_input.FrameInput(
                mouse_x=0,
                mouse_y=,
                width=self.render_width,
                height=self.render_height,
                mouse_left=self.left_down,
                mouse_middle=self.middle_down,
                mouse_right=self.right_down,
                mouse_wheel=self.wheel,
            )
        )
        GL.glViewport(0, 0, self.width, self.height)  # type: ignore
        GL.glClearColor(0.0, 1.0, 0.0, 0.0)  # type: ignore
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)  # type: ignore
        tm = time.time() - self.start
        self.nframes += 1
        print("fps", self.nframes / tm, end="\r")


if __name__ == "__main__":
    root = tkinter.Tk()
    app = AppOgl(root, width=320, height=200)
    app.pack(fill=tkinter.BOTH, expand=tkinter.YES)
    app.animate = 1
    app.after(100, app.printContext)
    app.mainloop()
