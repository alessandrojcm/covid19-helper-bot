#!/bin/bash

pip install poetry
python -m poetry export -f requirements.txt > requirements.txt
