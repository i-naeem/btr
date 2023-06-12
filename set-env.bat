@echo off

@REM Creates assets directory
mkdir assets

@REM Creates logs directory
mkdir logs

@REM Creates a virtual environment for the project
python -m venv env

@REM Actibvate the virtual env
activate.bat

@REM Install the required packages
pip install -r requirements.txt