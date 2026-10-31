@echo off
setlocal enabledelayedexpansion
title InfraWatch - AI Predictive Monitoring Dashboard

cd /d "%~dp0"

echo ========================================================================
echo                  INFRAWATCH - DIGITAL TWIN DASHBOARD
echo    AI-Powered Predictive Infrastructure Monitoring ^& Failure Intelligence
echo ========================================================================
echo.

:: Detect Python environment
set "PYTHON_EXE="

if exist "%~dp0venv\Scripts\python.exe" (
    set "PYTHON_EXE=%~dp0venv\Scripts\python.exe"
    echo [OK] Using virtual environment: venv
) else if exist "%~dp0.venv\Scripts\python.exe" (
    set "PYTHON_EXE=%~dp0.venv\Scripts\python.exe"
    echo [OK] Using virtual environment: .venv
) else (
    where python >nul 2>nul
    if %ERRORLEVEL% equ 0 (
        set "PYTHON_EXE=python"
        echo [OK] Using system Python
    ) else (
        echo [ERROR] Python was not found on your system!
        echo Please install Python 3.10+ or configure the virtual environment.
        echo.
        pause
        exit /b 1
    )
)

echo [OK] Starting InfraWatch Streamlit Web Application...
echo [OK] The application will open automatically in your default browser.
echo.
echo URL: http://localhost:8501
echo (Press Ctrl+C in this terminal window to stop the server)
echo ========================================================================
echo.

:: Start browser in parallel after 2 seconds as backup to ensure web page opens
start /b cmd /c "timeout /t 2 /nobreak >nul 2>&1 && start http://localhost:8501"

:: Launch Streamlit app
"%PYTHON_EXE%" -m streamlit run frontend\app.py --server.port 8501 --server.headless false

if %ERRORLEVEL% neq 0 (
    echo.
    echo [WARNING] Streamlit server exited with code %ERRORLEVEL%.
    pause
)
