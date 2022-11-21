# coding: utf-8
import glglue.frame_input


def main():
    import glglue.pysdl2
    from glglue.scene.triangle import TriangleScene

    scene = TriangleScene()

    loop = glglue.pysdl2.LoopManager()
    while True:
        frame = loop.begin_frame()
        if not frame:
            break
        scene.render(frame)
        loop.end_frame()


if __name__ == "__main__":
    main()
