#!/bin/bash


if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate


if [ ! -f "venv/installed" ]; then
    if [ -f "requirements.txt" ]; then
        echo "Installing dependencies..."
        pip3 install -r requirements.txt
        touch venv/installed
    else
        echo "requirements.txt not found, skipping dependency installation."
    fi
else
    echo "Dependencies already installed, skipping installation."
fi

echo "Starting the bot... @sudo_amirh"
python3 main.py

echo "done"
