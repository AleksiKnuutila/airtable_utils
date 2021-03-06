"""airtable_bot.

Usage:
airtable_bot [--api-key KEY] [--base-key BASE] [--crowdtangle-api-token TOKEN]
airtable_bot -h | --help
airtable_bot --version

Options:

 -h --help                  Show this screen.
 --version                  Show the version.
 --api-key api-key          Airtable API key
 --base-key base-key        Airtable base key
 --crowdtangle-api-token    Crowdtangle token
"""

import sys
import os
from collections import ChainMap

from airtable import Airtable
from airtable_utils.s3 import upload_file
from airtable_utils.crowdtangle import posts_search, total_engagement
from airtable_utils.common import config, logger

from tqdm import tqdm


# not used at the moment
def screenshot_webpage(url):
    """Make screenshot of page

    Arguments:
        url {string} -- URL of webpage
    """
    chrome_binary = '"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"'
    chrome_options = "--headless --disable-gpu --screenshot"
    fn = f"{url}.png"

    # this is pretty insecure
    os.system(f"{chrome_binary} {chrome_options} https://{url}")
    os.system(f"mv screenshot.png {fn}")


def empty_record(record):
    """Check if record is empty"""
    return not "Base URL" in record["fields"]


def crowdtangle_engagement(record, *, airtable):
    """ Engagement statistics based on URL from Crowdtangle """

    crowdtangle_posts = posts_search(searchTerm=record["fields"]["Base URL"])

    return {
        # "Count of public posts": str(len(crowdtangle_posts)),
        "Engagement in past month": str(total_engagement(crowdtangle_posts))
    }


def deduplicate(records, *, airtable):
    """ Remove duplicate rows """
    seen = set()
    duplicates = []
    for record in records:
        if record["fields"]["Base URL"] in seen:
            duplicates.append(True)
        else:
            seen.add(record["fields"]["Base URL"])
            duplicates.append(False)
    duplicate_ids = [x["id"] for x, y in zip(records, duplicates) if y]

    if duplicate_ids:
        logger.debug("Removing %s duplicate(s)" % len(duplicate_ids))
        airtable.batch_delete(duplicate_ids)


def add_background_information(records, *, data_sources, airtable):
    """ Helper function to collect and add background information on sources

    Args:
        records: List of records to append
        data_sources: List of functions that return dicts with information
        airtable: API object
    """

    for record in tqdm(records):

        fields = [
            data_source(record, airtable=airtable) for data_source in data_sources
        ]
        # Merge list of dicts
        fields = {k: v for d in fields for k, v in d.items()}
        fields["Status"] = "Waiting for initial coding"
        tqdm.write("Updating %s" % record["fields"]["Base URL"])
        airtable.update(record["id"], fields)


def update_coding_status(records, *, airtable):
    """ Update status for records that require more coding """
    record_ids = [x["id"] for x in records if len(x["fields"]["Coding decision"]) > 0]
    if record_ids:
        logger.debug("Updating coding status of %s records" % len(record_ids))
    for id in tqdm(record_ids):
        airtable.update(id, {"Status": "Further coding required"})


def main():
    """Main entry point of airtable_bot"""

    airtable = Airtable(config["base-key"], "Sources", api_key=config["api-key"])
    new_records = airtable.get_all(view="New records", maxRecords=2000)

    logger.info("Deleting empty records")
    empty_records = [x["id"] for x in new_records if empty_record(x)]
    if empty_records:
        logger.info("Deleted %s empty records" % len(empty_records))
        airtable.batch_delete(empty_records)
        new_records = [x for x in new_records if not empty_record(x)]

    logger.info("Deduplicating")
    deduplicate(new_records, airtable=airtable)

    logger.info("Adding background information")
    new_records = airtable.get_all(view="New records", maxRecords=2000)
    # List of functions that return background information
    data_sources = [crowdtangle_engagement]
    add_background_information(
        new_records, data_sources=data_sources, airtable=airtable
    )

    all_records = airtable.get_all(view="All records", maxRecords=2000)
    logger.info("Updating coding status")
    update_coding_status(all_records, airtable=airtable)


if __name__ == "__main__":
    main()
