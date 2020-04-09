#!/bin/bash

# Setting python version
pyenv install -v 3.8.2
pyenv global 3.8.2
pip install poetry

# Generating requirements
python -m poetry export -f requirements.txt > requirements.txt
