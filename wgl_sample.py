#import glglue.sample
import controller_sample
import glglue.wgl

if __name__=="__main__":
    controller=controller_sample.Controller()
    glglue.wgl.mainloop(controller, width=640, height=480, title=b"sample")

