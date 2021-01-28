"""Terraform handler.

Check https://www.terraform.io/docs/internals/json-format.html
for more info
"""
import logging

logger = logging.getLogger(__name__)


def getResourceChanges(data):
    """Filter Resource Changes from Plan."""

    logger.debug("filter resource_changes from plan")
    if "resource_changes" in data.keys():
        return data["resource_changes"]
    else:
        logger.error("no resource_changes found")
        return []


def filterNoOp(data):
    """Filter no-op actions."""

    changes = []
    logger.debug("filter no-op actions")
    for res in data:
        if res["change"]["actions"] != ["no-op"]:
            changes.append(res)

    return changes


def parseResource(data):
    """Parse Resource to retrive elements"""

    logger.debug("retrieve elements from resource")
    rc = {"address": data["address"], "actions": data["change"]["actions"]}
    return rc


def getAttributes(data):
    """Get attributes from resource"""

    resources = []
    logger.debug("get attributes from resources")
    for res in data:
        resources.append(parseResource(res))
    return resources


def parsePlan(tfplan):
    """Parse Terraform plan in JSON"""

    logger.debug("parsing file...")

    all_resources = getResourceChanges(tfplan)
    # print(all_resources)

    resource_changing = filterNoOp(all_resources)
    # print(resource_changing)

    resources = getAttributes(resource_changing)
    print(resources)
