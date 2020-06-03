"""airtable_forms.

Usage:
airtable_forms -h | --help
airtable_forms --version

Options:

 -h --help    Show this screen.
 --version    Show the version.
"""

import sys
from airtable_forms.from_docopt import from_docopt
from airtable_forms import __version__


def main(inputargs=None):
    """Main entry point of airtable_forms"""
    if inputargs is None:
        inputargs = sys.argv[1:] if len(sys.argv) > 1 else ""
    args = from_docopt(argv=inputargs, docstring=__doc__, version=__version__)

if __name__ == "__main__":
    main()
