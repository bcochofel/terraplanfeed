"""Terraform handler.

Check https://www.terraform.io/docs/internals/json-format.html
for more info
"""
import logging

logger = logging.getLogger(__name__)


def resourceChanges(tfplan):
    """Parse Terraform plan in JSON"""

    logger.debug("processing changes...")
    for r in tfplan["resource_changes"]:
        print(r["address"])
