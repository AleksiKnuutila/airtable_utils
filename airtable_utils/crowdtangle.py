import requests
import json
import os

from airtable_utils.common import config


def total_engagement(posts):
    """Count number of engagement over all posts

    Arguments:
        posts {array of Crowdtangle objects}
    """
    count = 0
    for post in posts:
        statistics = post["statistics"]["actual"]
        for key in statistics.keys():
            count += statistics[key]
    return count


def posts_search(**arguments):
    """Get posts from /posts/search endpoint
    """

    if not "startDate" in arguments and not "timeframe" in arguments:
        arguments["timeframe"] = "1 MONTH"
    if not "count" in arguments:
        arguments["count"] = "100"
    arguments["token"] = config["crowdtangle-api-token"]
    resp = requests.get("https://api.crowdtangle.com/posts/search", params=arguments)
    return json.loads(resp.text)["result"]["posts"]
