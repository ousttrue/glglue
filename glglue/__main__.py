import argparse


def main():
    parser = argparse.ArgumentParser(prog="glglue dll installer")

    subparsers = parser.add_subparsers(dest="subparser_name")

    parser_pysdl = subparsers.add_parser("pysdl2")

    args = parser.parse_args()
    if args.subparser_name == "pysdl2":
        import glglue.pysdl2

        glglue.pysdl2.install_packages()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
