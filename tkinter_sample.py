import sys
import tkinter
import glglue.togl
import glglue.sample
class Frame(tkinter.Frame):
    def __init__(self, width, height, master=None, **kw):
        #super(Frame, self).__init__(master, **kw)
        tkinter.Frame.__init__(self, master, **kw)
        # setup opengl widget
        self.controller=glglue.sample.SampleController()
        self.glwidget=glglue.togl.Widget(
                self, self.controller, width=width, height=height)
        self.glwidget.pack(fill=tkinter.BOTH, expand=True)
        # event binding(require focus)
        self.bind('<Key>', self.onKeyDown)
        self.bind('<MouseWheel>', lambda e: self.controller.onWheel(-e.delta) and self.glwidget.onDraw())

    def onKeyDown(self, event):
        key=event.keycode
        if key==27:
            # Escape
            sys.exit()
        if key==81:
            # q
            sys.exit()
        else:
            print("keycode: %d" % key)

f = Frame(width=600, height=600)
f.pack(fill=tkinter.BOTH, expand=True)
f.focus_set()
f.mainloop()

