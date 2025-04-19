@echo off
title Commission Tracker Server
call %~dp0\priv\run_with_token.bat python main.py --disable-watchdog