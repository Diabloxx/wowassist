@echo off
REM Convenience wrapper to run tests via main companion script
call "%~dp0run_companion.bat" test
exit /b %ERRORLEVEL%
