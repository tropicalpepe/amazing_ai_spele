@echo off
echo Starting Amazing AI Spele...

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not added to your PATH.
    echo Please install Python 3.10+ from https://www.python.org/downloads/
    pause
    exit /b 1
)

:: Create virtual environment if it doesn't exist
if not exist ".venv" (
    echo Creating a portable virtual environment...
    python -m venv .venv
)

:: Activate the virtual environment
call .venv\Scripts\activate.bat

:: Install dependencies silently
echo Installing and verifying dependencies...
python -m pip install --upgrade pip -q
pip install -r requirements.txt -q

:: Run the Streamlit application
echo Launching the game UI...
set PYTHONPATH=%cd%
streamlit run src\ui\app.py

:: If execution ends unexpectedly, pause so the user can see any errors
pause
