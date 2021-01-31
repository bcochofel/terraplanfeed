"""
STDOUT output driver module.

https://www.terraform.io/docs/internals/json-format.html#change-representation

Functions:
    getAction: gets the action from actions list
    parseChanges: gets list of changes and creates multiline summary
    write: writes the summary content to stdout
    main: entrypoint
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
**Terraform Plan changes summary:**
===================================
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


def write(content):
    """
    Writes summary of changes to stdout.

    Args:
        content(str): multiline string
    """

    logger.debug("write to stdout")
    print(HEADER)
    print(content)
    print(FOOTER)


def main(changes):
    """
    Entrypoint for stdout output driver.

    Args:
        changes(list): list of resources dict
    """

    logger.debug("stdout entrypoint")
    if not changes:
        content = "No changes"
    else:
        content = parseChanges(changes)
    write(content)
