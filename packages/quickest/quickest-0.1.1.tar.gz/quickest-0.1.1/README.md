
# Install


Set up the workspace:


    . .env
    chmod +x scripts/*

## Option 1. Install from source


Install ``poetry``, ``pyenv``, ``pylint``, ``sphinx`` and ``pytest``.

Build and install the library into the local ``pyenv`` environment:


    make install


## Option 2. Install from PyPI


This is not guaranteed to be the same version as the source in this repository. Check [PyPI](https://pypi.org/project/quickest/) for the latest release date.

    pip install quickest


# Test 

    pytest


# Use

## Train a threshold

    ./scripts/train.sh

## View the last experiment

    ./scripts/simulate.sh

## Profile one training step

    ./scripts/profile.sh


Pass a `-h` flag to a bash script to see more instructions.

# Documentation

Generate documentation:

    make doc