# coding: utf-8
'''
pip install pysdl2 pysdl2-dll
'''

def main():
    import glglue.pysdl2
    from glglue.scene.sample import SampleScene

    scene = SampleScene()

    loop = glglue.pysdl2.LoopManager()
    while True:
        frame = loop.begin_frame()
        if not frame:
            break
        scene.render(frame)
        loop.end_frame()


if __name__ == "__main__":
    main()
