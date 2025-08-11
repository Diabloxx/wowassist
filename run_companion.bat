@echo off
REM WoW Companion setup + run script (Assist Mode default)
setlocal ENABLEDELAYEDEXPANSION

REM Navigate into project subfolder
cd /d "%~dp0wow-companion" || (echo Failed to cd into wow-companion & exit /b 1)

echo [INFO] Working dir: %CD%

REM ---------------------------
REM 1. Create / activate virtual environment
REM ---------------------------
if not exist .venv (
  echo [INFO] Creating virtual environment (.venv)...
  where py >nul 2>&1 && (py -3.11 -m venv .venv || py -3.12 -m venv .venv || py -3 -m venv .venv) || (
    where python >nul 2>&1 && (python -m venv .venv) || (echo [ERROR] Python not found. Install Python 3.11+ and retry. & exit /b 1)
  )
)

call .venv\Scripts\activate.bat || (echo [ERROR] Failed to activate venv & exit /b 1)
echo [INFO] Python: %PYTHONHOME% (%VIRTUAL_ENV%)

REM ---------------------------
REM 2. Dependencies
REM ---------------------------
if not exist requirements.txt (
  echo [WARN] requirements.txt missing. Skipping dependency install.
) else (
  echo [INFO] Upgrading pip...
  python -m pip install --upgrade pip >nul 2>&1
  echo [INFO] Installing / syncing dependencies (may take a minute)...
  python -m pip install -r requirements.txt || (echo [ERROR] Dependency install failed & exit /b 1)
)

REM Optional: verify tesseract on PATH (warn only)
where tesseract >nul 2>&1 || echo [WARN] Tesseract not detected on PATH. OCR features may be degraded.

REM ---------------------------
REM 3. Mode Dispatch
REM    Usage:
REM      run_companion.bat            -> run app
REM      run_companion.bat perf       -> run app with perf timings
REM      run_companion.bat test       -> run tests
REM      run_companion.bat bench 30   -> benchmark loop for 30s
REM ---------------------------

set ARG=%1
if /I "%ARG%"=="test" goto run_tests
if /I "%ARG%"=="perf" goto run_perf
if /I "%ARG%"=="bench" goto run_bench
goto run_app

:run_tests
echo [INFO] Running test suite...
python -m pytest -q || (echo [ERROR] Tests failed & exit /b 1)
echo [INFO] Tests complete.
goto end

:run_perf
echo [INFO] Starting app with perf timings...
python -m src.app --perf
goto end

:run_bench
set SECONDS=%2
if "%SECONDS%"=="" set SECONDS=20
echo [INFO] Benchmarking main loop for %SECONDS%s...
python scripts/benchmark_loop.py --seconds %SECONDS%
goto end

:run_app
echo [INFO] Launching WoW Companion (Assist Mode)...
python -m src.app
goto end

:end
echo [INFO] Done.
endlocal
exit /b 0
