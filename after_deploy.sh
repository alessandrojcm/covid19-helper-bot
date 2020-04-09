#!/bin/bash

pip install poetry
poetry export -f requirements.txt > requirements.txt
pip install -r requirements.txt
npm i -g twilio-cli
twilio plugins:install @dabblelab/plugin-autopilot
twilio autopilot:update -s=./assistant/schema_ready.json --unique-name=TwilioHackathon
