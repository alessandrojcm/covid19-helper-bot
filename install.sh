#!/bin/bash

pip install poetry
poetry export -r requirements > requirements.txt
pip install -r requirements.txt
