class Window(QMainWindow):
    def __init__(self):
        super().__init__(None)
        import glglue.pyside6
        from glglue.scene.sample import SampleScene

        self.scene = SampleScene()

        self.glwidget = glglue.pyside6.Widget(self, render_gl=self.scene.render)
        self.setCentralWidget(self.glwidget)
