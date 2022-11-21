import argparse


def main():
    parser = argparse.ArgumentParser(prog="glglue dll installer")

    subparsers = parser.add_subparsers(dest="subparser_name")

    parser_pysdl = subparsers.add_parser("pysdl2")
    parser_glfw = subparsers.add_parser("glfw")

    args = parser.parse_args()
    if args.subparser_name == "pysdl2":
        import glglue.pysdl2

        glglue.pysdl2.install_packages()
    if args.subparser_name == "glfw":
        import glglue.glfw

        glglue.glfw.install_packages()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
