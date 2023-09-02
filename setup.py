import subprocess
import sys
import os

def setup():
    '''
    Script to setup the project. Execute with sudo.
    '''

    #Check if sudo
    if not os.geteuid() == 0:
        sys.exit('This script must be run with sudo.')

    # Initial update
    print('Updating...')
    subprocess.run(['sudo', 'apt', 'update'])

    print('Setting up enviroment...')
    # Install venv
    subprocess.run(['sudo', 'apt', 'install', 'python3.10-venv'])
    # Create venv
    subprocess.run(['python3', '-m', 'venv', '.venv'])
    # Activate venv
    subprocess.run(['source', '.venv/bin/activate'])

    print('Installing requirements...')
    # Install packages
    subprocess.run(['sudo', 'apt-get', 'install', 'gcc'])
    subprocess.run(['export', 'CC=gcc'])
    subprocess.run(['sudo', 'apt-get', 'install', 'g++'])
    subprocess.run(['export', 'CXX=g++'])
    subprocess.run(['sudo', 'apt-get', 'install', 'make'])
    
    print('Installing dependencies...')
    # Install requirements
    subprocess.run(['pip', 'install', '-r', 'requirements.txt'])

    # Create models folder
    if not os.path.isdir('./models'):
        os.mkdir('./models')