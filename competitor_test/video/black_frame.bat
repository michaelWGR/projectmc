@echo off
setlocal enabledelayedexpansion

set PYTHON_FILE=%~dp0black_frame.py
set "CMD="

:SHIFT_START
if "%2" == "" GOTO SHIFT_END
set CMD=%CMD% %1
shift
GOTO SHIFT_START
:SHIFT_END

for %%F in ("%1") do ( set CMD=!CMD! %%F )

echo python %PYTHON_FILE% %CMD%
python %PYTHON_FILE% %CMD%