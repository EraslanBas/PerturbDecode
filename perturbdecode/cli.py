# Command-line interface
"""
Command-line interface for PerturbDecode.

Examples
--------
::

    perturbdecode --version
    perturbdecode list-steps
"""

import argparse
import sys

PROG = "perturbdecode"


def main(argv=None):
    """Main entry point for the CLI.

    Parameters
    ----------
    argv : list of str, optional
        Argument vector to parse. Defaults to ``sys.argv[1:]``.

    Returns
    -------
    int
        Process exit status; ``0`` on success.
    """
    from . import __version__

    parser = argparse.ArgumentParser(
        prog=PROG,
        description="PerturbDecode - end-to-end analysis of single-cell perturbation screens",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"{PROG} {__version__}",
        help="Print version information and exit",
    )

    sub = parser.add_subparsers(dest="command", metavar="<command>")
    sub.add_parser("list-steps", help="List the available pipeline steps")

    args = parser.parse_args(argv)

    if args.command == "list-steps":
        from . import pertdec

        for name in pertdec.__all__:
            fn = getattr(pertdec, name, None)
            summary = ""
            if fn is not None and fn.__doc__:
                summary = fn.__doc__.strip().splitlines()[0]
            print(f"  {name:38s} {summary}")
        return 0

    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
