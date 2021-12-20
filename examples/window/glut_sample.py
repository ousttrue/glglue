# coding: utf-8
if __name__ == "__main__":
    import glglue.gl3.samplecontroller
    controller = glglue.gl3.samplecontroller.SampleController()

    import glglue.glut
    glglue.glut.mainloop(controller)
