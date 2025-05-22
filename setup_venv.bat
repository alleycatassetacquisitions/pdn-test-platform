@echo off
REM Setup script for the Serial Log Testing Platform virtual environment on Windows

REM Check if Python is installed
where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Python is not installed or not in PATH. Please install Python and try again.
    exit /b 1
)

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo Installing requirements...
pip install -r requirements.txt

REM Install the package in development mode
echo Installing package in development mode...
pip install -e .

echo Setup complete. Activate the virtual environment with:
echo   venv\Scripts\activate.bat 