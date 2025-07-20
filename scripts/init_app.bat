@echo off
echo Setting up the Pyn application...

echo Creating virtual environment and installing dependencies...
call scripts\setup_windows.bat

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Initializing the database...
flask init-db

echo Running the application...
python run.py

echo Setup complete. The application should now be running.
pause