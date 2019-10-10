# Python SDK for Screendoor [![CircleCI](https://badgen.net/circleci/github/SFDigitalServices/screendoor-sdk-py/master)](https://circleci.com/gh/SFDigitalServices/screendoor-sdk-py) [![Coverage Status](https://coveralls.io/repos/github/SFDigitalServices/screendoor-sdk-py/badge.svg?branch=master)](https://coveralls.io/github/SFDigitalServices/screendoor-sdk-py?branch=master)

Python SDK for interacting with Screendor API

http://dobtco.github.io/screendoor-api-docs/

## Install
> $ pip install -e "git://github.com/SFDigitalServices/screendoor-sdk-py#egg=screendoor-sdk"

## Example Usage
> from screendoor_sdk.screendoor import Screendoor

> scrndr = Screendoor(`API_KEY`)

> responses = scrndr.get_project_responses(`PROJECT_ID`, {'per_page': 1, 'page' : 1}, 1)

> response = scrndr.update_project_response(`PROJECT_ID`, `RESPONSE_ID`, {"1": "Test Name"})

> labels = scrndr.get_project_labels(`PROJECT_ID`)
