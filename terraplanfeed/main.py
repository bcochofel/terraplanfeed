"""Main entrypoint for terraplanfeed command."""
import logging
import sys
import os
import json

from terraplanfeed.terraform import parseJson

logger = logging.getLogger(__name__)


def terraplanfeed(filename):
    """Execute terraplanfeed."""

    """Open JSON file"""
    logger.debug("parsing file %s", filename)
    with open(filename) as f:
        try:
            data = json.load(f)
        except json.decoder.JSONDecodeError:
            logger.debug("%s", sys.exc_info())
            sys.exit(1)

    parseJson(data)
