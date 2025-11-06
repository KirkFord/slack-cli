import json
import re
import sys

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from . import errors
from . import token
from . import messaging

__all__ = ["client", "init"]


BaseError = SlackApiError


class SlackClient:
    INSTANCE = None

    def __init__(self, user_token):
        self._web_client = WebClient(token=user_token)

    @classmethod
    def create_instance(cls, user_token):
        cls.INSTANCE = cls(user_token)

    @classmethod
    def instance(cls):
        if cls.INSTANCE is None:
            # This is not supposed to happen
            raise ValueError("Slack client token was not defined")
        return cls.INSTANCE

    # Provide access to the WebClient for direct API calls
    def __getattr__(self, name):
        return getattr(self._web_client, name)


def init(user_token=None, team=None):
    """
    This function must be called prior to any use of the Slack API.
    """
    user_token = user_token
    loaded_token = token.load(team=team)
    must_save_token = False
    if user_token:
        if user_token != loaded_token:
            must_save_token = True
    else:
        user_token = loaded_token
        if not user_token:
            user_token = token.ask(team=team)
            must_save_token = True

    # Initialize slack_sdk client globally
    SlackClient.INSTANCE = SlackClient(user_token)
    if must_save_token:
        save_token(user_token, team=team)


def save_token(user_token, team=None):
    # Always test token before saving
    try:
        client().api_test()
    except SlackApiError:
        raise errors.SlackCliError("Invalid Slack token: '{}'".format(user_token))

    # Get team
    try:
        response = client().team_info()
        team = team or response["team"]["domain"]
    except SlackApiError as e:
        message = str(e)
        if e.response.get("error") == "missing_scope":
            message = (
                "Missing scope on token {}. This token requires the 'team:read' scope."
            ).format(user_token)
        raise errors.SlackCliError(message)

    # Save token
    try:
        token.save(user_token, team)
    except errors.ConfigSaveError as e:
        sys.stderr.write("❌ ")
        sys.stderr.write(e.args[0])
        sys.stderr.write("\n")
        sys.stderr.write(
            "⚠️ Could not save token to disk. You will have to configure the Slack"
            " token again next time you run slack-cli.\n"
        )


def client():
    return SlackClient.instance()


def update_status_fields(**profile):
    client().users_profile_set(profile=profile)
