@echo off
title Installing Commission Tracker
echo [1m[7m[94mSetting up the virtual environment...[0m
python -m venv %~dp0
echo [1m[7m[94mUpdating pip...[0m
echo.
call %~dp0\bat\priv\run.bat python -m pip install --upgrade pip
echo.
echo [1m[7m[94mInstalling requirements...[0m
echo.
call %~dp0\bat\priv\run.bat pip install -r requirements.txt
echo.
echo [1m[7m[92mDone![0m
pause