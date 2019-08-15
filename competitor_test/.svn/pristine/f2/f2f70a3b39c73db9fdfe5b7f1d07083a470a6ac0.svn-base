@echo off
setlocal enabledelayedexpansion

set PYTHON_FILE=%~dp0number_detector.py
set "CMD="

:SHIFT_START
if "%2" == "" GOTO SHIFT_END
set CMD=%CMD% %1
shift
GOTO SHIFT_START
:SHIFT_END

for %%F in ("%1") do ( set CMD=!CMD! %%F )

echo %CMD%

python %PYTHON_FILE% %CMD%