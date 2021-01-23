"""Main terraformfeed cli."""
import os
import sys

import click
from terraplanfeed import __version__


def version_msg():
    """Return the Terraplanfeed version, location and Python powering it."""
    python_version = sys.version[:3]
    location = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    message = "Terraplanfeed %(version)s from {} (Python {})"
    return message.format(location, python_version)


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.version_option(__version__, "-v", "--version", message=version_msg())
def main():
    """Handle arguments."""
    pass


if __name__ == "__main__":
    main()
