"""Main entrypoint for terraplanfeed command."""
import logging
import sys
import os
import json

from terraplanfeed.terraform import parsePlan

logger = logging.getLogger(__name__)


def terraplanfeed(filename):
    """Execute terraplanfeed."""

    """Open JSON file"""
    logger.debug("reading file %s", filename)
    with open(filename) as f:
        try:
            tf = json.load(f)
        except ValueError as e:
            logger.error("%s", e)
            sys.exit(1)

    parsePlan(tf)
