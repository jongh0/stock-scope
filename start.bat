@echo off
cd /d "%~dp0"

echo [StockScope] Starting local server...
echo   http://localhost:8080
echo.
echo Press Ctrl+C to stop.
echo.

start "" /b cmd /c "timeout /t 1 >nul && start http://localhost:8080"

where py >nul 2>&1
if %errorlevel% == 0 (
    py -m http.server 8080
) else (
    python -m http.server 8080
)

echo.
echo Server stopped.
pause
