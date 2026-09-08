@echo off
title Vernacular AI - Next-Gen Vernacular Education Platform
echo ======================================================================
echo    VERNACULAR AI - NEXT-GEN MULTI-LINGUAL EDUCATION PLATFORM
echo     (51 Languages, Live Video Studio, Multi-Broadcast & SQLite DB)
echo ======================================================================
echo.

cd /d "%~dp0backend"

if not exist "venv\Scripts\python.exe" (
    echo [1/3] Setting up Python virtual environment...
    python -m venv venv
    echo [2/3] Installing dependencies...
    venv\Scripts\pip.exe install -r requirements.txt
) else (
    echo [*] Virtual environment ready.
)

echo.
echo [*] Opening Vernacular AI in your default browser...
start http://127.0.0.1:5000

echo [*] Starting Flask Server on http://127.0.0.1:5000...
echo Press CTRL+C to stop the server.
echo.
venv\Scripts\python.exe app.py
pause
