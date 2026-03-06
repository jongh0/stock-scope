@echo off
cd /d "%~dp0"

echo [StockScope] Updating stock data...
echo.

where py >nul 2>&1
if %errorlevel% == 0 (
    py scripts/update_data.py
) else (
    python scripts/update_data.py
)

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Update failed. Install required packages:
    echo   pip install yfinance pandas numpy requests
) else (
    echo.
    echo [DONE] Refresh your browser.
)

pause
