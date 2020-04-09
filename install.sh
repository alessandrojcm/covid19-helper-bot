#!/bin/bash

pip install poetry
poetry export -f requirements.txt > requirements.txt
pip install -r requirements.txt
