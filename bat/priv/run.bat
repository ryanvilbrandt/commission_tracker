@echo off
set venv_root_dir=%~dp0..\..

pushd %venv_root_dir%

call Scripts\activate.bat

%*

call Scripts\deactivate.bat

popd

exit /b