"""
Azure DevOps module for Pull Request comment with changes.

This module expects the following ENV variables:
- SYSTEM_TEAMFOUNDATIONSERVERURI
- SYSTEM_TEAMPROJECT
- BUILD_REPOSITORY_ID
- SYSTEM_PULLREQUEST_PULLREQUESTID
- SYSTEM_ACCESSTOKEN

if any of these variables is empty it will use stdout driver.

Some useful links:
https://docs.microsoft.com/en-us/azure/devops/pipelines/build/variables?view=azure-devops&tabs=yaml#system-variables-devops-services
https://docs.microsoft.com/en-us/rest/api/azure/devops/git/pull%20request%20threads/create?view=azure-devops-rest-6.0
https://docs.microsoft.com/en-us/rest/api/azure/devops/git/pull%20request%20threads/create?view=azure-devops-rest-6.0#commentthreadstatus
https://docs.microsoft.com/en-us/rest/api/azure/devops/git/pull%20request%20threads/create?view=azure-devops-rest-6.0#comment
https://docs.microsoft.com/en-us/rest/api/azure/devops/git/pull%20request%20threads/create?view=azure-devops-rest-6.0#commenttype

Functions:
    getAction: gets the action from actions list
    parseChanges: gets list of changes and creates multiline summary
    validateEnvVars: validates required env variables
    formatUrl: formats URL using environment variables
    formatDataToSend: creates data to be sent in the request
    sendRequest: send the request with the content to devops
    main: entrypoint
"""
import logging
import os
import base64
import requests
from terraplanfeed.stdout import write

logger = logging.getLogger(__name__)

COMMENTTYPE = {
    "CODECHANGE": "codeChange",
    "SYSTEM": "system",
    "TEXT": "text",
    "UNKNOWN": "unknown",
}

COMMENTTHREADSTATUS = {
    "ACTIVE": "active",
    "BYDESIGN": "byDesign",
    "CLOSED": "closed",
    "FIXED": "fixed",
    "PENDING": "pending",
    "UNKNOWN": "unknown",
    "WONTFIX": "wontFix",
}

ACTION_SYMBOLS = {
    "no-op": "👍",
    "create": "✨",
    "read": "📖",
    "update": "📝",
    "replace": "🚧",
    "delete": "🛑",
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


def emptyString(s):
    """
    Validates if string id empty

    Args:
        s(str): String to check

    Returns:
        boolean true or false if string is empty or not
    """

    logger.debug("check if {} is empty".format(s))
    if not (s and s.strip()):
        return True

    return False


def validateEnvVars(azdo):
    """
    Validates the contents of the required env variables

    Args:
        azdo(dict): Azure DevOps parameters

    Returns:
        boolean true or false if they are present
    """

    logger.debug("check required parameters")
    if emptyString(azdo["organization"]):
        return False
    if emptyString(azdo["project"]):
        return False
    if emptyString(azdo["repository"]):
        return False
    if emptyString(azdo["pullrequest"]):
        return False
    if emptyString(azdo["accesstoken"]):
        return False

    return True


def formatUrl(azdo):
    """
    Formats URL using environment variables.

    Args:
        azdo(dict): Azure DevOps parameters

    Returns: url
    """

    url = ""
    logger.debug("format url")
    url = "{url}{proj}/_apis/git/repositories/{repoid}/pullRequests/{prid}/threads?api-version={apiversion}".format(
        url=azdo["organization"],
        proj=azdo["project"],
        repoid=azdo["repository"],
        prid=azdo["pullrequest"],
        apiversion=azdo["apiversion"],
    )

    return url


def formatDataToSend(content, commentType, statusCode):
    """
    Creates JSON content to send to Azure DevOps.

    Args:
        content(str): multiline string
        commentType(str): comment type
        statusCode(str): status code

    Returns:
        dict with the content
    """

    formattedContent = HEADER + content + FOOTER
    data = {
        "comments": [
            {
                "parentCommentId": 0,
                "content": formattedContent,
                "commentType": commentType,
            }
        ],
        "status": statusCode,
    }

    return data


def sendRequest(url, data, azdo):
    """
    Sends request to Azure DevOps API.

    Args:
        url: URL to send request
        data: json content to send to API
        azdo(dict): Azure DevOps parameters

    Returns:
        True or False based on the send request
    """

    logger.debug("send request")
    logger.debug("url: {}".format(url))
    logger.debug("data: {}".format(data))

    token = azdo["accesstoken"]
    access_token = ":{}".format(token)

    encodedBytes = base64.b64encode(access_token.encode("utf-8"))
    encodedStr = str(encodedBytes, "utf-8")

    session = requests.Session()
    session.headers["Authorization"] = "Basic {}".format(encodedStr)
    response = session.post(url, json=data)

    return response.status_code


def generate_pr_comment(changes, azdo):
    """
    Handles changes and formats content to send to Azure DevOps API.

    Args:
        changes(list): list of resources dict
        azdo(dict): Azure DevOps parameters
    """

    ret = False
    logger.debug("azure devops entrypoint")
    if not changes:
        content = "No changes " + ACTION_SYMBOLS["no-op"]
        commentType = COMMENTTYPE["TEXT"]
        statusCode = COMMENTTHREADSTATUS["CLOSED"]
    else:
        content = parseChanges(changes)
        commentType = COMMENTTYPE["CODECHANGE"]
        statusCode = COMMENTTHREADSTATUS["ACTIVE"]
    data = formatDataToSend(content, commentType, statusCode)
    url = formatUrl(azdo)
    print(url)
    if validateEnvVars(azdo):
        url = formatUrl(azdo)
        retcode = sendRequest(url, data, azdo)
        logger.debug("status code: {}".format(retcode))
        if retcode == 200:
            ret = True
    else:
        write(content)
        ret = True

    return ret
