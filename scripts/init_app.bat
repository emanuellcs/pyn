@echo off
echo Setting up the Pyn application...

REM Change directory to the project root (parent directory of scripts)
cd ..

REM Create virtual environment if it doesn't exist
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt

echo Setting FLASK_APP environment variable...
set FLASK_APP=run.py

echo Initializing the database...
flask init-db

echo Running the application...
python run.py

echo Setup complete. The application should now be running.
pause
