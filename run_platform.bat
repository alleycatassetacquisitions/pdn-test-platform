@echo off
REM Run the Serial Log Testing Platform in Windows

REM Activate virtual environment if it exists
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
) else (
    echo Warning: Virtual environment not found. Running with system Python.
)

REM Run the platform with arguments passed to this script
python -m src.main %*

REM Pause if run directly (not from command line)
if not defined PROMPT (
    pause
) 