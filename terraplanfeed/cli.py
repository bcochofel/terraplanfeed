"""
Entry point for package.

Arguments:
    -h, --help: prints help
    -V, --version: prints version, location and python powering it
    <filename> (required): terraform plan in json format
    -v, --verbose: prints debug information
    -d, --debug-file: filename to print debug information
    -o, --output: output driver
"""

import os
import sys
import click

from envparse import Env

from terraplanfeed import __version__
from terraplanfeed.log import configure_logger
from terraplanfeed.main import terraplanfeed

env = Env(
    SYSTEM_TEAMFOUNDATIONSERVERURI=dict(cast=str, default=""),
    SYSTEM_TEAMPROJECT=dict(cast=str, default=""),
    BUILD_REPOSITORY_ID=dict(cast=str, default=""),
    SYSTEM_PULLREQUEST_PULLREQUESTID=dict(cast=str, default=""),
    SYSTEM_ACCESSTOKEN=dict(cast=str, default=""),
    AZDO_API_VERSION=dict(cast=str, default="6.0"),
)
# env.read_envfile()


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
@click.option(
    "-o",
    "--output",
    type=click.Choice(["stdout", "azuredevops"], case_sensitive=False),
    default="stdout",
    help="Output driver",
)
@click.option(
    "--azdo-organization",
    default=env.str("SYSTEM_TEAMFOUNDATIONSERVERURI"),
    help="Azure DevOps Organization Service URL",
)
@click.option(
    "--azdo-project",
    default=env.str("SYSTEM_TEAMPROJECT"),
    help="Azure DevOps Project",
)
@click.option(
    "--azdo-repository",
    default=env.str("BUILD_REPOSITORY_ID"),
    help="Azure DevOps Repository ID",
)
@click.option(
    "--azdo-pullrequest",
    default=env.str("SYSTEM_PULLREQUEST_PULLREQUESTID"),
    help="Azure DevOps Pull Request ID (used to comment PR)",
)
@click.option(
    "--azdo-pat",
    default=env.str("SYSTEM_ACCESSTOKEN"),
    help="Personal Access Token",
)
@click.option(
    "--azdo-apiversion",
    default=env.str("AZDO_API_VERSION"),
    help="Azure DevOps API Version",
)
def main(
    filename,
    verbose,
    debug_file,
    output,
    azdo_organization,
    azdo_project,
    azdo_repository,
    azdo_pullrequest,
    azdo_pat,
    azdo_apiversion,
):
    """Parse Terraform plan in JSON format."""

    configure_logger(
        stream_level="DEBUG" if verbose else "INFO", debug_file=debug_file
    )

    azdo_params = {
        "organization": azdo_organization,
        "project": azdo_project,
        "repository": azdo_repository,
        "pullrequest": azdo_pullrequest,
        "accesstoken": azdo_pat,
        "apiversion": azdo_apiversion,
    }

    terraplanfeed(filename, output, azdo_params)


if __name__ == "__main__":
    main()
