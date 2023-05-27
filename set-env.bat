@REM Creates assets directory
mkdir assets

@REM Creates a virtual environment for the project
python -m venv btrenv

@REM Actibvate the virtual env
activate.bat

@REM Install the required packages
pip install -r requirements.txt