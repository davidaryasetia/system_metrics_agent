@echo off

python --version 2>NUL
if errorlevel 1 goto errorNoPython

python -m venv venv 
CALL "%cd%\venv\Scripts\activate.bat"

@REM
pip install -r "%cd%\Document\requirements.txt"

Pause
goto:eof

:errorNoPython
echo.
echo Error^ : Python 3.8.10 is not installed
Pause