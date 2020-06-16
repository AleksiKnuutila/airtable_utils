# Introduction
airtable_utils contains code to help with Airtable.
# Use

airtable_bot.py and airtable_forms.py can be run as Python scripts.

```
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
```

api-key, base-key and crowdtangle-api-token need to be defined in either secret.yaml or as commandline arguments.

# Installation

To get the code:
```
git clone https://github.com/AleksiKnuutila/airtable_utils
```

# Setting up

```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```