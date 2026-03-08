# AGENTS.md

This file provides guidance to Codex (Codex.ai/code) when working with code in this repository.

## Commands

**Run the dashboard locally:**
```bat
start.bat                   # Starts Python HTTP server at http://localhost:8080
python -m http.server 8080  # Equivalent direct command
```

**Update stock data:**
```bat
update.bat                  # Downloads latest data for all tickers
```

**Run update script directly:**
```bash
pip install yfinance pandas numpy requests

python scripts/update_data.py   # Downloads 3-year history for all ~86 tickers via yfinance
```

## Architecture

Serverless static dashboard. The browser loads `index.html`, fetches `data/stocks.json` (a single file containing all tickers), and renders an HTML table with SVG sparklines. No external API calls are made from the browser.

### Data Flow
```
Yahoo Finance (yfinance, 3-year daily OHLCV)
  → scripts/update_data.py
    → data/stocks.json   (single file, all tickers)
      → Browser fetches via fetch('data/stocks.json')
```

### JS Module Loading Order (index.html script tags)
1. `js/config.js` — `GROUPS`, `ALL_TICKERS`, `TICKER_NAMES`, `TICKER_CURRENCY`
2. `js/sparkline.js` — `createSparkline()`, `getChartColors()`
3. `js/app.js` — `StockScope` class (entry point, creates `window.app`)

All modules are plain globals — no bundler, no ES modules.

### stocks.json Structure
```json
{
  "updated": "2026-03-08T09:00:00",
  "stocks": {
    "AAPL": {
      "name": "애플",
      "currency": "USD",
      "price": 227.52,
      "change_pct": -0.85,
      "week_pct": 1.23,
      "mdd_52w": -18.4,
      "rsi": 48.3,
      "macd_hist": 0.123,
      "macd_up": true,
      "hist_30d": [...],    // 30 daily close prices
      "hist_1y":  [...],    // 252 daily close prices
      "hist_3y":  [...]     // ~156 weekly close prices (downsampled)
    },
    ...
  }
}
```

### Adding a Ticker or Group
- **New ticker**: Add to `STOCKS` dict in `scripts/update_data.py` and to the appropriate group in `js/config.js → GROUPS`
- **New group**: Add an object `{ id, name, stocks: [{name, ticker}] }` to `GROUPS` in `js/config.js`
- Ticker must exist in both places; `update_data.py` is the source of truth for what gets fetched

### Technical Indicators (computed in update_data.py)
- **RSI(14)**: Standard Wilder RSI using rolling mean of gains/losses
- **MACD**: EMA(12) − EMA(26), signal=EMA(9); `macd_hist` = MACD − signal; `macd_up` = histogram increasing
- **MDD**: `(price − 52w_high) / 52w_high × 100` (uses last 252 trading days)
- **week_pct**: 5 trading days ago close → current price change

### Sparkline Rendering (sparkline.js)
- Pure SVG, inline as HTML string — no canvas, no ECharts
- `hist_3y` is weekly-resampled (`resample('W').last()`) to reduce data size
- Colors (`upColor`/`downColor`) are passed as hex from `getChartColors()` at render time because SVG fill colors can't use CSS variables once inlined

### Thresholds for Column Coloring (app.js)
| Metric | Class | Condition |
|--------|-------|-----------|
| MDD | `mdd-mild` | −10% < MDD ≤ −5% |
| MDD | `mdd-moderate` | −20% < MDD ≤ −10% |
| MDD | `mdd-severe` | −30% < MDD ≤ −20% |
| MDD | `mdd-critical` | MDD ≤ −30% |
| RSI | `rsi-high` | RSI ≥ 70 (과매수) |
| RSI | `rsi-low` | RSI ≤ 30 (과매도) |
| MACD | `macd-bull-strong` | hist > 0 && increasing |
| MACD | `macd-bull-weak` | hist > 0 && decreasing |
| MACD | `macd-bear-weak` | hist < 0 && increasing |
| MACD | `macd-bear-strong` | hist < 0 && decreasing |

### Theme
- Dark/light toggle stored in `localStorage('ss-theme')`, applied as `data-theme` on `<html>`
- On theme toggle, `_render()` is called to re-inject sparkline SVGs with correct hex colors
