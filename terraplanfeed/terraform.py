"""Terraform handler."""
import logging

logger = logging.getLogger(__name__)


def resourceChanges(tfplan):
    """Parse Terraform plan in JSON"""

    logger.debug("processing changes...")
    for r in tfplan["resource_changes"]:
        print(r["address"])
