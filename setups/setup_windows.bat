# setup.bat (Windows)
@echo off

:: Get the directory where the script is located
SET SCRIPT_DIR=%~dp0

:: Create a virtual environment
python -m venv venv

:: Activate the virtual environment
call venv\Scripts\activate.bat

:: Install dependencies from requirements.txt in the script directory
pip install -r "%SCRIPT_DIR%requirements.txt"
