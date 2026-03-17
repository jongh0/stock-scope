# StockScope - Project Overview & Instructions

StockScope is a serverless static dashboard for monitoring stocks and ETFs, providing real-time-ish data and historical visualizations (sparklines) without a traditional backend.

## Project Architecture

The project follows a "Static Site + Scheduled Data Fetching" model:
1.  **Data Layer**: A Python script (`scripts/update_data.py`) fetches stock data from Yahoo Finance and Naver Finance and saves it as a single JSON file (`data/stocks.json`).
2.  **Frontend Layer**: A vanilla HTML/CSS/JS dashboard fetches the JSON file and renders an interactive table.
3.  **Automation**: GitHub Actions runs the update script hourly to keep the data fresh.

### Key Technologies
- **Frontend**: Vanilla JavaScript, CSS (Custom Variables), HTML5.
- **Data Processing**: Python 3, `yfinance`, `pandas`, `numpy`.
- **Hosting**: GitHub Pages.

---

## Getting Started

### Prerequisites
- Python 3.x
- Browser (Modern)

### Installation
Install the required Python packages for data fetching:
```bash
pip install yfinance pandas numpy requests
```

### Running Locally
You can start a local development server using the provided batch file or Python's built-in server:
```bash
# Using batch file (Windows)
start.bat

# Manual command
python -m http.server 8080
```
Then open `http://localhost:8080` in your browser.

### Updating Data
To manually refresh the stock data:
```bash
# Using batch file (Windows)
update.bat

# Manual command
python scripts/update_data.py
```

---

## Development Conventions

### Project Structure
- `js/config.js`: Contains UI configuration, including groups and ticker mappings.
- `js/app.js`: Main application logic (fetching data, rendering table, event handling).
- `js/sparkline.js`: Logic for generating SVG sparklines.
- `css/style.css`: All styling, including theme-specific variables.
- `data/stocks.json`: The generated data source (Do not edit manually).
- `scripts/update_data.py`: The data fetching and indicator calculation engine.

### Adding a New Ticker
To add a new stock or ETF to the dashboard, you must update two files:
1.  **`scripts/update_data.py`**: Add the ticker to the `STOCKS` dictionary. This ensures the data is fetched.
2.  **`js/config.js`**: Add the ticker to the appropriate group in the `GROUPS` array. This ensures it is displayed in the UI.

### Technical Indicators
The following indicators are calculated in `scripts/update_data.py`:
- **RSI (14)**: Relative Strength Index.
- **MACD**: Moving Average Convergence Divergence (12, 26, 9).
- **MDD**: Maximum Drawdown (52-week).
- **Sharpe Ratio**: Annualized risk-adjusted return.
- **Beta**: Volatility relative to the S&P 500.

---

## Instruction for Gemini CLI

When working on this project, please adhere to the following:
- **No Bundlers**: Do not introduce npm, webpack, or any build tools. Keep the project as a collection of static files.
- **Pure JavaScript**: Avoid frameworks like React or Vue. Use vanilla DOM manipulation.
- **Surgical Updates**: When adding features, ensure they align with the existing `StockScope` class structure in `app.js`.
- **Data Integrity**: Ensure any changes to the data format in `update_data.py` are mirrored in the frontend rendering logic in `app.js`.
- **Performance**: Keep the `stocks.json` file size in mind. Historical data is downsampled (e.g., 3-year data is weekly) to maintain fast load times.
