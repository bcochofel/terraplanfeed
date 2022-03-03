"""
Main entrypoint for terraplanfeed command.

Main code execution for terraplanfeed command.

Functions:
    terraplanfeed: main code execution
"""
import logging
import sys
import json

from terraplanfeed.terraform import parsePlan
from terraplanfeed.stdout import generate_stdout
from terraplanfeed.azuredevops import generate_pr_comment

logger = logging.getLogger(__name__)


def terraplanfeed(filename, output, azdo, textonly, drift, detailed_exitcode):
    """
    Execute terraplanfeed.

    Args:
        filename(str): Terraform plan in JSON format
        output(str): output driver to write feedback
        azdo(dict): Azure DevOps parameters
        textonly(bool): Disable emoji
        drift(bool): Flag denoting drift mode
        detailed_exitcode(bool): Return detailed exit codes

    Returns:
        Boolean
    """

    """Open JSON file"""
    logger.debug("reading file %s", filename)
    with open(filename) as f:
        try:
            tf = json.load(f)
        except ValueError as e:
            logger.error("%s", e)
            sys.exit(1)

    resources = parsePlan(tf, drift)

    if output.lower() == "azuredevops":
        generate_pr_comment(resources, azdo, textonly, drift)
    else:
        generate_stdout(resources, textonly, drift, detailed_exitcode)
