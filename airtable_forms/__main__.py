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

from airtable import Airtable
from airtable_forms.common import config, logger
import chevron

OUTPUT_DIR = "docs/"
WEB_ROOT = "http://aleksiknuutila.github.io/airtable_forms/"


def main():
    """Main entry point of airtable_forms"""

    with open("template.md", "r") as f:
        md_template = f.read()

    airtable = Airtable(config["base-key"], "Media sources", api_key=config["api-key"])
    media_sources = [
        {k.replace(" ", "_"): v for k, v in x["fields"].items()}
        for x in airtable.get_all(view="Waiting for coding", maxRecords=10)
    ]
    coders = [{"coder_name": "Alice"}, {"coder_name": "Bob"}, {"coder_name": "Charles"}]

    # Assign coders for every page
    coders_assigned = [
        coders[int(idx / (len(media_sources) / len(coders)))]
        for idx in range(len(media_sources))
    ]

    for coder, source in zip(coders_assigned, media_sources):
        page_content = chevron.render(md_template, {**source, **coder})
        page_fn = "code-{}-{}.md".format(
            coder["coder_name"], "".join(source["Domain"].split(".")[:-1])
        )
        page_path = os.path.join(OUTPUT_DIR, page_fn)

        with open(page_path, "w") as f:
            f.write(page_content)

        print(
            "Form for coding for %s: %s"
            % (coder["coder_name"], WEB_ROOT + page_fn.replace("md", "html"))
        )


if __name__ == "__main__":
    main()
