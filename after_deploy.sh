#!/bin/bash

python main.py prepare-schema
npm i -g twilio-cli
twilio plugins:install @dabblelab/plugin-autopilot
twilio autopilot:update -s=./assistant/schema_ready.json --unique-name=TwilioHackathon
