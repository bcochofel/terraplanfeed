"""
STDOUT output driver module.

https://www.terraform.io/docs/internals/json-format.html#change-representation

Functions:
    getAction: gets the action from actions list
    parseChanges: gets list of changes and creates multiline summary
    writeToStdout: writes the summary content to stdout
"""
import logging

logger = logging.getLogger(__name__)

ACTION_SYMBOLS = {
    "no-op": "None",
    "create": "Create",
    "read": "Read",
    "update": "Update",
    "replace": "Replace",
    "delete": "Delete",
}

HEADER = """
Summary of changes:
===================

"""

FOOTER = """
"""


def getAction(actions):
    """
    Get action

    Args:
        actions(list): list of actions

    Returns:
        action symbol
    """

    logger.debug("get action")
    if "create" in actions and len(actions) > 1:
        return ACTION_SYMBOLS["replace"]
    else:
        return ACTION_SYMBOLS[actions[0]]


def parseChanges(changes):
    """
    Parse changes.

    Args:
        changes(list): list of resources dict

    Returns:
        Multiline string with summary of changes
    """

    content = ""
    logger.debug("parsing changes...")
    for c in changes:
        action = getAction(c["actions"])
        message = "({action}): {name} ({address})".format(
            action=action, name=c["name"], address=c["address"]
        )
        content += message + "\n"
    return content


def writeToStdout(changes):
    """
    Writes summary of changes to stdout.

    Args:
        changes(list): list of resources dict
    """

    logger.debug("write to stdout...")
    content = parseChanges(changes)
    print(HEADER)
    print(content)
    print(FOOTER)
