# Future Imports
from __future__ import absolute_import

# Python Standard Library Imports
import json

# Third Party (PyPI) Imports
import requests

# Local Imports
from ..settings import SLACK_WEBHOOK_URL


if SLACK_WEBHOOK_URL is None:
    raise Exception('HTK_SLACK_WEBHOOK_URL or SLACK_WEBHOOK_URL not set in ENV')


def slack_message(
    webhook_url=None,
    channel=None,
    username=None,
    text='',
    attachments=None,
    icon_emoji=None,
    unfurl_links=True,
    unfurl_media=True,
    error_response_handlers=None
):
    """Performs a webhook call to Slack

    https://api.slack.com/incoming-webhooks
    https://api.slack.com/docs/message-formatting

    `channel` override must be a public channel
    """
    payload = {
        'text' : text,
        'unfurl_links' : unfurl_links,
        'unfurl_media' : unfurl_media,
    }

    if channel:
        payload['channel'] = channel
    if username:
        payload['username'] = username
    if icon_emoji:
        payload['icon_emoji'] = icon_emoji
    if attachments:
        payload['attachments'] = attachments

    try:
        response = requests.post(SLACK_WEBHOOK_URL, json=payload)
        if response.status_code == 200:
            # success case, do nothing
            pass
        elif response.status_code <= 399:
            # 200-300, do nothing
            pass
        else:
            print('Slack webhook call error: [{}] {}'.format(response.status_code, response.content))
    except (requests.exceptions.InvalidSchema, requests.exceptions.MissingSchema) as e:
        raise Exception(
            'Bad SLACK_WEBHOOK_URL: [{}] ({})'.format(
                SLACK_WEBHOOK_URL,
                e.__class__.__name__
            )
        )
    except:
        raise

    return response


__all__ = [
    'slack_message',
]
