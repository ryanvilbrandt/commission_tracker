@echo off
set venv_root_dir=%~dp0..\..

pushd %venv_root_dir%

call Scripts\activate.bat

setlocal
set /p token=<bat\priv\kofi_verification_token.txt
set KOFI_VERIFICATION_TOKEN=%token%
%*
endlocal

call Scripts\deactivate.bat

popd

exit /b