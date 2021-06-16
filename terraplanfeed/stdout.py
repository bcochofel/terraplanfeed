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
    "no-op": "👍",
    "create": "✨",
    "read": "📖",
    "update": "📝",
    "replace": "🚧",
    "delete": "🛑",
}

ACTION_TEXT = {
    "no-op": ".",
    "create": "+",
    "read": "r",
    "update": "U",
    "replace": "R",
    "delete": "X",
}

HEADER = """
**Terraform Plan changes summary:**
===================================
"""

FOOTER = """
"""


def getAction(actions, textonly):
    """
    Get action

    Args:
        actions(list): list of actions
        textonly(bool): disable emoji

    Returns:
        action symbol
    """

    logger.debug("get action")
    lookup = ACTION_TEXT if textonly else ACTION_SYMBOLS
    if "create" in actions and len(actions) > 1:
        return lookup["replace"]
    else:
        return lookup[actions[0]]


def parseChanges(changes, textonly):
    """
    Parse changes.

    Args:
        changes(list): list of resources dict
        textonly(bool): disable emoji

    Returns:
        Multiline string with summary of changes
    """

    content = ""
    logger.debug("parsing changes...")
    for c in changes:
        action = getAction(c["actions"], textonly)
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


def generate_stdout(changes, textonly = False):
    """
    Entrypoint for stdout output driver.

    Args:
        changes(list): list of resources dict
        textonly(bool): disable emoji
   """

    logger.debug("stdout entrypoint")
    if not changes:
        content = "No changes"
    else:
        content = parseChanges(changes, textonly)
    write(content)
