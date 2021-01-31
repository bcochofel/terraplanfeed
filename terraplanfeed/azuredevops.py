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
import terraplanfeed.stdout as stdout

logger = logging.getLogger(__name__)

URLCOMPONENTS = {
    "URL": os.getenv("SYSTEM_TEAMFOUNDATIONSERVERURI"),
    "PROJ": os.getenv("SYSTEM_TEAMPROJECT"),
    "REPOSITORYID": os.getenv("BUILD_REPOSITORY_ID"),
    "PULLREQUESTID": os.getenv("SYSTEM_PULLREQUEST_PULLREQUESTID"),
    "APIVERSION": "6.0",
}

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
    "no-op": ":thumbsup:",
    "create": ":sparkles:",
    "read": ":open_book:",
    "update": ":pencil2:",
    "replace": ":warning:",
    "delete": ":stop_sign:",
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


def validateEnvVars():
    """
    Validates the contents of the required env variables

    Returns:
        boolean true or false if they are present
    """

    logger.debug("check required env variables")
    if URLCOMPONENTS["URL"] is None:
        return False
    if URLCOMPONENTS["PROJ"] is None:
        return False
    if URLCOMPONENTS["REPOSITORYID"] is None:
        return False
    if URLCOMPONENTS["PULLREQUESTID"] is None:
        return False
    if os.getenv("SYSTEM_ACCESSTOKEN") is None:
        return False

    return True


def formatUrl():
    """
    Formats URL using environment variables.

    Returns: url
    """

    url = ""
    logger.debug("format url")
    url = "{url}{proj}/_apis/git/repositories/{repoid}/pullRequests/{prid}/threads?api-version={apiversion}".format(
        url=URLCOMPONENTS["URL"],
        proj=URLCOMPONENTS["PROJ"],
        repoid=URLCOMPONENTS["REPOSITORYID"],
        prid=URLCOMPONENTS["PULLREQUESTID"],
        apiversion=URLCOMPONENTS["APIVERSION"],
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


def sendRequest(url, data):
    """
    Sends request to Azure DevOps API.

    Args:
        url: URL to send request
        data: json content to send to API

    Returns:
        True or False based on the send request
    """

    logger.debug("send request")
    logger.debug("url: {}".format(url))
    logger.debug("data: {}".format(data))

    token = os.getenv("SYSTEM_ACCESSTOKEN")
    access_token = ":{}".format(token)

    encodedBytes = base64.b64encode(access_token.encode("utf-8"))
    encodedStr = str(encodedBytes, "utf-8")

    session = requests.Session()
    session.headers["Authorization"] = "Basic {}".format(encodedStr)
    response = session.post(url, json=data)

    return response.status_code


def main(changes):
    """
    Handles changes and formats content to send to Azure DevOps API.

    Args:
        changes(list): list of resources dict
    """

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
    if validateEnvVars():
        url = formatUrl()
        retcode = sendRequest(url, data)
        logger.debug("status code: {}".format(retcode))
    else:
        stdout.write(content)
