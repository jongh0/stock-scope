@echo off
cd /d "%~dp0"

echo [StockScope] Updating stock data...
echo.

where py >nul 2>&1
if %errorlevel% == 0 (
    set PY=py
) else (
    set PY=python
)

%PY% -c "import yfinance" >nul 2>&1
if %errorlevel% neq 0 (
    echo [StockScope] Installing required packages...
    %PY% -m pip install yfinance pandas numpy requests --quiet
    echo.
)

%PY% scripts/update_data.py

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Update failed. Install required packages:
    echo   pip install yfinance pandas numpy requests
) else (
    echo.
    echo [DONE] Refresh your browser.
)

pause
