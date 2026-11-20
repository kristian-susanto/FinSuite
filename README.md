# FinSuite — Stock Research Dashboard

A pair of lightweight Flask web applications that bundle stock-research utilities into a single dark/light-themed dashboard. The two scripts (`stockanalysis.py` and `tradingview.py`) share the same UI shell and tooling; they differ in which financial data provider the **Multi-Tab Researcher** opens against (StockAnalysis vs. TradingView).

Everything runs locally at `http://127.0.0.1:5000` — no external build step, no template directory, no static files.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Running the App](#running-the-app)
- [Using the Dashboard](#using-the-dashboard)
  - [Stock Multi-Tab Researcher](#stock-multi-tab-researcher)
  - [Click Counter](#click-counter)
  - [Text Case Converter](#text-case-converter)
  - [Ticker Symbol Extractor](#ticker-symbol-extractor)
  - [Financial Shorthand Converter](#financial-shorthand-converter)
- [Historical Data Page](#historical-data-page)
- [HTTP Routes](#http-routes)
- [How It Works](#how-it-works)
- [StockAnalysis vs. TradingView Builds](#stockanalysis-vs-tradingview-builds)
- [Troubleshooting](#troubleshooting)
- [Disclaimer](#disclaimer)

---

## Overview

FinSuite is a self-hosted research companion for retail investors and spreadsheet-driven analysts. Given an **exchange** and a **ticker**, it opens a coordinated set of browser tabs for fundamental and price research, and it provides small quality-of-life tools (ticker extraction, case conversion, a click counter, and — in the TradingView build — a K/M/B/T financial-shorthand converter).

| File               | Data source for the researcher                 | Extra tool                    |
| ------------------ | ---------------------------------------------- | ----------------------------- |
| `stockanalysis.py` | [StockAnalysis.com](https://stockanalysis.com) | —                             |
| `tradingview.py`   | [TradingView.com](https://www.tradingview.com) | Financial Shorthand Converter |

Both files:

- Use Flask + embedded HTML (via `render_template_string`).
- Serve a **History** page backed by a Python proxy to Yahoo Finance.
- Share the counter, case converter, ticker extractor, and theme system.
- Suppress Werkzeug request logging with a custom `QuietRequestHandler`.

---

## Features

- **Multi-tab stock researcher** — open up to 8 research tabs (Overview, Historical Data, Income Statement, Balance Sheet, Cash Flow, Ratios, Revenue, Dividends) with one click.
- **Preset packages** — _Quarterly Package_ / _Semester Package_ open a fixed bundle of 4 tabs.
- **Exchange directory** — 100+ exchanges with names, countries, and codes; autocomplete via `<datalist>`.
- **Yahoo Finance historical data** — server-side proxy fetches 10 years of daily closes and pivots them into quarter-end / half-year tables.
- **Interactive History page** — sortable periods, Close Price vs. Highest Close rows, one-click copy as tab-separated values (paste straight into Excel/Sheets).
- **Ticker Symbol Extractor** — paste raw table data → clean, deduplicated, A→Z sorted ticker list.
- **Text Case Converter** — UPPERCASE, lowercase, Capitalize Word, Sentence case, with clipboard copy.
- **Click Counter** — for tallying rows while reviewing data.
- **Dark / light theme** — persisted in `localStorage` across pages.
- **Pop-up fallback** — a manual link list is rendered if the browser blocks automatic tab opening.
- **Refresh guard** — `Ctrl/Cmd+R` and `F5` are intercepted to preserve counter/workspace state.

---

## Requirements

- **Python 3.9+**
- Python packages:

  ```bash
  pip install flask requests
  ```

- A modern browser with JavaScript enabled.
- Internet access (StockAnalysis / TradingView pages and Yahoo Finance data are loaded remotely).
- Pop-up permission for `127.0.0.1:5000` if you want automatic tab opening.

---

## Installation

1. Clone or download the repository.
2. (Optional) create and activate a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Linux / macOS
   .venv\Scripts\activate         # Windows
   ```

3. Install dependencies:

   ```bash
   pip install flask requests
   ```

4. Place `stockanalysis.py` and/or `tradingview.py` in the same folder.

---

## Running the App

Start either script:

```bash
# StockAnalysis build
python stockanalysis.py

# TradingView build
python tradingview.py
```

Expected console output:

```
 * Running on http://127.0.0.1:5000
```

Then open <http://127.0.0.1:5000> in your browser.

> **Note:** Both scripts bind to `0.0.0.0:5000`. Do not run them simultaneously on the same machine unless you change the port in one of them.

---

## Using the Dashboard

### Stock Multi-Tab Researcher

1. **Exchange Name** — type a country or exchange; autocomplete suggestions come from the built-in `exchanges` list (e.g. `Hong Kong Stock Exchange — Hong Kong`).
2. **Ticker Symbol** — e.g. `0700`, `AAPL`, `7203`.
3. **Select Data Points** — pick the tabs to open (checkbox grid). Use **All** / **None** for quick toggles.
4. **Data Source Support** — choose a mode:
   - **Quarterly Package** — opens 4 fixed tabs (Historical Data, Income Statement, Balance Sheet, Ratios).
   - **Semester Package** — same as above, but the History page defaults to **semiannual** granularity.
   - **StockAnalysis** _(stockanalysis.py)_ / **TradingView** _(tradingview.py)_ — opens whichever data points you checked, against the respective provider.
5. Click **Open All Selected Tabs**.

**Behaviour notes**

- Tabs open 350 ms apart to avoid pop-up blocking.
- A **Manual Generated Links** panel appears below the button with the same links, so you can open them individually if automatic opening fails.
- In package mode the first tab (Historical Data) opens **in-app** via `/history/<symbol>`; the other three go to the remote provider.

**Ticker normalization**

- `HKEX` tickers of 1–3 digits are left-padded to 4 digits for StockAnalysis URLs (e.g. `700` → `0700`).
- For Yahoo Finance, Hong Kong tickers have leading zeros stripped and `.HK` appended (e.g. `0700` → `700.HK`). The `/history/<symbol>` route re-pads to 4 digits for the display title.

**Package period**

- Package mode always requests `?p=quarterly` from StockAnalysis; the semester choice only affects the in-app History view's default granularity.

### Click Counter

A simple tally with **+**, **−**, and **Reset** (reset prompts via SweetAlert2). Handy for counting rows while cross-referencing data.

### Text Case Converter

Paste any text and transform with **UPPERCASE**, **lowercase**, **Capitalize Word**, or **Sentence case**. **Copy to Clipboard** copies the current value; **Clear** empties it.

### Ticker Symbol Extractor

Designed for pasting raw rows copied from a screener or spreadsheet. Two input shapes are recognised:

- **Tab-separated rows** — the ticker must be in the **first column**; a later column must contain numeric data, and the second column must contain a company name (has lowercase letters) or a `D` marker.
- **Line-by-line** — a ticker on its own line, followed (after blank lines) by a company-name line or a `D` marker.

Detected tickers must match `^([A-Z][A-Z0-9]{0,5}|\d{1,6})$` and are filtered against a noise list (`TTM`, `EPS`, `ETF`, `ADR`, …).

Options:

- **Remove duplicates** — dedupe results.
- **Sort Z → A** — reverse the default A → Z ordering.
- **Tab-separated (single row)** — output as a single tab-joined row instead of one per line.

Buttons: **Copy result**, **Load sample** (a large HK Engineering & Construction dataset), **Clear**. A live status line reports the ticker count.

### Financial Shorthand Converter

_(TradingView build — `tradingview.py`)_

A K/M/B/T multiplier helper that expands or contracts values like `1.5B` → `1,500,000,000` (and vice versa). The legend chips document the multipliers:

| Suffix | Multiplier         |
| ------ | ------------------ |
| K      | ×1,000             |
| M      | ×1,000,000         |
| B      | ×1,000,000,000     |
| T      | ×1,000,000,000,000 |

---

## Historical Data Page

Reached at `/history/<symbol>` (e.g. `/history/700.HK`), the page:

1. Requests 10 years of daily closes via the in-app `/proxy` route → Yahoo Finance.
2. Buckets every trading day into either:
   - **Quarterly buckets** — `1Q` (Jan–Mar), `1H` (Apr–Jun), `9M` (Jul–Sep), `FY` (Oct–Dec)
   - **Semiannual buckets** — `1H` (Jan–Jun), `FY` (Jul–Dec)
3. Renders a table with three rows:
   - **Actual Date** — the period-end date
   - **Close Price** — the closing price on the period-end day
   - **Highest Close** — the highest daily close within the period (hover a cell to see the exact date)
4. Includes a **Current** column with the most recent trading day's close.

### Copying price data

At the bottom of the page:

- **Latest Period** — pick the starting period (newest first).
- **Periods to Copy (n)** — number of periods to include (defaults to 20 quarterly / 10 semiannual, capped at the available count).
- **Value** — copy either **Highest Close** or **Close Price**.
- Press **Enter** anywhere on the page (outside buttons/inputs/links) or click **Copy Price Data**.

The clipboard payload is **tab-separated values only** (no labels):

```
<current close>\t<period 1>\t<period 2>\t…
```

Paste straight into a single spreadsheet row.

A **Quarterly / Semiannual** toggle in the header re-renders the table and pushes the new `freq` value into the URL (via `history.pushState`), so the view is shareable/bookmarkable.

---

## HTTP Routes

Both apps expose the same three routes:

| Method | Path                                 | Purpose                                                           |
| ------ | ------------------------------------ | ----------------------------------------------------------------- |
| `GET`  | `/`                                  | Main dashboard (inlined HTML, no templates required).             |
| `GET`  | `/history/<symbol>`                  | Historical-data table for a Yahoo Finance symbol.                 |
| `GET`  | `/proxy?symbol=…&range=…&interval=…` | Server-side proxy to `query1.finance.yahoo.com/v8/finance/chart`. |

### `/proxy`

Proxies a single Yahoo Finance chart request to avoid browser CORS restrictions. Query parameters:

- `symbol` (default `0700.HK`)
- `range` (default `10y`)
- `interval` (default `1d`)

Returns the raw JSON with the upstream status code, or `{"error": "..."}` with HTTP 500 on failure. A desktop Chrome `User-Agent` is set so Yahoo responds with data rather than a block page.

---

## How It Works

- **Single-file apps** — HTML/CSS/JS is embedded as Python raw strings (`HTML_PAGE`, `HISTORY_PAGE`) and injected via `render_template_string`. No template directory or static files required.
- **Exchange mapping** — two lookup tables drive URL generation:
  - `YAHOO_SUFFIX_MAP` — maps exchange code → Yahoo Finance suffix (e.g. `HKEX → .HK`, `TSE → .T`).
  - `SA_EXCHANGE_MAP` — maps exchange code → StockAnalysis.com path segment (e.g. `HKEX → hkg`).
- **URL builders** — `saBaseUrl()` assembles either a `/stocks/<ticker>` (US exchanges) or `/quote/<exchange>/<ticker>` URL. `buildSAPackageTargets()` and `buildStockAnalysisTargets()` return arrays of `{ id, name, url }` objects that the UI renders as both auto-opened tabs and fallback links.
- **Period bucketing** — `buildPeriodMeta(date, frequency)` returns `{ key, endMonth, label }`; `processPeriodData()` iterates the Yahoo timestamp/close arrays once, tracking the period-end close and the highest intra-period close.
- **State persistence** — theme is stored in `localStorage` under the key `theme`.
- **Refresh protection** — `Ctrl/Cmd+R` and `F5` are intercepted and suppressed (with a toast) to keep the counter and workspace state stable.
- **Silent logs** — `QuietRequestHandler` subclasses `WSGIRequestHandler` and no-ops `log_request`, `log_info`, and `log`.

---

## StockAnalysis vs. TradingView Builds

The two scripts are largely identical. Differences:

| Aspect                                                  | `stockanalysis.py`  | `tradingview.py`                        |
| ------------------------------------------------------- | ------------------- | --------------------------------------- |
| Third radio option                                      | `StockAnalysis`     | `TradingView`                           |
| Remote provider                                         | `stockanalysis.com` | `tradingview.com`                       |
| Exchange → provider mapping                             | `SA_EXCHANGE_MAP`   | TradingView equivalents                 |
| Extra tool                                              | —                   | Financial Shorthand Converter (K/M/B/T) |
| History page, ticker extractor, counter, case converter | Identical           | Identical                               |

If you maintain both, the shared code (theme, counter, extractor, History page, `/proxy`) can be extracted into a single module to reduce duplication.

---

## Troubleshooting

| Symptom                                  | Likely cause / fix                                                                                                                           |
| ---------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| Tabs don't open                          | Browser pop-up blocker. Allow pop-ups for `127.0.0.1:5000`, or use the **Manual Generated Links** panel.                                     |
| History page shows "No data found"       | Wrong ticker or unsupported exchange suffix. Check the `YAHOO_SUFFIX_MAP` entry for your exchange.                                           |
| History page shows "Server returned 500" | Yahoo Finance rate-limited or blocked the proxy. Wait and retry.                                                                             |
| `Copy Price Data` fails silently         | Non-secure context (HTTP on a non-localhost host). The Clipboard API requires HTTPS or `localhost`; the fallback uses `execCommand('copy')`. |
| Extractor shows "no tickers detected"    | The pasted format doesn't match either the tab-separated or line-by-line rules. Ensure tickers are in the first column or on their own line. |
| `Port 5000 already in use`               | Another process (often macOS AirPlay Receiver) is holding the port. Change `port=5000` in the script.                                        |
| Refresh shortcuts blocked                | Intentional — a toast explains it. Re-open the URL if you need a fresh state.                                                                |

---

## Disclaimer

FinSuite is a personal research and productivity tool. It proxies third-party data (Yahoo Finance) and generates deep links to StockAnalysis.com and TradingView.com. It is **not affiliated** with any of those providers. Respect their terms of service, rate limits, and robots policies. Nothing in this app constitutes financial advice; verify all data independently before acting on it.
