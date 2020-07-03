import argparse

from fimed import __version__, __author__

HEADER = "\n".join(
    [
        r"  ______   __     __    __     ______     _____    ",
        r' /\  ___\ /\ \   /\ "-./  \   /\  ___\   /\  __-.  ',
        r" \ \  __\ \ \ \  \ \ \-./\ \  \ \  __\   \ \ \/\ \ ",
        r"  \ \_\    \ \_\  \ \_\ \ \_\  \ \_____\  \ \____- ",
        r"   \/_/     \/_/   \/_/  \/_/   \/_____/   \/____/ ",
        "                                                    ",
        f" ver. {__version__}     author {__author__}        ",
        "                                                    ",
    ]
)


def get_parser():
    parser = argparse.ArgumentParser(prog="FIMED")

    subparsers = parser.add_subparsers(dest="command", help="FIMED sub-commands")
    subparsers.required = True

    subparsers.add_parser("deploy", help="Deploy server")

    return parser


def cli():
    print(HEADER)
    args, _ = get_parser().parse_known_args()

    if args.command == "deploy":
        from fimed.app import run_server

        run_server()


if __name__ == "__main__":
    cli()
