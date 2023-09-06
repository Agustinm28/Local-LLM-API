#!/bin/bash

### Script to setup the project. Execute with sudo.

## Check if the script is being run as root
if [ "$EUID" -ne 0 ]
  then echo "This script must be run with sudo."
  exit 1
fi

## Install update
echo "Updating..."
sudo apt update

## Setting up enviroment
echo "Setting up enviroment..."
# Install pip
# Check if pip is installed
if ! [ -x "$(command -v pip3)" ]; then
    echo "Installing pip..."
    sudo apt install python3-pip
fi
# Install venv
# Check if venv is installed
if ! [ -x "$(command -v python3.10-venv)" ]; then
    echo "Installing venv..."
    sudo apt install python3.10-venv
fi
# Create venv
# Check if venv is created
if ! [ -d ".venv" ]; then
    echo "Creating venv..."
    python3 -m venv .venv
fi
# Activate venv
echo "Activating venv..."
source .venv/bin/activate

## Install packages
echo "Installing packages..."

# Install gcc
# Check if gcc is installed
if ! [ -x "$(command -v gcc)" ]; then
    echo "Installing gcc..."
    sudo apt-get install gcc
    export CC=gcc
fi

# Install g++
# Check if g++ is installed
if ! [ -x "$(command -v g++)" ]; then
    echo "Installing g++..."
    sudo apt-get install g++
    export CXX=g++
fi

# Install make
# Check if make is installed
if ! [ -x "$(command -v make)" ]; then
    echo "Installing make..."
    sudo apt-get install make
fi

## Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

## Create models folder
# Check if models folder exists
if ! [ -d "models" ]; then
    echo "Creating models folder..."
    mkdir models
fi