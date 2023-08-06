# Boon Amber Python SDK

An SDK for Boon Amber sensor analytics

## Installation

The Boon Amber SDK is a Python 3 project and can be installed via pip. After cloning the `amber-python-sdk` repository to the current directory, run:

```
pip install amber-python-sdk
```

## Credentials setup

Note: An account in the Boon Amber cloud must be obtained from Boon Logic to use the Amber SDK.

The account credentials should be placed in a file named _~/.Amber.license_:

```
{
    "default": {
        "username": "AMBER-ACCOUNT-USERNAME",
        "password": "AMBER-ACCOUNT-PASSWORD"
    }
}
```

The _~/.Amber.license_ file will be consulted by the Amber SDK to successfully find and authenticate with your Amber account credentials. Credentials may optionally be provided instead via the environment variables `AMBER_USERNAME` and `AMBER_PASSWORD`.

## Connectivity test

The following Python script provides a basic proof-of-connectivity:

**connect-example.py**

```
from boonamber import AmberClient

# At initialization the client discovers Amber account credentials
# under the "default" entry in the ~/.Amber.license file.
amber = AmberClient()

# These credentials are used to authenticate against the Amber cloud.
amber.authenticate()

# The client is then authenticated for one hour of use, and may
# re-authenticate at any time with another call to authenticate().
sensors = amber.list_sensors()
print("sensors: {}".format(sensors))
```

Running the connect-example.py script should yield output like the following:
```
$ python connect-example.py
sensors: {}
```
where the dictionary `{}` lists all sensors that currently exist under the given Boon Amber account.
