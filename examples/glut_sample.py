# coding: utf-8
if __name__ == "__main__":
    import glglue.gl3
    controller = glglue.gl3.SampleController()

    import glglue.glut
    glglue.glut.mainloop(controller)
