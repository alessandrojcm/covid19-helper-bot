#!/bin/bash

# Installing requirements for cli
pynv install -v 3.8.2
pip install poetry
python -m poetry export -f requirements.txt > requirements.txt
pip install --user -r requirements.txt

# Installing twilio cli
nvm install 13.12.0
nvm use 13.12.0
npm i -g twilio-cli

# Generating schema
python -m poetry run main.py prepare-schema

# Updating assistant
twilio plugins:install @dabblelab/plugin-autopilot
twilio autopilot:update -s=./assistant/schema_ready.json --unique-name=COVID19-Bot
