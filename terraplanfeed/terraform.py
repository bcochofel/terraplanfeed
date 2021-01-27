"""Terraform handler."""
import logging

logger = logging.getLogger(__name__)


def parseJson(data):
    """Parse Terraform plan in JSON"""

    logger.debug("processing changes...")
    for r in data["resource_changes"]:
        print(r["address"])
