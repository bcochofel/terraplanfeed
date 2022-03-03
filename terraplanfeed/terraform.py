"""Terraform handler.

This module handles terraform plan in json output format.

Check https://www.terraform.io/docs/internals/json-format.html
for more info

Functions:
    getResourceChanges: filters resource_changes from plan file
    filterNoOp: filters out no-op actions from resource_changes
    parseResource: parses resource to get some metadata like,
        name, address
    calculateName: tries to calculate resource name
    getAttributes: creates a list of resources with some attributes
    parsePlan: main function
"""
import logging

logger = logging.getLogger(__name__)


def getResourceChanges(data, drift=False):
    """
    Filters Resource Changes from Plan.

    Retrieves the resource_changes or resource_drift portion from terraform plan.

    Args:
        data (dict): dict from json.load('<terraform plan in json format>')
        drift (bool): If true process drift rather than changes

    Returns:
        List of resource_changes or resource_drift
    """

    if drift:
        logger.debug("filter resource_drift from plan")
        if "resource_drift" in data.keys():
            return data["resource_drift"]
        else:
            logger.debug("no resource_drift found")
            return []
    else:
        logger.debug("filter resource_changes from plan")
        if "resource_changes" in data.keys():
            return data["resource_changes"]
        else:
            logger.error("no resource_changes found")
            return []


def filterNoOp(resources):
    """
    Filters no-op actions.

    Parses all the resource_changes and cleans out the ones with no-op actions

    Args:
        data(list): list of resource_changes (output from getResourceChanges)

    Returns:
        List of resources that are going to be changed
    """

    changes = []
    logger.debug("filter no-op actions")
    for res in resources:
        if res["change"]["actions"] != ["no-op"]:
            changes.append(res)

    return changes


def calculateName(resource):
    """
    Tries to calculate the name of the resource.

    Args:
        resource(dict): Resource object

    Returns:
        String name
    """

    name = ""
    beforeName = ""
    afterName = ""
    logger.debug("tries to calculate resource name")
    if resource["change"]["before"] is not None:
        if "name" in resource["change"]["before"]:
            beforeName = resource["change"]["before"]["name"]
            logger.debug("beforeName: %s", beforeName)
    if resource["change"]["after"] is not None:
        if "name" in resource["change"]["after"]:
            afterName = resource["change"]["after"]["name"]
            logger.debug("afterName: %s", afterName)

    if afterName and beforeName and (afterName != beforeName):
        name = beforeName + " --> " + afterName
    elif afterName and beforeName:
        name = beforeName
    elif beforeName and (afterName is not None):
        name = beforeName
    elif afterName and (beforeName is not None):
        name = afterName
    else:
        name = "<known after apply>"

    return name


def parseResource(resource):
    """
    Parse Resource to retrieve metadata.

    Args:
        resource(dict): Resource object

    Returns:
        Dict with resources attributes
    """

    logger.debug("retrieve elements from resource")
    rc = {
        "actions": resource["change"]["actions"],
        "name": calculateName(resource),
        "address": resource["address"],
    }
    return rc


def getAttributes(data):
    """
    Get attributes from resource.

    Args:
        data(list): list of resources

    Returns:
        List of resources dict with attributes
    """

    resources = []
    logger.debug("get attributes from resources")
    for res in data:
        resources.append(parseResource(res))
    return resources


def parsePlan(tfplan, drift):
    """
    Parse Terraform plan in JSON.

    Args:
        tfplan(dict): dict from json.load('<terraform plan in json format>')

    Returns:
        List of resources dict with attributes
    """

    logger.debug("parsing file...")

    all_resources = getResourceChanges(tfplan, drift)
    logger.debug(all_resources)

    resource_changing = filterNoOp(all_resources)
    logger.debug(resource_changing)

    resources = getAttributes(resource_changing)
    logger.debug(resources)

    return resources
