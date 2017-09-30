import aiohttp
import datetime
import json
import logging
import random

from opsdroid.matchers import match_webhook

GITHUB_API_URL = "https://api.github.com"
HACKTOBERFEST_COMMENTS = [
    "Thanks @{contributor}!\n\nThis PR counts towards [Hacktoberfest](https://hacktoberfest.digitalocean.com/) so make sure you [sign up](https://hacktoberfest.digitalocean.com/sign_up/register).",
    "Nice one @{contributor}!\n\nAll PRs this month counts towards [Hacktoberfest](https://hacktoberfest.digitalocean.com/) so make sure you [sign up](https://hacktoberfest.digitalocean.com/sign_up/register).",
    "Good work @{contributor}!\n\nAll PR will give you [Hacktoberfest](https://hacktoberfest.digitalocean.com/) goodness so make sure you [sign up](https://hacktoberfest.digitalocean.com/sign_up/register)."
]

_LOGGER = logging.getLogger(__name__)


def get_github_connector(opsdroid):
    """Get the github connector"""
    for connector in opsdroid.connectors:
        if connector.name == 'github':
            return connector
    return None


@match_webhook('events')
async def hacktoberfest_event(opsdroid, config, message):
    """On new pull requests respond with a thank you anc hacktoberfest message."""
    request = await message.post()
    payload = json.loads(request["payload"])
    if datetime.datetime.now().month == 10 and "action" in payload \
            and payload["action"] == "opened" and "pull_request" in payload:
        contributor = payload["pull_request"]["user"]["login"]
        issue = "{}/{}#{}".format(payload["repository"]["owner"]["login"],
                                  payload["repository"]["name"],
                                  payload["pull_request"]["number"])
        comment = random.choice(HACKTOBERFEST_COMMENTS).format(contributor=contributor)
        connector = get_github_connector(opsdroid)
        if connector is not None:
            message = Message("",
                              contributor,
                              issue,
                              connector)
            await message.respond(comment)
        else:
            _LOGGER.error("Cannot find GitHub connector")
