#!/bin/bash

# Installing requirements for cli
pip install poetry
python -m poetry export -f requirements.txt > requirements.txt
pip install --user -r requirements.txt

# Installing twilio cli
npm i -g twilio-cli

# Generating schema
python -m poetry run main.py prepare-schema

# Updating assistant
twilio plugins:install @dabblelab/plugin-autopilot
twilio autopilot:update -s=./assistant/schema_ready.json --unique-name=COVID19-Bot
