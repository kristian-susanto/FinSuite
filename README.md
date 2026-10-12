# FinSuite — Unified Tool Suite Documentation

---

## Table of Contents

- [Overview](#overview)
- [Core Key Features](#core-key-features)
  - [1. Stock Multi-Tab Researcher](#1-stock-multi-tab-researcher)
  - [2. Click Counter](#2-click-counter)
  - [3. Text Case Converter](#3-text-case-converter)
  - [4. Financial Shorthand Converter](#4-financial-shorthand-converter)
  - [5. Ticker Symbol Extractor](#5-ticker-symbol-extractor)
- [Stock Researcher — Data Source Modes](#stock-researcher--data-source-modes)
- [Local Historical Data Tab](#local-historical-data-tab)
- [Global Core Layout Specifications](#global-core-layout-specifications)
- [Prerequisites & Environment Setup](#prerequisites--environment-setup)
- [How to Use the Suite](#how-to-use-the-suite)
- [Keyboard Shortcuts](#keyboard-shortcuts)
- [Financial Shorthand Converter Reference](#financial-shorthand-converter-reference)
- [Ticker Symbol Extractor Reference](#ticker-symbol-extractor-reference)
- [Customization](#customization)
- [Browser Support](#browser-support)
- [Troubleshooting](#troubleshooting)
- [Unified Architecture & Technologies Used](#unified-architecture--technologies-used)
- [License](#license)

---

## Overview

**FinSuite** is a single-file Flask web application that bundles five complementary tools into one browser-based workspace:

1. **Stock Multi-Tab Researcher** — Launch multiple research tabs for a selected exchange, ticker, and data provider, including a locally rendered historical data view.
2. **Click Counter** — Track high-frequency click interactions with temporary tally state and safe reset controls.
3. **Text Case Converter** — Transform text between uppercase, lowercase, title case, and sentence case.
4. **Financial Shorthand Converter** — Convert `K`, `M`, `B`, and `T` financial shorthand values into full integers for spreadsheet workflows.
5. **Ticker Symbol Extractor** — Extract, deduplicate, and alphabetically sort ticker symbols from raw screener output for clean spreadsheet pasting.

Together, these tools eliminate context switching by combining productivity utilities, capital market analytics, and financial data normalization in one interface.

---

## Core Key Features

### 1. 📊 Stock Multi-Tab Researcher

Designed for investors, traders, and financial analysts to eliminate repetitive browser research by triggering deep-dive analysis pipelines simultaneously with a single action.

- **Multi-Tab Execution Workflow:** Generates and launches custom analytical URLs instantly, mapping exchange codes and asset symbols dynamically.
- **Cross-Global Exchange Resolution System:** Out-of-the-box support for international markets including NYSE, HKG, SGX, SSE, TYO, and more.
- **Granular Data Point Filtering:** Choose precisely which dimensions to investigate (e.g., Latest News, Financial Ratios, Historical Trends, Balance Sheets, Income Statements, Cash Flow Metrics, or Dividend Trackers). This checklist applies to **TradingView** and **StockAnalysis** modes.
- **Four Data Source Modes:** Switch the structural parsing logic between **Quarterly Package**, **Semester Package**, **TradingView**, or **StockAnalysis** depending on your data pipeline preferences.
- **Package Modes (Quarterly & Semester):** One-click bundled workflows that ignore the granular checklist and launch a fixed set of **6 analytical tabs** in a single action — combining StockAnalysis, TradingView, and a locally rendered historical data view.
  - **Quarterly Package (default):** TradingView financial statement URLs use the `FQ` period parameter, and the local Historical Data popup opens in **Quarterly** mode.
  - **Semester Package:** TradingView financial statement URLs use the `FH` period parameter, and the local Historical Data popup opens in **Semiannual** mode directly. You can still toggle back to Quarterly inside the popup.
- **Local Historical Data View:** The ⏳ **Historical Data** tab is rendered on the fly by the Flask backend. It queries Yahoo Finance daily closes (10 years), reduces them to period-end closes, and displays them in a **transposed, responsive table** with a **Current** column always shown first (leftmost), followed by period columns. The tab includes an **in-popup Quarterly / Semiannual toggle** so the user can switch reporting frequency without returning to the main page.
- **In-Popup Frequency Toggle:** The Historical Data popup carries its own **Quarterly** and **Semiannual** toggle in the blue header. Clicking either button re-renders the table instantly using the already-cached daily data — no additional network request is issued.
- **Context-Aware Keyboard Shortcut:** Pressing `Enter` inside the Exchange Name field, Ticker Symbol field, or any non-textarea/non-button form control immediately triggers the research pipeline.
- **Fail-Safe Manual Backup Registry:** Embedded link presentation tier ensures that if a modern browser blocks multi-popups, backup clickable links render seamlessly to bypass security restrictions.

### 2. 🖱️ Click Counter

A lightweight, reactive digital tallying and micro-interaction sandbox designed for high-frequency tracking.

- **Micro-Interaction Visual System:** Live viewport numbers dynamically expand and contract using hardware-accelerated CSS scaling matrices upon click inputs.
- **Refresh Shortcut Interception:** Intercepts volatile browser events (such as accidental keyboard `F5`, `Ctrl+R`, `Ctrl+Shift+R`, `Ctrl+F5`, and `Shift+F5` refreshes) to help protect the temporary click count from unintended page reloads. The handler uses the capture phase and `stopPropagation` for maximum coverage.
- **Safe Reset Dialogs:** Employs explicit user-intent confirmations before wiping state tracking records back to zero.
- **Decrement Control:** Includes a dedicated `−` button to reduce the current count by one when the value is greater than zero.

### 3. 🔤 Text Case Converter

A professional-grade typographical formatting workstation tailored for developers, copywriters, and structured data cleaners.

- **Four-State Transformation Matrix:**
  - `UPPERCASE`: Standardizes code variables, tickers, or headings into all capital letters.
  - `lowercase`: Converts strings to lowercase formats for normalized database ingestions.
  - `Capitalize Word`: Formats strings into title-case blocks by auto-capitalizing every segmented word.
  - `Sentence case`: Corrects running prose by adjusting only the initial character of the text sequence.
- **One-Click Buffer Interface:** Directly interacts with the system clipboard APIs for frictionless, one-tap copy operations.
- **Clear Action Feedback:** Displays a toast confirmation after clearing text from the workspace.

### 4. 💰 Financial Shorthand Converter

A lightweight, responsive module that converts shorthand financial values with **K**, **M**, **B**, and **T** suffixes into full numbers. It automatically skips percentage lines, outputs tab-separated values for easy pasting into Sheets (horizontally), and includes an optional reverse-order feature to match right-to-left spreadsheet layouts.

- **Suffix conversion** — Converts `K` (×1,000), `M` (×1,000,000), `B` (×1,000,000,000), and `T` (×1,000,000,000,000) to full integers.
- **Percentage skipping** — Lines containing a `%` sign are ignored automatically.
- **Horizontal paste** — Output values are separated by tabs (`\t`), so they paste across a row in Sheets.
- **Reverse order** — Optional checkbox (enabled by default) to reverse the output order, ideal for spreadsheets that list newest data on the left.
- **Exact math** — Uses BigInt arithmetic to avoid floating-point errors with very large numbers.
- **Invisible character handling** — Strips zero-width and bidirectional control characters that often come with copied data.
- **Responsive design** — Works on desktop, tablet, and mobile.
- **One-click copy** — Copies the entire output to the clipboard.
- **No dependencies** — Implemented in vanilla JavaScript with no external runtime libraries.

### 5. 📋 Ticker Symbol Extractor

A precision parsing module that ingests raw screener output and returns a clean, deduplicated, alphabetically sorted list of ticker symbols — ready to paste as a spreadsheet column or a single tab-separated row.

- **Dual-format ticker detection** — Recognises both **alphabetic symbols** (e.g., `NVDA`, `AMZN`, `DIS`) and **numeric symbols** (e.g., `2475`, `6951`, `679`) so it works with US markets, ASEAN exchanges, and Hong Kong stock codes alike.
- **Context-aware confirmation** — A line is only accepted as a ticker if the following non-empty line looks like a company name (contains lowercase characters) or is the standalone market marker `D`. This prevents header rows, numeric cells, and unrelated short lines from polluting the output.
- **Header noise filtering** — Common financial header abbreviations (`TTM`, `EPS`, `YOY`, `QOQ`, `ETF`, `IPO`, `CEO`, `CFO`, `ROE`, `ROA`, `ROI`, `NAV`, `ALL`, `NONE`, `NA`) are automatically discarded.
- **Alphabetical sorting (A → Z)** — The default output order; a single checkbox flips it to **Z → A** for reverse workflows.
- **Duplicate removal** — On by default; toggle it off to preserve every occurrence in the source.
- **Flexible output shape** — Choose **one symbol per line** (ready for a column) or **tab-separated single row** (ready for a row) with a single checkbox.
- **Live statistics badge** — Displays how many tickers were extracted and which sort direction is active (e.g., `22 tickers · A → Z`).
- **One-click copy** — The **Copy result** button pushes the entire output to your clipboard.
- **Built-in sample loader** — The **Load sample** button populates the input with a real-world Hong Kong electronic technology screener export.
- **No dependencies** — Pure vanilla JavaScript, zero external libraries.

---

## Stock Researcher — Data Source Modes

The Stock Multi-Tab Researcher supports four data-source modes, selectable through the **Data Source Support** radio panel.

| Mode                  | Default | Checklist Used? | Tabs Opened | Description                                                                                                                                                                                 |
| --------------------- | :-----: | :-------------: | :---------: | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Quarterly Package** |    ✓    |       No        |      6      | Fixed multi-source bundle (StockAnalysis + TradingView + Local Historical Data) with TradingView financial statement period `FQ`. Local Historical Data popup opens in **Quarterly** mode.  |
| **Semester Package**  |    —    |       No        |      6      | Fixed multi-source bundle (StockAnalysis + TradingView + Local Historical Data) with TradingView financial statement period `FH`. Local Historical Data popup opens in **Semiannual** mode. |
| **TradingView**       |    —    |       Yes       |    1 – 9    | Granular control; only the checklist-selected data points are opened. Tickers are normalized to uppercase, exchange codes are remapped.                                                     |
| **StockAnalysis**     |    —    |       Yes       |    1 – 9    | Granular control; only the checklist-selected data points are opened. Generated URLs use lowercase exchange/ticker values.                                                                  |

### Package Modes — Fixed 6-Tab Bundle

When **Quarterly Package** or **Semester Package** is selected, the data-point checklist is dimmed and disabled, and clicking **Open All Selected Tabs** immediately launches the following six analytical views:

| #   | Data Point          | Provider                      | Purpose                                                         | Period Parameter                                                  |
| --- | ------------------- | ----------------------------- | --------------------------------------------------------------- | ----------------------------------------------------------------- |
| 1   | 🏢 Overview         | StockAnalysis                 | Company profile, sector, business summary                       | —                                                                 |
| 2   | 🏢 Overview         | TradingView                   | Company profile, sector, business summary                       | —                                                                 |
| 3   | ⏳ Historical Data  | Local (Flask + Yahoo Finance) | Current close + Quarterly / Semiannual closes over the last 10y | Quarterly for Quarterly Package / Semiannual for Semester Package |
| 4   | 📑 Income Statement | TradingView                   | Income statement                                                | `FQ` (Quarterly) / `FH` (Semester)                                |
| 5   | ⚖️ Balance Sheet    | TradingView                   | Balance sheet                                                   | `FQ` (Quarterly) / `FH` (Semester)                                |
| 6   | 📊 Ratios           | TradingView                   | Statistics and valuation ratios                                 | `FQ` (Quarterly) / `FH` (Semester)                                |

Package modes are intentionally unconfigurable on the main page — they are fixed reconnaissance bundles designed so that switching between providers is not necessary when you simply want comprehensive coverage of a ticker. The locally rendered **Historical Data** tab is unique to Package modes and is opened via a client-side fetch to the Flask `/proxy` endpoint.

---

## Local Historical Data Tab

When the ⏳ **Historical Data** target is executed (only available inside Package modes), the application opens a fresh browser tab and performs the following:

1. Resolves the ticker to a Yahoo Finance symbol using the exchange suffix map (e.g., `HKEX → .HK`).
2. Calls the Flask `/proxy?symbol=…&range=10y&interval=1d` endpoint, which forwards the request to Yahoo Finance with a desktop User-Agent header.
3. Caches the returned daily closes in memory — the data is fetched **once per popup**.
4. Reduces the daily data to **period-end closing prices** based on the currently selected frequency:
   - **Quarterly** — one data point per calendar quarter (Mar / Jun / Sep / Dec).
   - **Semiannual** — one data point per half-year, keeping only **June** and **December** closes.
5. Renders a **transposed, responsive table** with a **Current** column always shown first (leftmost), followed by the most recent period column to the right:

   | **Period**      | **Current** | 9M2026     | 1H2026     | 1Q2026     | FY2025     | 9M2025     | 1H2025     | 1Q2025     |
   | --------------- | ----------- | ---------- | ---------- | ---------- | ---------- | ---------- | ---------- | ---------- |
   | **Actual Date** | 2026-09-22  | 2026-09-18 | 2026-06-30 | 2026-03-31 | 2025-12-30 | 2025-09-30 | 2025-06-30 | 2025-03-27 |
   | **Close Price** | 6,200.00    | 6,300.00   | 5,550.00   | 6,450.00   | 8,075.00   | 7,625.00   | 8,675.00   | 8,500.00   |
   - **Current column:** Shows the most recent trading day's actual date and close.
   - **Period row (header):** Compact labels derived from the period-end month:
     - March → `1Q<year>` (e.g., `1Q2026`)
     - June → `1H<year>` (e.g., `1H2026`)
     - September → `9M<year>` (e.g., `9M2026`)
     - December → `FY<year>` (e.g., `FY2025`)
   - **Actual Date row:** Actual trading date of the period-end close.
   - **Close Price row:** Period-end closing price in the listing currency.
   - The leftmost label column is **sticky** so it stays visible while scrolling horizontally.
   - The table uses a 💼 favicon and adapts to `prefers-color-scheme` (light/dark).

### In-Popup Frequency Toggle

The Historical Data popup carries its own frequency selector in the blue header, positioned below the title:

```text
┌──────────────────────────────────────────────────────────┐
│  0700.HK — Historical Data                               │
│  Quarter-End Closing Prices · Last 10 Years · …          │
│  ┌───────────┬─────────────┐                             │
│  │ Quarterly │ Semiannual  │  ← click to switch          │
│  └───────────┴─────────────┘                             │
└──────────────────────────────────────────────────────────┘
```

- The active frequency is preselected based on the chosen Package mode.
- Clicking the other button immediately re-renders the table using cached data.
- The switch is **instant and offline** — no additional request to Flask or Yahoo Finance is made.
- Users may toggle back and forth freely without returning to the main application page.

If a ticker is invalid, Yahoo Finance returns no data, or a selected frequency produces no rows, the tab renders a friendly error card (including a Quarterly / Semiannual fallback switch) instead of the table.

---

## Global Core Layout Specifications

- **Hybrid Flask + Client-Side Architecture:** The frontend runs entirely inside the browser viewport, while a lightweight **Flask backend** (`app.py`) serves the page and provides a single `/proxy` endpoint used exclusively for fetching Yahoo Finance historical data.
- **Unified Global Theme Switcher:** Features a centralized master light/dark theme manager. Changes map instantly across all component blocks, typography color tokens, and custom alert cards.
- **Persistent Preferences:** Automatically mirrors user theme states using `localStorage`.
- **Fully Responsive Matrix UI:** Built from clean CSS grids and fluid flexbox structures.
- **Optimized Typography & Footprint:** Crisp font stack hierarchy and inline SVG assets for instant paint times.

---

## Prerequisites & Environment Setup

### Prerequisites

- **Python 3.8 or higher** — [Download Python](https://www.python.org/downloads/)
- **pip** (bundled with modern Python installations)

Verify your installation:

```bash
python --version
pip --version
```

### Step 1: Create a Virtual Environment

**Windows:**

```bash
python -m venv venv
```

**macOS / Linux:**

```bash
python3 -m venv venv
```

### Step 2: Activate the Virtual Environment

**Windows (Command Prompt):**

```bash
venv\Scripts\activate
```

**Windows (PowerShell):**

```powershell
.\venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install flask requests
```

Or create a `requirements.txt` with:

```text
flask
requests
```

Then install with:

```bash
pip install -r requirements.txt
```

### Step 4: Run the Application

```bash
python app.py
```

You should see:

```text
=======================================================
  Server Running
  Open:  http://localhost:5000
=======================================================
```

Open your browser and navigate to `http://localhost:5000`.

---

## How to Use the Suite

### Step 1: Initialize the Application

Run the Flask server:

```bash
python app.py
```

Then open `http://localhost:5000` in your browser.

### Step 2: Utilizing the Stock Researcher

1. **Define the Destination Market:** Begin typing the exchange name in the **Exchange Name** field. Select from the autocomplete registry.
2. **Input Asset Tickers:** Enter the ticker code in the **Ticker Symbol** field (e.g., `BBRI`, `AAPL`, `D05`).
3. **Choose Your Analytics Provider:** Select one of the four modes in the **Data Source Support** radio panel.
4. **Configure Your Focus Area (Checklist modes only):** Use the checkbox panel or the instant `All` / `None` triggers.
5. **Execute Research Tabs:** Click **Open All Selected Tabs** — or press `Enter` in the Exchange/Ticker/radio field.
   - If tabs do not open, allow pop-ups from the site, or use the manual link panel that appears below the controls.
6. **Switch Frequency Inside the Historical Data Tab (optional):** Use the **Quarterly** / **Semiannual** buttons in the blue header of the popup.

### Step 3: Operating the Click Counter

1. Click **CLICK HERE** to increment.
2. Use the `−` button to decrement by one (never below zero).
3. Use **Reset** and confirm the prompt to clear the counter.

### Step 4: Converting Data Typography

1. Paste or type raw text into the textarea.
2. Trigger one of the four case transformations.
3. Click **Copy to Clipboard** to export.

### Step 5: Using the Financial Shorthand Converter

1. Paste your list of values into the **Input** textarea.
2. (Optional) Adjust the **Reverse order** checkbox.
3. Click **Copy result**.
4. Paste into your Sheets spreadsheet — values will fill a row horizontally.

### Step 6: Extracting Ticker Symbols

1. Paste screener output into the **Input** textarea of the **📋 Ticker Symbol Extractor** card.
2. Review the auto-detected tickers in the **Output** textarea.
3. Adjust options as needed.
4. Click **Copy result**.
5. Paste into your spreadsheet.

---

## Keyboard Shortcuts

| Shortcut                                                                            | Context                   | Action                                                          |
| ----------------------------------------------------------------------------------- | ------------------------- | --------------------------------------------------------------- |
| `Enter`                                                                             | Exchange Name field       | Triggers **Open All Selected Tabs**                             |
| `Enter`                                                                             | Ticker Symbol field       | Triggers **Open All Selected Tabs**                             |
| `Enter`                                                                             | Radio/checkbox option     | Triggers **Open All Selected Tabs**                             |
| `Enter`                                                                             | Focused button            | Activates that specific button                                  |
| `Enter`                                                                             | Inside any textarea       | Inserts a new line (default browser behaviour)                  |
| `Ctrl+R` / `Cmd+R` / `Ctrl+Shift+R` / `Cmd+Shift+R` / `F5` / `Ctrl+F5` / `Shift+F5` | Anywhere on the main page | Blocked — refresh is intercepted to protect click-counter state |

> **Note:** Modern browsers may treat hard refresh shortcuts as a user-safety escape hatch and may not allow JavaScript to fully block them. For guaranteed prevention, run the app in kiosk mode or as a PWA/Electron shell. Inside the Historical Data popup, refresh shortcuts are **not** intercepted.

---

## Financial Shorthand Converter Reference

### Features

- **Suffix conversion** – `K` (×1,000), `M` (×1,000,000), `B` (×1,000,000,000), `T` (×1,000,000,000,000).
- **Percentage skipping** – Lines containing `%` are ignored.
- **Horizontal paste** – Output values are tab-separated.
- **Reverse order** – Optional checkbox (checked by default).
- **Exact math** – BigInt arithmetic.
- **Invisible character handling** – Strips zero-width and bidirectional control characters.
- **Responsive design** – Desktop, tablet, mobile.
- **One-click copy** – Copies the entire output.
- **No dependencies** – Single module with embedded CSS/JS.

### Quick Start

1. Start Flask with `python app.py` and open `http://localhost:5000`.
2. Paste values into the **Input** textarea.
3. (Optional) Adjust the **Reverse order** checkbox.
4. Click **Copy result**.
5. Paste into your Sheets spreadsheet.

### Input Format

- One value per line.
- Each line may contain: a number with optional decimal point, optional suffix (`K`, `M`, `B`, `T`, case-insensitive), optional sign (`+` or `−`).
- Lines containing `%` are skipped entirely.
- Blank lines are ignored.
- Extra spaces and invisible Unicode characters are cleaned automatically.

**Example input:**

```text
9.26 T
−2.05%
9.70 T
+4.25%
10.33 T
+9.01%
9.90 T
+1.90%
10.55 T
+13.93%
10.06 T
+3.75%
10.12 T
−2.02%
11.64 T
+17.60%
```

### Output Format

- Each valid input line produces a full integer with comma thousands separators (e.g., `9,260,000,000,000`).
- Percentage lines are omitted.
- All results are joined with a tab character (`\t`).

**Example output (with default Reverse order checked):**

```text
11,640,000,000,000	10,120,000,000,000	10,060,000,000,000	10,550,000,000,000	9,900,000,000,000	10,330,000,000,000	9,700,000,000,000	9,260,000,000,000
```

### Reverse Order Option

- **Checked (default):** Output is reversed. Newest becomes leftmost.
- **Unchecked:** Output preserves the original input order.

### How It Works

1. **Line parsing** – Each line is cleaned of invisible characters and trimmed.
2. **Percentage detection** – If a line contains `%`, it is skipped.
3. **Number extraction** – A regex captures sign, numeric part, and optional suffix.
4. **Suffix mapping** – The suffix maps to a BigInt multiplier.
5. **Exact multiplication** – The numeric string is split into integer and fractional parts.
6. **Formatting** – Commas inserted every three digits.
7. **Output assembly** – All converted values are collected, optionally reversed, and joined with tabs.

---

## Ticker Symbol Extractor Reference

### Ticker Extractor Features

- **Dual-format detection** — Accepts both alphabetic symbols (`NVDA`, `AMZN`, `DIS`) and numeric symbols (`2475`, `6951`, `679`).
- **Contextual confirmation** — A line is accepted as a ticker only if the next non-empty line looks like a company name or equals `D`.
- **Header noise filtering** — Common financial abbreviations are ignored.
- **Alphabetical sorting** — Default A → Z; one checkbox flips to Z → A.
- **Duplicate removal** — Enabled by default.
- **Flexible output shape** — One symbol per line or tab-separated single row.
- **Live statistics** — A badge above the output shows total count and sort direction.
- **One-click copy** — Pushes the entire output to your clipboard.
- **Sample loader** — Drops in a real export.
- **Zero dependencies** — Vanilla JavaScript only.

### Ticker Extractor Quick Start

1. Start Flask with `python app.py` and open `http://localhost:5000`.
2. Scroll to the **📋 Ticker Symbol Extractor** card.
3. Paste your screener output into the **Input** textarea.
4. (Optional) Adjust the checkboxes.
5. Click **Copy result**.
6. Paste into Excel or Google Sheets.

### Ticker Extractor Input Format

- Plain-text block containing ticker symbols on their own lines, immediately followed by a company name or the market marker `D`.
- Blank lines, header rows, numeric cells, and standalone short words are tolerated and ignored.

### Ticker Extractor Output Format

- **Column mode (default):** One ticker per line.
- **Tab-separated mode (checkbox):** All tickers joined by `\t`.

### Detection Rules

1. **Pattern match** — Trimmed line must be an alphabetic ticker (`^[A-Z][A-Z0-9]{1,5}$`) or numeric ticker (`^\d{3,6}$`).
2. **Noise filter** — The line must not be one of the reserved header abbreviations.
3. **Context confirmation** — Next non-empty line must contain lowercase OR be exactly `D` OR be followed by `D`.
4. **Deduplication (optional)** — If enabled, only the first occurrence is kept.

### Ticker Extractor Options

| Option                         | Default | Effect                                            |
| ------------------------------ | ------- | ------------------------------------------------- |
| **Remove duplicates**          | ✓ On    | Only the first occurrence of each ticker is kept. |
| **Sort Z → A**                 | Off     | Reverses the alphabetical sort order.             |
| **Tab-separated (single row)** | Off     | Joins the output with `\t` instead of `\n`.       |

### Ticker Extractor How It Works

1. **Line splitting** — Input is split on `\r\n` or `\n`.
2. **Trim & match** — Each line is trimmed and tested against the ticker regex.
3. **Noise rejection** — Reserved header words are skipped.
4. **Context lookahead** — Next two non-empty lines are inspected.
5. **Dedup collection** — Surviving tickers are pushed into the result array.
6. **Sort** — Lexicographic sort (A → Z by default).
7. **Join** — Joined with `\n` or `\t` and written to the output.
8. **Statistics** — The stats badge is updated.

---

## Customization

You can easily modify the tools by editing the source in `app.py`:

- **Sample data (Financial Shorthand Converter)** — Change the `SAMPLE` array inside its IIFE.
- **Sample data (Ticker Symbol Extractor)** — Change the `SAMPLE` array inside its IIFE.
- **Ticker detection rules** — Adjust the `TICKER_RE` regex and the `NOISE` object.
- **Ticker context confirmation** — Edit the `looksLikeTicker` condition.
- **Multipliers (Financial Shorthand Converter)** — Adjust the `MULT` object.
- **Placeholder text** — Update `placeholder` attributes on any textarea.
- **Styling** — All CSS is embedded in the `<style>` block inside `HTML_PAGE`.
- **Historical table layout** — The transposed Historical Data table is generated inside `openHistoryTab()`.
- **Default historical frequency** — Modify `let freq = (initialFreq === "semiannual") ? "semiannual" : "quarterly";`.
- **Quarterly / Semiannual grouping logic** — Handled inside `processPeriodData(timestamps, closes, freq)`.
- **Package tab delay** — Adjust the `350` millisecond timeout inside `processSearch()`.
- **Proxy timeout** — The `/proxy` route uses a 15-second timeout.
- **Refresh shortcut interception** — Edit the `isRefreshCombo` condition inside the `keydown` listener.

No build step is required — the Flask server hosts the single-file frontend.

---

## Browser Support

The tool works in all modern browsers that support:

- ES6+ (arrow functions, `const`/`let`, template literals).
- BigInt (Chrome 67+, Firefox 68+, Safari 14+, Edge 79+).
- Async clipboard API (or fallback to `document.execCommand('copy')`).
- `fetch` API for the local Historical Data proxy.

For older browsers, the fallback copy method may work, but BigInt support is essential.

---

## Troubleshooting

> **Note:** The main page intercepts refresh shortcuts (`Ctrl+R`, `Ctrl+Shift+R`, `F5`, `Ctrl+F5`, `Shift+F5`). If you need to force a refresh to clear a cache, use your browser's menu (e.g., View → Reload) or open the page in a new incognito window. Inside the Historical Data popup, refresh shortcuts are **not** intercepted.

| Issue                                          | Possible Cause                               | Solution                                                                                                       |
| ---------------------------------------------- | -------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| Copy button does nothing                       | Browser blocks clipboard access              | Use a secure context (HTTPS or localhost) or copy manually from the output textarea.                           |
| Values not pasting horizontally                | Spreadsheet settings                         | Ensure you paste into a single cell and the tab character is preserved.                                        |
| Wrong number of columns (Shorthand Converter)  | Input contains unrecognised lines            | Check the stats indicator; unrecognised lines are silently ignored.                                            |
| Reverse order not working                      | Checkbox state                               | Make sure the checkbox is checked if you need reversed output.                                                 |
| Large numbers lose precision                   | JavaScript number limitations                | The tool uses BigInt, so precision is maintained.                                                              |
| `Enter` does not trigger search                | Focused inside a `<textarea>`                | Textareas intentionally keep native newline behaviour. Move focus to the Exchange/Ticker field.                |
| Package mode launched too few tabs             | Fixed bundle of 6 tabs is expected           | This is by design. Switch to StockAnalysis or TradingView mode for granular control.                           |
| Historical Data tab shows error                | Flask `/proxy` unreachable or ticker invalid | Ensure `python app.py` is running and the page is loaded from `http://localhost:5000`.                         |
| Historical Data favicon still shows old emoji  | Browser favicon cache                        | Open the popup in an incognito window, or reload the main page.                                                |
| Historical table dates not aligned with prices | Horizontal scrolling is expected             | The table is intentionally transposed. The leftmost label column stays sticky.                                 |
| Quarterly / Semiannual toggle not visible      | Browser cached the old popup template        | Open the main page in an incognito window or reload the page.                                                  |
| Semiannual mode shows fewer rows than expected | Only June & December are kept                | This is by design — Semiannual mode keeps exactly the two half-year ends per year.                             |
| Ticker Extractor returns 0 tickers             | Input format doesn't match detection rules   | Click **Load sample** to compare shapes. Ensure ticker lines are followed by a company name or the `D` marker. |
| Ticker Extractor includes false positives      | Header word not in the noise list            | Add the word to the `NOISE` object inside the Ticker Symbol Extractor IIFE.                                    |
| Ticker Extractor misses some symbols           | Symbol format not matched by the regex       | Extend `TICKER_RE` to include the missing format.                                                              |
| Ticker Extractor output order looks odd        | Numeric sorting is lexicographic             | By design, tickers are sorted as strings.                                                                      |

---

## Unified Architecture & Technologies Used

- **Flask (Python) Backend:** `app.py` serves the single-file frontend via `render_template_string` and exposes a `/proxy` endpoint that forwards requests to Yahoo Finance for historical price data.
- **HTML5 Elements:** Structured content layout separating input contexts from interactive control modules.
- **CSS3 Variables & Responsive Design:** Centralized color variables handle real-time theme swapping; mobile-first layout engine.
- **Vanilla JavaScript (ES6+):** Manages local caching layers, typography transformations, tracking variables, URL mapping, the local Historical Data tab, and the Ticker Symbol Extractor. The main page also runs a capture-phase `keydown` listener to intercept refresh shortcuts.
- **SweetAlert2 Library Integration:** Modern, non-blocking toast popups and validation dialogs that match the selected system theme.
- **BigInt Arithmetic:** Exact financial suffix conversion without floating-point precision loss.
- **Regex-Based Parsing:** The Ticker Symbol Extractor uses `^([A-Z][A-Z0-9]{1,5}|\d{3,6})$` to accept both alphabetic and numeric ticker formats in a single pass.
- **Clipboard API Integration:** One-click copy operations across the suite, with fallback support.
- **`requests` (Python):** Used by the Flask `/proxy` route to make outbound HTTP calls to Yahoo Finance with a desktop User-Agent header.

---

## License

This suite is provided as-is for personal and commercial use. No warranty is expressed or implied. You are free to modify and distribute it.
