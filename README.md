# COVID19 Helper Bot

[![buddy pipeline](https://app.buddy.works/alessandrojcuppari/twilio-dev-hackathon/pipelines/pipeline/249599/badge.svg?token=a9e1f4c76f608ac31ab34c3b5288bf437ad38ee029c8b60b20406efbe0484335 "buddy pipeline")](https://app.buddy.works/alessandrojcuppari/twilio-dev-hackathon/pipelines/pipeline/249599)
[![DeepSource](https://static.deepsource.io/deepsource-badge-dark-mini.svg)](https://deepsource.io/gh/alessandrojcm/twilio-dev-hackathon/?ref=repository-badge)
[<figure><img src="https://buddy.works" /><figcaption>Automated by Buddy](https://assets.buddy.works/automated-dark.svg)</figcaption></figure>

A Whatsapp Bot to help get information about COVID19, aiming to parcipate
on the [Twilio & Dev 2020 Hackathon](https://dev.to/devteam/announcing-the-twilio-hackathon-on-dev-2lh8).

Pretty much a work in progress.

## Stack

- Python3.8.2
- Poetry
- Fastapi
    - Pydantic
- Fauna DB
- Hosted on Heroku
- Pytest
- Loguru

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
    │   ├── models - Pydatic models
    │   │   └── twilio_actions
    │   ├── scripts - Helper scripts (mainly cli stuff)
    │   ├── services - Utilites for interaction with external apis and logic too heavy for the routes
    │   └── utils - Helper functions
    ├── assistant - Autopilot schema
    ├── design_docs - Some diagrams
    └── tests - Pytest
