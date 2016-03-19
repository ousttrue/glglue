import glglue.sample
import glglue.wgl

if __name__=="__main__":
    controller=glglue.sample.SampleController()
    glglue.wgl.mainloop(controller, width=640, height=480, title=b"sample")

