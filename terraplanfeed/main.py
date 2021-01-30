"""
Main entrypoint for terraplanfeed command.

Main code execution for terraplanfeed command.

Functions:
    terraplanfeed: main code execution
"""
import logging
import sys
import os
import json

from terraplanfeed.terraform import parsePlan
import terraplanfeed.stdout as stdout
import terraplanfeed.azuredevops as azuredevops

logger = logging.getLogger(__name__)


def terraplanfeed(filename, output):
    """
    Execute terraplanfeed.

    Args:
        filename: Terraform plan in JSON format
        output: output driver to write feedback
    """

    """Open JSON file"""
    logger.debug("reading file %s", filename)
    with open(filename) as f:
        try:
            tf = json.load(f)
        except ValueError as e:
            logger.error("%s", e)
            sys.exit(1)

    resources = parsePlan(tf)

    if output.lower() == "azuredevops":
        azuredevops.main(resources)
    else:
        stdout.main(resources)
