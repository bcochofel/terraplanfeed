"""Entry point for package."""

import os
import sys
import json
import click

from terraplanfeed import __version__


def version_msg():
    """Return the Terraplanfeed version, location and Python powering it."""
    python_version = sys.version[:3]
    location = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    message = "Terraplanfeed %(version)s from {} (Python {})"
    return message.format(location, python_version)


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.version_option(__version__, "-V", "--version", message=version_msg())
@click.argument("filename", type=click.Path(exists=True))
def main(filename):
    """Parse Terraform plan in JSON format."""
    #    click.echo("Terraform JSON file: %s" % filename)

    """Open JSON file"""
    with open(filename) as f:
        data = json.load(f)
    # print(data["resource_changes"])
    for r in data["resource_changes"]:
        print(r["address"])
