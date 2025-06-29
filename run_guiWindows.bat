@echo off
REM ----------------------------------------------------------
REM Batch launcher for SQLMap-and-ML-Integration-GUI-Version
REM ----------------------------------------------------------

echo Starting SQLMap-and-ML-Integration-GUI-Version...

REM Change directory to the GUI folder
cd /d "%~dp0GUI"

REM Run the Python script
python SQLiGUI.py

pause
