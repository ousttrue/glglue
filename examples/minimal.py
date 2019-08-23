import pathlib
import sys
sys.path.insert(0, str(pathlib.Path(__file__).parents[1]))

def main():
    import glglue.sample
    # import glglue.wgl as gg
    # import glglue.pysdl2 as gg
    import glglue.glut as gg
    gg.mainloop(glglue.sample.SampleController())

if __name__ == '__main__':
    main()
