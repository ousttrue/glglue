import argparse


def install_packages(pkg):
    import pip

    args = ["install", pkg]
    import platform

    pip.main(args)


def main():
    parser = argparse.ArgumentParser(prog="glglue dll installer")

    subparsers = parser.add_subparsers(dest="subparser_name")

    parser_pysdl = subparsers.add_parser("pysdl2")
    parser_glfw = subparsers.add_parser("glfw")
    parser_gyside6 = subparsers.add_parser("pyside6")

    args = parser.parse_args()
    if args.subparser_name == "pysdl2":
        import glglue.pysdl2

        glglue.pysdl2.install_packages()
    elif args.subparser_name == "glfw":
        import glglue.glfw

        glglue.glfw.install_packages()
    elif args.subparser_name == "pyside6":
        try:
            import glglue.pyside6
        except:
            install_packages("pyside6")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
