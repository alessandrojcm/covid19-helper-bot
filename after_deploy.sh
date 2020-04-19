#!/bin/bash

# Installing requirements for cli
pip install poetry
python -m poetry export -f requirements.txt > requirements.txt
pip install --user -r requirements.txt

# Installing twilio cli
npm i -g twilio-cli

# Generating schema
python main.py prepare-schema

# Updating assistant
twilio plugins:install @dabblelab/plugin-autopilot
twilio autopilot:update -s=assistant/schema_ready.json --unique-name=COVID19-Bot
twilio autopilot:modelbuilds:create --assistant-sid=UA37ceb2c26d38cb3a43768074e324c6df
