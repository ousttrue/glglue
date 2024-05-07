# coding: utf-8
"""
https://github.com/mcfletch/pyopengl/tree/master/OpenGL/DLLS

environment variable PATH to freeglut64.vc14.dll
"""


def main():

    import glglue.glut
    from glglue.scene.sample import SampleScene

    scene = SampleScene()

    # manual loop
    loop = glglue.glut.LoopManager()
    while True:
        # require freeglut glutMainLoopEvent
        frame = loop.begin_frame()
        if not frame:
            break
        scene.render(frame)
        loop.end_frame()


if __name__ == "__main__":
    main()
