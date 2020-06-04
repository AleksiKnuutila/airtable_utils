"""airtable_forms.

Usage:
airtable_forms
airtable_forms -h | --help
airtable_forms --version

Options:

 -h --help    Show this screen.
 --version    Show the version.
"""

import os
import sys

import chevron
from airtable import Airtable
from airtable_forms.common import config


def main():
    """Main entry point of airtable_forms"""

    OUTPUT_DIR="docs/"

    with open("template.md", "r") as f:
        md_template = f.read()

    airtable = Airtable(config["base-key"], "Media sources", api_key=config["api-key"])
    media_sources = [
        x["fields"] for x in airtable.get_all(view="Waiting for coding", maxRecords=10)
    ]
    coders = [{"coder_name": "Alice"}, {"coder_name": "Bob"}]

    # Assign coders for every page
    coders_assigned = [
        coders[int(idx / (len(media_sources) / len(coders)))]
        for idx in range(len(media_sources))
    ]

    for coder, source in zip(coders_assigned, media_sources):
        page_content = chevron.render(md_template, {**source, **coder})


        pass


if __name__ == "__main__":
    main()
