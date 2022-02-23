# PACKAGES
import requests
import os
import json
import discord
from discord import Webhook, RequestsWebhookAdapter
import datetime

# ENVIRONEMENT SECRETS
import os
os.environ["DISCORD_WEBHOOK"] = "your webhook"
os.environ["bearer_token"] = "your bearer"

bearer_token = os.environ['bearer_token']

# FUNCTIONS
def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2FilteredStreamPython"
    return r


def get_rules():
    print(bearer_oauth)
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream/rules", auth=bearer_oauth
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot get rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    print(json.dumps(response.json()))
    return response.json()


def delete_all_rules(rules):
    if rules is None or "data" not in rules:
        return None

    ids = list(map(lambda rule: rule["id"], rules["data"]))
    payload = {"delete": {"ids": ids}}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        auth=bearer_oauth,
        json=payload
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot delete rules (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    print(json.dumps(response.json()))


def set_rules(delete):
    # You can adjust the rules if needed to follow accounts
    accounts = "(from:elonmusk OR from:mcuban)"
    sample_rules = [
      {"value": accounts},
      # {"value": "is:retweet "+accounts},
      # {"value": "is:quote "+accounts}        
    ]
    payload = {"add": sample_rules}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        auth=bearer_oauth,
        json=payload,
    )
    if response.status_code != 201:
        raise Exception(
            "Cannot add rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    print(json.dumps(response.json()))

def get_stream(set):
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream?tweet.fields=entities,author_id", auth=bearer_oauth, stream=True,
    )
    print(response.status_code) #if you get from the api succesfully it will return 200 in the console
    if response.status_code != 200:
        raise Exception(
            "Cannot get stream (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    for response_line in response.iter_lines():
        if response_line:
            json_response = json.loads(response_line) #this gives you the Tweet data

            ######
            # add your own custom filtering here and logic for each time there is a new Tweet from a specified account
            ######


# STATE VARIABLES
webhook_url = os.environ['DISCORD_WEBHOOK']
discord.webhook = Webhook.from_url(webhook_url, adapter=RequestsWebhookAdapter()) #webhook

# running code
rules = get_rules()
delete = delete_all_rules(rules)
set = set_rules(delete)
get_stream(set)


