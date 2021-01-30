"""
Entry point for package.

Arguments:
    -h, --help: prints help
    -V, --version: prints version, location and python powering it
    <filename> (required): terraform plan in json format
    -v, --verbose: prints debug information
    -d, --debug-file: filename to print debug information
"""

import os
import sys
import click

from terraplanfeed import __version__
from terraplanfeed.log import configure_logger
from terraplanfeed.main import terraplanfeed


def version_msg():
    """Return the Terraplanfeed version, location and Python powering it."""
    python_version = sys.version[:3]
    location = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    message = "Terraplanfeed %(version)s from {} (Python {})"
    return message.format(location, python_version)


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.version_option(__version__, "-V", "--version", message=version_msg())
@click.argument("filename", type=click.Path(exists=True))
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    help="Print debug information",
    default=False,
)
@click.option(
    "-d",
    "--debug-file",
    type=click.Path(),
    default=None,
    help="Print debug information to this file",
)
def main(filename, verbose, debug_file):
    """Parse Terraform plan in JSON format."""

    configure_logger(
        stream_level="DEBUG" if verbose else "INFO", debug_file=debug_file
    )

    terraplanfeed(filename)


if __name__ == "__main__":
    main()
