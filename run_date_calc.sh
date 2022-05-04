#!/bin/bash

# Create venv if it does not exist
if ! [[ -d "$(pwd)/venv" ]]; then
    echo "Setting Up virtualenvironment"
    python3 -m venv venv
fi

echo "Run the program"
$(pwd)/venv/bin/python3 main.py
