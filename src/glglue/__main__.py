import argparse


def install_pyside6():
    import pip

    args = ["install", "pyside6"]

    pip.main(args)


def install_pysdl2():
    import pip

    args = ["install", "pysdl2"]
    import platform

    if platform.system() == "Windows":
        args.append("pysdl2-dll")
    pip.main(args)


def install_glfw():
    import pip

    args = ["install", "glfw"]

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

        install_pysdl2()
    elif args.subparser_name == "glfw":
        import glglue.glfw

        install_glfw()
    elif args.subparser_name == "pyside6":
        try:
            import glglue.pyside6
        except:
            install_pyside6()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
