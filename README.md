# COVID19 Helper Bot

[![buddy pipeline](https://app.buddy.works/alessandrojcuppari/twilio-dev-hackathon/pipelines/pipeline/249599/badge.svg?token=a9e1f4c76f608ac31ab34c3b5288bf437ad38ee029c8b60b20406efbe0484335 "buddy pipeline")](https://app.buddy.works/alessandrojcuppari/twilio-dev-hackathon/pipelines/pipeline/249599)
[![DeepSource](https://static.deepsource.io/deepsource-badge-dark-mini.svg)](https://deepsource.io/gh/alessandrojcm/twilio-dev-hackathon/?ref=repository-badge)
[![buddy pipeline](https://app.buddy.works/alessandrojcuppari/twilio-dev-hackathon/pipelines/pipeline/249599/badge.svg?token=a9e1f4c76f608ac31ab34c3b5288bf437ad38ee029c8b60b20406efbe0484335 "buddy pipeline")](https://app.buddy.works/alessandrojcuppari/twilio-dev-hackathon/pipelines/pipeline/249599)

A Whatsapp Bot to help get information about COVID19, aiming to participate
on the [Twilio & Dev 2020 Hackathon](https://dev.to/devteam/announcing-the-twilio-hackathon-on-dev-2lh8).

Using Twilio Autopilot and Python 3.8

## Stack

- Python3.8.2
- Poetry
- Fastapi
    - Pydantic
- Fauna DB
- Hosted on Heroku
- Pytest
- Loguru
- Requests
- Sentry
- Click

Kickstarted with: https://github.com/Dectinc/cookiecutter-fastapi

## Project structure

Files related to application are in the ``app`` or ``tests`` directories.
Application parts are:

    .
    ├── app
    │   ├── api - Api routes
    │   │   └── routes
    │   │       └── autopilot - Twilio Autopilot Dynamic actions
    │   ├── core - Critical configuration (sessions, logging, etc)
    │   ├── custom_routers - FastAPI custom routes
    │   ├── error_handlers - Custom error handlers
    │   ├── middlewares - FastAPI/Starlette middleware configuration
    │   ├── models - Pydatic models
    │   ├── scripts - Helper scripts (mainly cli stuff)
    │   ├── services - Utilites for interaction with external apis and logic too heavy for the routes
    │   └── utils - Helper functions
    ├── assistant - Autopilot schema
    ├── design_docs - Some diagrams (not to comprehensive)
    └── tests - Pytest


## How to run
First, install dependencies with [Poetry](https://python-poetry.org/): `poetry install`.

### Integrated cli

This app comes with an integrated CLI, activate the env (with `poetry shell`) and run
`python main.py`. The options are:

    Usage: main.py [OPTIONS] COMMAND [ARGS]...

      COVID19 Whatsapp Bot CLI Helper

    Options:
      --help  Show this message and exit.

    Commands:
      create-collections  Creates all collections defined in the models folder
      generate-env        Generates a file .env with the default configuration with the default values
      prepare-schema      Replaces the variables in the assistant schema for the ones on the env
      run                 Runs the development server

### FaunaDB
Then, we need to set FaunaDB; two options:

#### Use provide Docker file

* Spin up the Docker image: `docker-compose up`.
* Run the FaunaDB shell: `docker-compose exec --user root shell /bin/bash`
* Run: `fauna create-database myapp`
* Then, `fauna create-key myapp`
* Copy the key that gets generated

#### Use FaunaDB from the cloud
Easier but not so recommended for development.

* Check out FaunaDB's [getting started](https://docs.fauna.com/fauna/current/start/cloud.html)
* Follow the steps to generate a key for the database you created
* The URL now will be: https://db.fauna.com (hold this)

### Environment variables.

The default environment variables are defined ins `app/models/config` and are as follow:

    API_PREFIX = "/api"
    AUTOPILOT_ENDPOINT_PREFIX = "/autopilot" # API Prefix for autopilot endpoints
    VERSION = "0.1.0"
    DEBUG = False
    TESTING = False
    PROJECT_NAME = "COVID19 Helper Bot"
    LOGGING_LEVEL = LoggingLevels.INFO
    ENVIRONMENT = Environments.DEV # Possible also STAGING and PRODUCTION
    FAUNA_DB_URL = "http://localhost:8443"
    FAUNA_SERVER_KEY = "your_server_key_here"
    TWILIO_ENDPOINT = "http://localhost:5000" # Your API's endpoint that will be called by Twilio
    NOVELCOVID_JHUCSSE_API_URL = "https://corona.lmao.ninja/v2"
    ENDLESS_MEDICAL_API_URL = "https://api.endlessmedical.com/v1/dx"
    OUTCOME_THRESHOLD = 0.45  # Confidence level for recommending seeking medical help
    FAKE_NUMBER = '+15555555' # Fake number to be user in dev
    TWILIO_AUTH_TOKEN # Not needed in dev, can be leaved as this
    SENTRY_DSN # Not needed in dev, can be leaved as this

The order on which the variables take precedence are:

1) The ones defined in the SO environment
2) The ones defined in the `.env` file
3) The defaults on the config schema

For development purposes, just generate the `.env` file with `python main.py generate-env`

You need to replace `FAUNA_SERVER_KEY` with the key obtained when you set up FaunaDB. Also, if you are using
the cloud version, you need to replace the `FAUNA_DB_URL` with the url stated on that step.

### Create schema

Once the envs are set up, run `python main.py create-collection` to generate the FaunaDB Collections an indexes.

### Running

Finally, you can run the server with `python main.py run`.
Docs available under `/docs`.

### Generate the Autopilot Assistant

The Autopilot Assistant Schema for this bot lives in `assistant/schema.json`.

Refer to Twilio [docs](https://www.twilio.com/docs/autopilot/twilio-autopilot-cli) for how to create an assistant
with the CLI.

Once that's done, replace the `TWILIO_ENDPOINT` with your url; run `python main.py prepare-schema` to prepare the
assistant schema with the

Then, open the `after_deploy.sh` script and replace the `--unique-name` flag for your assistant's unique name.
Run the script with `bash` to update your assistant with the schema (needs `yarn` installed).
This script is a bit rough on the edges, since it was written ad-hoc for CI/CD.

### For running in local

In dev mode, the API injects the `FAKE_NUMBER` env into all incoming Autopilot Requests, this way you can test
your API locally from the Twilio Simulator using a SSH tunnel such as ngrok.

### Deployment

This API comes with a Procfile ready to be deployed on Heroku. But, for running, it will require the following
envs to be present:

* `FAUNA_SERVER_KEY`
* `TWILIO_AUTH_TOKEN`
* `SENTRY_DSN`

### Tests

The tests are by no means complete, but you can run them anyways with `pytest`. The caveat is that, being FaunaDB so new,
there is not much info on how to mock it; so the `FAUNA_SERVER_KEY` would need to be present (use Docker for this).

### Information

All information regarding statistics are from the [Novelcovid API](https://corona.lmao.ninja/v2); which in turn
takes its data from the John Hopkins University repository.

The [Endless Medical API](https://www.endlessmedical.com/) was used for the analysis of the user symptoms.
This analysis only serves as guidance and **does not** replace the diagnosis of a doctor.

### Thanks

Huge thanks to the team of Endless Medical for answering my inquiries and being so helpful overall. And thanks
to all the friends and family who copped with my annoying "could you please text the bot?"
