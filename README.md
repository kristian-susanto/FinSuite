# FinSuite — Unified Tool Suite Documentation

Welcome to the unified documentation for **FinSuite**. FinSuite combines five essential tools into a single, high-performance web interface: the **Stock Multi-Tab Researcher**, **Click Counter**, **Text Case Converter**, **Financial Shorthand Converter**, and **Ticker Symbol Extractor**.

This README merges all references into one unified guide for professional workflows, capital market analytics, productivity tracking, and financial data preparation.

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
- [Global Core Layout Specifications](#global-core-layout-specifications)
- [Prerequisites & Environment Setup](#prerequisites--environment-setup)
  - [Prerequisites](#prerequisites)
  - [Step 1: Create a Virtual Environment](#step-1-create-a-virtual-environment)
  - [Step 2: Activate the Virtual Environment](#step-2-activate-the-virtual-environment)
  - [Step 3: Install Dependencies](#step-3-install-dependencies)
  - [Step 4: Run the Application](#step-4-run-the-application)
- [How to Use the Suite](#how-to-use-the-suite)
  - [Step 1: Initialize the Application](#step-1-initialize-the-application)
  - [Step 2: Utilizing the Stock Researcher](#step-2-utilizing-the-stock-researcher)
  - [Step 3: Operating the Click Counter](#step-3-operating-the-click-counter)
  - [Step 4: Converting Data Typography](#step-4-converting-data-typography)
  - [Step 5: Using the Financial Shorthand Converter](#step-5-using-the-financial-shorthand-converter)
  - [Step 6: Extracting Ticker Symbols](#step-6-extracting-ticker-symbols)
- [Keyboard Shortcuts](#keyboard-shortcuts)
- [Financial Shorthand Converter Reference](#financial-shorthand-converter-reference)
  - [Features](#features)
  - [Quick Start](#quick-start)
  - [Input Format](#input-format)
  - [Output Format](#output-format)
  - [Reverse Order Option](#reverse-order-option)
  - [How It Works](#how-it-works)
- [Ticker Symbol Extractor Reference](#ticker-symbol-extractor-reference)
  - [Features](#ticker-extractor-features)
  - [Quick Start](#ticker-extractor-quick-start)
  - [Input Format](#ticker-extractor-input-format)
  - [Output Format](#ticker-extractor-output-format)
  - [Detection Rules](#detection-rules)
  - [Options](#ticker-extractor-options)
  - [How It Works](#ticker-extractor-how-it-works)
  - [Examples](#ticker-extractor-examples)
- [Customization](#customization)
- [Browser Support](#browser-support)
- [Troubleshooting](#troubleshooting)
- [Unified Architecture & Technologies Used](#unified-architecture--technologies-used)
- [License](#license)

---

## Overview

The suite is a unified collection that provides complementary productivity, analytics, and financial data preparation tools:

1. **Stock Multi-Tab Researcher** — Launch multiple research tabs for a selected exchange, ticker, and data provider, including a locally rendered historical data view.
2. **Click Counter** — Track high-frequency click interactions with temporary tally state and safe reset controls.
3. **Text Case Converter** — Transform text between uppercase, lowercase, title case, and sentence case.
4. **Financial Shorthand Converter** — Convert `K`, `M`, `B`, and `T` financial shorthand values into full integers for spreadsheet workflows.
5. **Ticker Symbol Extractor** — Extract, deduplicate, and alphabetically sort ticker symbols from raw screener output for clean spreadsheet pasting.

Together, these tools eliminate context switching by combining productivity utilities, capital market analytics, and financial data normalization in one browser-based application.

---

## Core Key Features

### 1. 📊 Stock Multi-Tab Researcher

Designed for investors, traders, and financial analysts to eliminate repetitive browser research by triggering deep-dive analysis pipelines simultaneously with a single action.

- **Multi-Tab Execution Workflow:** Generates and launches custom analytical URLs instantly, mapping exchange codes and asset symbols dynamically.
- **Cross-Global Exchange Resolution System:** Out-of-the-box support for international markets including NYSE, HKG, SGX, SSE, TYO, and more.
- **Granular Data Point Filtering:** Choose precisely which dimensions to investigate (e.g., Latest News, Financial Ratios, Historical Trends, Balance Sheets, Income Statements, Cash Flow Metrics, or Dividend Trackers). This checklist applies to **TradingView** and **StockAnalysis** modes.
- **Four Data Source Modes:** Switch the structural parsing logic between **Quarterly Package**, **Semester Package**, **TradingView**, or **StockAnalysis** depending on your data pipeline preferences.
- **Package Modes (Quarterly & Semester):** One-click bundled workflows that ignore the granular checklist and launch a fixed set of **6 analytical tabs** in a single action — combining StockAnalysis, TradingView, and a locally rendered historical data view.
  - **Quarterly Package (default):** TradingView financial statement URLs use the `FQ` period parameter.
  - **Semester Package:** TradingView financial statement URLs use the `FH` period parameter. The local Historical Data popup still opens in **Quarterly** mode by default, and you can switch it to **Semiannual** inside the popup.
- **Local Historical Data View:** The ⏳ **Historical Data** tab is rendered on the fly by the Flask backend. It queries Yahoo Finance daily closes (10 years), reduces them to period-end closes, and displays them in a **transposed, responsive table** with a **Latest Close** column always shown first (leftmost), followed by period columns. The tab includes an **in-popup Quarterly / Semiannual toggle** so the user can switch reporting frequency without returning to the main page.
- **In-Popup Frequency Toggle:** The Historical Data popup carries its own **Quarterly** (default) and **Semiannual** toggle in the header. Clicking either button re-renders the table instantly using the already-cached daily data — no additional network request is issued.
- **Context-Aware Keyboard Shortcut:** Pressing `Enter` inside the Exchange Name field, Ticker Symbol field, or any non-textarea/non-button form control immediately triggers the research pipeline — no need to move your mouse to the button.
- **Fail-Safe Manual Backup Registry:** Embedded link presentation tier ensures that if a modern browser blocks multi-popups, backup clickable links render seamlessly to bypass security restrictions.

### 2. 🖱️ Click Counter

A lightweight, reactive digital tallying and micro-interaction sandbox designed for high-frequency tracking.

- **Micro-Interaction Visual System:** Live viewport numbers dynamically expand and contract using hardware-accelerated CSS scaling matrices upon click inputs for clear visual feedback.
- **Refresh Shortcut Interception:** Intercepts volatile browser events (such as accidental keyboard `F5`, `Ctrl+R`, `Ctrl+Shift+R`, `Ctrl+F5`, and `Shift+F5` refreshes) to help protect the temporary click count from unintended page reloads. The handler uses the capture phase and `stopPropagation` for maximum coverage. **Note:** Modern browsers may still allow hard refresh shortcuts to pass through as a user-safety feature; see the [Keyboard Shortcuts](#keyboard-shortcuts) section for details.
- **Safe Reset Dialogs:** Employs explicit user-intent confirmations before wiping state tracking records back to zero.
- **Decrement Control:** Includes a dedicated `−` button to reduce the current count by one when the value is greater than zero.

### 3. 🔤 Text Case Converter

A professional-grade typographical formatting workstation tailored for developers, copywriters, and structured data cleaners.

- **Multi-State Transformation Matrix:**
  - `UPPERCASE`: Standardizes code variables, tickers, or headings into all capital letters.
  - `lowercase`: Converts strings to lowercase formats for normalized database ingestions.
  - `Capitalize Word`: Formats strings into title-case blocks by auto-capitalizing every segmented word.
  - `Sentence case`: Corrects running prose by adjusting only the initial character of text sequences.
- **One-Click Buffer Interface:** Directly interacts with the system clipboard APIs for frictionless, one-tap copy operations.
- **Clear Action Feedback:** Displays a toast confirmation after clearing text from the workspace.

### 4. 💰 Financial Shorthand Converter

A lightweight, responsive module that converts shorthand financial values with **K**, **M**, **B**, and **T** suffixes into full numbers. It automatically skips percentage lines, outputs tab-separated values for easy pasting into Sheets (horizontally), and includes an optional reverse-order feature to match right-to-left spreadsheet layouts.

- **Suffix conversion** — Converts `K` (×1,000), `M` (×1,000,000), `B` (×1,000,000,000), and `T` (×1,000,000,000,000) to full integers.
- **Percentage skipping** — Lines containing a `%` sign are ignored automatically.
- **Horizontal paste** — Output values are separated by tabs (`\t`), so they paste across a row in Sheets.
- **Reverse order** — Optional checkbox to reverse the output order, ideal for spreadsheets that list newest data on the left.
- **Exact math** — Uses BigInt arithmetic to avoid floating-point errors with very large numbers.
- **Invisible character handling** — Strips zero-width and bidirectional control characters that often come with copied data.
- **Responsive design** — Works on desktop, tablet, and mobile.
- **One-click copy** — Copies the entire output to the clipboard.
- **No dependencies** — Implemented in vanilla JavaScript with no external runtime libraries.

### 5. 📋 Ticker Symbol Extractor

A precision parsing module that ingests raw screener output and returns a clean, deduplicated, alphabetically sorted list of ticker symbols — ready to paste as a spreadsheet column or a single tab-separated row.

- **Dual-format ticker detection** — Recognises both **alphabetic symbols** (e.g., `NVDA`, `AMZN`, `DIS`) and **numeric symbols** (e.g., `2475`, `6951`, `679`) so it works with US markets, ASEAN exchanges, and Hong Kong stock codes alike.
- **Context-aware confirmation** — A line is only accepted as a ticker if the following non-empty line looks like a company name (contains lowercase characters) or is the standalone market marker `D` (as produced by StockAnalysis screener exports). This prevents header rows, numeric cells, and unrelated short lines from polluting the output.
- **Header noise filtering** — Common financial header abbreviations (`TTM`, `EPS`, `YOY`, `QOQ`, `ETF`, `IPO`, `CEO`, `CFO`, `ROE`, `ROA`, `ROI`, `NAV`, `ALL`, `NONE`, `NA`) are automatically discarded.
- **Alphabetical sorting (A → Z)** — The default output order; a single checkbox flips it to **Z → A** for reverse workflows.
- **Duplicate removal** — On by default; toggle it off to preserve every occurrence in the source.
- **Flexible output shape** — Choose **one symbol per line** (ready for a column) or **tab-separated single row** (ready for a row) with a single checkbox.
- **Live statistics badge** — Displays how many tickers were extracted and which sort direction is active (e.g., `22 tickers · A → Z`).
- **One-click copy** — The **Copy result** button pushes the entire output to your clipboard, ready to paste into Excel or Google Sheets.
- **Built-in sample loader** — The **Load sample** button populates the input with a real-world Hong Kong electronic technology screener export so you can test the parser without hunting for your own data.
- **No dependencies** — Pure vanilla JavaScript, zero external libraries.

---

## Stock Researcher — Data Source Modes

The Stock Multi-Tab Researcher supports four data-source modes, selectable through the **Data Source Support** radio panel. The selected mode determines which URLs are generated, how ticker casing is normalized, and whether the granular checklist is used.

| Mode                  | Default | Checklist Used? | Tabs Opened | Description                                                                                                                                                                           |
| --------------------- | :-----: | :-------------: | :---------: | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Quarterly Package** |   ✅    |       No        |      6      | Fixed multi-source bundle (StockAnalysis + TradingView + Local Historical Data) with TradingView financial statement period `FQ`. Ideal for quarterly deep-dive research.             |
| **Semester Package**  |    —    |       No        |      6      | Fixed multi-source bundle (StockAnalysis + TradingView + Local Historical Data) with TradingView financial statement period `FH`. Local historical popup still defaults to Quarterly. |
| **TradingView**       |    —    |       Yes       |    1 – 9    | Granular control; only the checklist-selected data points are opened. Tickers are normalized to uppercase, exchange codes are remapped.                                               |
| **StockAnalysis**     |    —    |       Yes       |    1 – 9    | Granular control; only the checklist-selected data points are opened. Generated URLs use lowercase exchange/ticker values.                                                            |

### Package Modes — Fixed 6-Tab Bundle

When **Quarterly Package** or **Semester Package** is selected, the data-point checklist is dimmed and disabled, and clicking **Open All Selected Tabs** immediately launches the following six analytical views:

| #   | Data Point          | Provider                      | Purpose                                                        | Period Parameter                                                           |
| --- | ------------------- | ----------------------------- | -------------------------------------------------------------- | -------------------------------------------------------------------------- |
| 1   | 🏢 Overview         | StockAnalysis                 | Company profile, sector, business summary                      | —                                                                          |
| 2   | 🏢 Overview         | TradingView                   | Company profile, sector, business summary                      | —                                                                          |
| 3   | 📑 Income Statement | TradingView                   | Income statement                                               | `FQ` for Quarterly Package / `FH` for Semester Package                     |
| 4   | ⚖️ Balance Sheet    | TradingView                   | Balance sheet                                                  | `FQ` for Quarterly Package / `FH` for Semester Package                     |
| 5   | 📊 Ratios           | TradingView                   | Statistics and valuation ratios                                | `FQ` for Quarterly Package / `FH` for Semester Package                     |
| 6   | ⏳ Historical Data  | Local (Flask + Yahoo Finance) | Latest close + Quarterly / Semiannual closes over the last 10y | Opens Quarterly by default; can be switched to Semiannual inside the popup |

Package modes are intentionally unconfigurable on the main page — they are fixed reconnaissance bundles designed so that switching between providers is not necessary when you simply want comprehensive coverage of a ticker. The locally rendered **Historical Data** tab is unique to Package modes and is opened via a client-side fetch to the Flask `/proxy` endpoint. Frequency (Quarterly vs. Semiannual) is chosen **inside the popup**, not on the main page.

### Local Historical Data Tab

When the ⏳ **Historical Data** target is executed (only available inside Package modes), the application opens a fresh browser tab and performs the following:

1. Resolves the ticker to a Yahoo Finance symbol using the exchange suffix map (e.g., `HKG → .HK`).
2. Calls the Flask `/proxy?symbol=…&range=10y&interval=1d` endpoint, which forwards the request to Yahoo Finance with a desktop User-Agent header.
3. Caches the returned daily closes in memory — the data is fetched **once per popup**.
4. Reduces the daily data to **period-end closing prices** based on the currently selected frequency:
   - **Quarterly (default)** — one data point per calendar quarter (Mar / Jun / Sep / Dec).
   - **Semiannual** — one data point per half-year, keeping only **June** and **December** closes.
5. Renders a **transposed, responsive table** with a **Latest Close** column always shown first (leftmost), followed by the most recent period column to the right:

   | **Period**      | **Latest** | 9M2026     | 1H2026     | 1Q2026     | FY2025     | 9M2025     | 1H2025     | 1Q2025     |
   | --------------- | ---------- | ---------- | ---------- | ---------- | ---------- | ---------- | ---------- | ---------- |
   | **Actual Date** | 2026-09-22 | 2026-09-18 | 2026-06-30 | 2026-03-31 | 2025-12-30 | 2025-09-30 | 2025-06-30 | 2025-03-27 |
   | **Close Price** | 6,200.00   | 6,300.00   | 5,550.00   | 6,450.00   | 8,075.00   | 7,625.00   | 8,675.00   | 8,500.00   |
   - **Latest column:** Shows the most recent trading day's actual date and close. Styled identically to every other column (same stripe header, same border, same font weight) so the table reads as one uniform grid.
   - **Row 1 — Period (header):** Compact labels derived from the period-end month:
     - March → `1Q<year>` (e.g., `1Q2026`)
     - June → `1H<year>` (e.g., `1H2026`)
     - September → `9M<year>` (e.g., `9M2026`)
     - December → `FY<year>` (e.g., `FY2025`)
   - **Row 2 — Actual Date:** Actual trading date of the period-end close (or the latest trading day for the _Latest_ column).
   - **Row 3 — Close Price:** Period-end closing price in the listing currency.
   - The leftmost **Period / Actual Date / Close Price** label column is **sticky**, so it stays visible while scrolling horizontally.
   - The **Period** header uses the same font size and weight as the other column headers so all columns look visually consistent.
   - The table uses a 💼 favicon, matches the global light/dark theme via `prefers-color-scheme`, and adapts its padding/typography on mobile screens.

### In-Popup Frequency Toggle

The Historical Data popup carries its own frequency selector in the blue header, positioned below the title:

```text
┌──────────────────────────────────────────────────────┐
│  BBCA.JK — Historical Data                           │
│  Quarter-End Closing Prices · Last 10 Years · …      │
│  ┌───────────┬────────────┐                          │
│  │ Quarterly │ Semiannual │  ← click to switch       │
│  └───────────┴────────────┘                          │
└──────────────────────────────────────────────────────┘
```

- **Quarterly** is active by default and displays every quarter-end close.
- Clicking **Semiannual** immediately re-renders the table to show only June and December closes.
- The switch is **instant and offline** — no additional request to Flask or Yahoo Finance is made. The popup keeps the original daily closes cached in memory and simply re-runs the period-grouping logic.
- The active button is highlighted white against the blue header; the inactive button blends into the header background.
- Users may toggle back and forth freely without ever returning to the main application page.

The **main page** intentionally does _not_ expose a frequency selector. Package modes always open the popup in **Quarterly** mode, and the user changes it from inside the popup if desired.

If a ticker is invalid, Yahoo Finance returns no data, or a selected frequency produces no rows, the tab renders a friendly error card (including a Quarterly / Semiannual fallback switch) instead of the table.

---

## Global Core Layout Specifications

- **Hybrid Flask + Client-Side Architecture:** The frontend runs entirely inside the browser viewport, while a lightweight **Flask backend** (`app.py`) serves the page and provides a single `/proxy` endpoint used exclusively for fetching Yahoo Finance historical data.
- **Unified Global Theme Switcher:** Features a centralized master light/dark theme manager. Changes map instantly across all component blocks, typography color tokens, and custom alert cards.
- **Persistent Preferences:** Automatically mirrors user theme states using modern browser `localStorage`, ensuring your preferred interface style persists across subsequent sessions.
- **Fully Responsive Matrix UI:** Built from the ground up using clean CSS grids and fluid flexbox structures. Seamlessly transforms between compact mobile screens, tablets, and extensive multi-monitor setups.
- **Optimized Typography & Footprint:** Employs a crisp font stack hierarchy and inline SVG assets to ensure instant paint times and high layout performance.

---

## Prerequisites & Environment Setup

Before running the suite, ensure you have the following installed on your machine.

### Prerequisites

- **Python 3.8 or higher** — [Download Python](https://www.python.org/downloads/)
- **pip** (Python package installer, bundled with modern Python installations)

Verify your installation by running:

```bash
python --version
pip --version
```

### Step 1: Create a Virtual Environment

It is strongly recommended to isolate your project dependencies using a virtual environment. Navigate to the project folder containing `app.py`, then run:

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

Once activated, your terminal prompt should be prefixed with `(venv)`.

### Step 3: Install Dependencies

The suite requires **Flask** and **requests**. Install them with:

```bash
pip install flask requests
```

> **Tip:** You can also create a `requirements.txt` file containing:
>
> ```text
> flask
> requests
> ```
>
> Then install with `pip install -r requirements.txt`.

### Step 4: Run the Application

Start the Flask development server:

```bash
python app.py
```

You should see the following banner in your terminal:

```text
=======================================================
  Server Running
  Open:  http://localhost:5000
=======================================================
```

Open your browser and navigate to `http://localhost:5000` to access the application.

---

## How to Use the Suite

### Step 1: Initialize the Application

Run the Flask server from your terminal:

```bash
python app.py
```

Then open your browser and navigate to:

```text
http://localhost:5000
```

The console will print the server banner and the exact URL for convenience.

### Step 2: Utilizing the Stock Researcher

1. **Define the Destination Market:** Begin typing the name of an exchange in the **Exchange Name** text area. Select from the automated global autocomplete registry (e.g., _Indonesia Stock Exchange (Indonesia)_ or _Nasdaq Stock Market (United States)_).
2. **Input Asset Tickers:** Input your specific tracking target code into the **Ticker Symbol** field (e.g., `BBRI`, `AAPL`, or `D05`).
3. **Choose Your Analytics Provider:** Select one of the four modes in the **Data Source Support** radio panel:
   - **📦 Quarterly Package (default)** — Skips the checklist and launches a fixed 6-tab bundle across StockAnalysis, TradingView, and the local Historical Data view. TradingView financial statement URLs use `FQ`.
   - **📦 Semester Package** — Skips the checklist and launches a fixed 6-tab bundle across StockAnalysis, TradingView, and the local Historical Data view. TradingView financial statement URLs use `FH`. The local Historical Data popup still opens in Quarterly mode by default.
   - **TradingView** — Enables the checklist; only selected data points are opened. Tickers are normalized to uppercase and exchange codes are remapped (e.g., `SHA` → `SSE`).
   - **StockAnalysis** — Enables the checklist; only selected data points are opened. Generated URLs use lowercase exchange/ticker values.
4. **Configure Your Focus Area (Checklist modes only):** If you are in StockAnalysis or TradingView mode, use the checkbox panel to specify the modules you need. You can use the instant `All` or `None` triggers to modify selections quickly. _(This panel is disabled in Package modes.)_
5. **Execute Research Tabs:** Click **Open All Selected Tabs** — or simply press `Enter` while focused on the Exchange Name, Ticker Symbol, or a radio/checkbox option.
   - _Note on Security Blocks:_ If the tabs do not open immediately, check your browser's address bar for a "Pop-up Blocked" icon, select "Always allow pop-ups from this source," and retry. Alternatively, use the manually generated reference panel that appears below the controls.
   - _Note on the Historical Data tab:_ Because the historical view is fetched from your local Flask server, it must run from `http://localhost:5000` (or your deployed host). Opening the HTML file directly from the filesystem will disable the proxy call.
6. **Switch Frequency Inside the Historical Data Tab (optional):** Once the ⏳ **Historical Data** popup is open, use the **Quarterly** / **Semiannual** buttons in the blue header to switch how period closes are grouped. The table re-renders instantly with no additional network request. The **Latest** column always remains the leftmost column.

### Step 3: Operating the Click Counter

1. Click or tap the primary **CLICK HERE** module to increment tally parameters seamlessly.
2. Use the `−` button to decrement the current count by one. The counter will not go below zero.
3. To clear the counting buffer, activate the red **Reset** button and accept the verification prompt.

### Step 4: Converting Data Typography

1. Paste or type any alphanumeric raw data strings inside the centralized textarea.
2. Trigger any of the four available case transformations to modify text values instantly:
   - `UPPERCASE`
   - `lowercase`
   - `Capitalize Word`
   - `Sentence case`
3. Click **Copy to Clipboard** to export your formatted text directly into your workflow buffers.

### Step 5: Using the Financial Shorthand Converter

1. Paste your list of values into the **Input** textarea.
2. (Optional) Adjust the **Reverse order** checkbox if needed.
3. Click **Copy result**.
4. Paste into your Sheets spreadsheet — values will fill a row horizontally.

### Step 6: Extracting Ticker Symbols

1. **Paste your screener output:** Copy rows directly from your screener (StockAnalysis, TradingView, or any source that lists ticker symbols on their own line, followed by a company name or the market marker `D`) and paste them into the **Input** textarea of the **📋 Ticker Symbol Extractor** card.
2. **Review the auto-detected tickers:** The **Output** textarea updates live and shows the extracted, deduplicated, alphabetically sorted tickers. A stats badge above the output displays the total count and the active sort direction (e.g., `22 tickers · A → Z`).
3. **Adjust options as needed** (see [Ticker Symbol Extractor Options](#ticker-extractor-options)):
   - **Remove duplicates** — On by default; uncheck to preserve every occurrence.
   - **Sort Z → A** — Off by default; check to reverse the alphabetical order.
   - **Tab-separated (single row)** — Off by default; check if you want to paste the tickers as a horizontal row rather than a column.
4. **Copy the result:** Click **Copy result** to push the formatted output to your clipboard.
5. **Paste into your spreadsheet:** Because the output is deduplicated, alphabetically sorted, and (optionally) tab-separated, it drops cleanly into Excel or Google Sheets without further cleanup.

> **Tip:** If your screener produces an unexpected format, click **Load sample** to see exactly what input shape the suite expects, then compare it against your own data.

---

## Keyboard Shortcuts

| Shortcut                                                                                            | Context                   | Action                                                                                                    |
| --------------------------------------------------------------------------------------------------- | ------------------------- | --------------------------------------------------------------------------------------------------------- |
| `Enter`                                                                                             | Exchange Name field       | Triggers **Open All Selected Tabs**                                                                       |
| `Enter`                                                                                             | Ticker Symbol field       | Triggers **Open All Selected Tabs**                                                                       |
| `Enter`                                                                                             | Radio/checkbox option     | Triggers **Open All Selected Tabs**                                                                       |
| `Enter`                                                                                             | Focused button            | Activates that specific button                                                                            |
| `Enter`                                                                                             | Inside any textarea       | Inserts a new line (default browser behaviour)                                                            |
| `Ctrl + R` / `Cmd + R` / `Ctrl + Shift + R` / `Cmd + Shift + R` / `F5` / `Ctrl + F5` / `Shift + F5` | Anywhere on the main page | Blocked — refresh is intercepted to protect click-counter state (browser may still override hard refresh) |

> **Note:** Modern browsers may treat hard refresh shortcuts (`Ctrl+Shift+R`, `Ctrl+F5`) as a user-safety escape hatch and may not allow JavaScript to fully block them. The main page uses a capture-phase `keydown` listener with `preventDefault()` and `stopPropagation()` to intercept as many refresh combinations as possible, but for guaranteed prevention, run the app in kiosk mode or as a PWA/Electron shell. Inside the Historical Data popup, use the mouse (or a screen-reader click) on the **Quarterly** / **Semiannual** buttons to switch frequency. The keyboard `Enter` interception only applies to the main application page.

---

## Financial Shorthand Converter Reference

The Financial Shorthand Converter is a lightweight, responsive web tool that converts shorthand financial values with **K**, **M**, **B**, and **T** suffixes into full numbers. It automatically skips percentage lines, outputs tab-separated values for easy pasting into Sheets (horizontally), and includes an optional reverse-order feature to match right-to-left spreadsheet layouts.

### Features

- **Suffix conversion** – Converts `K` (×1,000), `M` (×1,000,000), `B` (×1,000,000,000), and `T` (×1,000,000,000,000) to full integers.
- **Percentage skipping** – Lines containing a `%` sign are ignored automatically.
- **Horizontal paste** – Output values are separated by tabs (`\t`), so they paste across a row in Sheets.
- **Reverse order** – Optional checkbox to reverse the output order, ideal for spreadsheets that list newest data on the left.
- **Exact math** – Uses BigInt arithmetic to avoid floating-point errors with very large numbers.
- **Invisible character handling** – Strips zero-width and bidirectional control characters that often come with copied data.
- **Responsive design** – Works on desktop, tablet, and mobile.
- **One-click copy** – Copies the entire output to the clipboard.
- **No dependencies** – A single module with embedded CSS and JavaScript.

### Quick Start

1. Start the Flask server with `python app.py` and open `http://localhost:5000` in any modern web browser.
2. Paste your list of values into the **Input** textarea.
3. (Optional) Adjust the **Reverse order** checkbox if needed.
4. Click **Copy result**.
5. Paste into your Sheets spreadsheet – values will fill a row horizontally.

### Input Format

- One value per line.
- Each line may contain:
  - A number with optional decimal point (e.g., `9.26`, `10`, `11.64`).
  - An optional suffix: `K`, `M`, `B`, or `T` (case-insensitive).
  - An optional sign: `+` or `−` (the tool normalises various dash characters).
- Lines that contain a `%` symbol are skipped entirely.
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
- All results are joined with a tab character (`\t`), so they appear on a single line in the output textarea.
- When pasted into Sheets, each value occupies its own cell in a row.

**Example output (for the input above):**

```text
9,260,000,000,000	9,700,000,000,000	10,330,000,000,000	9,900,000,000,000	10,550,000,000,000	10,060,000,000,000	10,120,000,000,000	11,640,000,000,000
```

> **Note:** If the **Reverse order** checkbox is checked, the output sequence is reversed (e.g., `11,640,000,000,000` first).

### Reverse Order Option

Many financial spreadsheets place the most recent period on the left and older periods on the right. If your input list is ordered from oldest to newest (left to right), enabling **Reverse order** will flip the sequence so the newest value appears first when pasted.

- **Checked (default):** Output is reversed. Newest (last in input) becomes first (leftmost in spreadsheet).
- **Unchecked:** Output preserves the original input order.

You can toggle this checkbox at any time; the output updates instantly.

### How It Works

1. **Line parsing** – Each line is cleaned of invisible characters and trimmed.
2. **Percentage detection** – If a line contains `%`, it is skipped.
3. **Number extraction** – A regular expression captures the sign, numeric part, and optional suffix.
4. **Suffix mapping** – The suffix is mapped to a BigInt multiplier:
   - `K` → 1,000
   - `M` → 1,000,000
   - `B` → 1,000,000,000
   - `T` → 1,000,000,000,000
   - No suffix → 1
5. **Exact multiplication** – The numeric string is split into integer and fractional parts. Both the scale (10^fraction length) and the multiplier are powers of ten, so the conversion is exact using BigInt arithmetic.
6. **Formatting** – The resulting integer is converted to a string and commas are inserted every three digits.
7. **Output assembly** – All converted values are collected, optionally reversed, and joined with tabs.

---

## Ticker Symbol Extractor Reference

The Ticker Symbol Extractor is a client-side parser that turns raw screener output into a clean, deduplicated, alphabetically sorted list of ticker symbols. It is designed for workflows where you copy a screener result set (for example, from StockAnalysis or TradingView), then need a neat column of symbols to paste into a spreadsheet.

### Ticker Extractor Features

- **Dual-format detection** — Accepts both alphabetic symbols (`NVDA`, `AMZN`, `DIS`) and numeric symbols (`2475`, `6951`, `679`) so it handles US, ASEAN, and Hong Kong markets without configuration.
- **Contextual confirmation** — A line is accepted as a ticker only if the next non-empty line looks like a company name (contains lowercase characters) or equals `D` (the StockAnalysis market marker). This eliminates header rows, numeric cells, and unrelated short lines.
- **Header noise filtering** — Common financial abbreviations are ignored automatically: `TTM`, `EPS`, `YOY`, `QOQ`, `ETF`, `IPO`, `CEO`, `CFO`, `ROE`, `ROA`, `ROI`, `NAV`, `ALL`, `NONE`, `NA`.
- **Alphabetical sorting** — Default output order is A → Z; a single checkbox flips it to Z → A.
- **Duplicate removal** — Enabled by default; uncheck to preserve every occurrence in source order.
- **Flexible output shape** — Choose **one symbol per line** (for a spreadsheet column) or **tab-separated single row** (for a spreadsheet row).
- **Live statistics** — A badge above the output shows the total ticker count and active sort direction.
- **One-click copy** — Pushes the entire output to your clipboard with a themed confirmation toast.
- **Sample loader** — The **Load sample** button drops in a real Hong Kong electronic technology screener export so you can test the parser instantly.
- **Zero dependencies** — Vanilla JavaScript only, no external runtime library.

### Ticker Extractor Quick Start

1. Start the Flask server with `python app.py` and open `http://localhost:5000` in any modern browser.
2. Scroll to the **📋 Ticker Symbol Extractor** card (directly beneath the Financial Shorthand Converter).
3. Paste your screener output into the **Input** textarea.
4. (Optional) Adjust the **Remove duplicates**, **Sort Z → A**, or **Tab-separated** checkboxes.
5. Click **Copy result**.
6. Paste into Excel or Google Sheets.

### Ticker Extractor Input Format

- Any plain-text block that contains ticker symbols on their own lines, immediately followed (in the next non-empty line) by a company name or the market marker `D`.
- Blank lines, header rows, numeric cells, and standalone short words are tolerated and ignored.
- Multi-column tab-separated rows (e.g., `Mkt cap\tPrice\tChg %\tVol`) are tolerated — only the standalone ticker lines are extracted.

**Example input (excerpt from a Hong Kong screener export):**

```text
Symbol
Mkt cap
Price
Chg %
…
2
2475
Luxshare Precision Industry Co., Ltd. Class H
D
446.21 B HKD	52.95 HKD	-1.12%	436.69 K	0.19	—	—	—	0.00%	Electronic technology
Strong buy
6
6951
Chaozhou Three-Circle (Group) Co., Ltd. Class H
D
272.95 B HKD	124.1 HKD	-2.90%	173.86 K	0.11	—	—	—	0.00%	Electronic technology
Strong buy

2476
Victory Giant Technology (HuiZhou) Co., Ltd. Class H
D
194.06 B HKD	195.1 HKD	-1.22%	546.33 K	0.16	32.72	5.96 HKD	—	0.00%	Electronic technology
Strong buy
```

### Ticker Extractor Output Format

- **Column mode (default):** One ticker per line, ready to paste into a single spreadsheet column.

  ```text
  679
  712
  759
  889
  1037
  1120
  1300
  1478
  1480
  1679
  1879
  1989
  2382
  2475
  2476
  3228
  6088
  6951
  8070
  8286
  8375
  ```

- **Tab-separated mode (checkbox):** All tickers joined by `\t`, ready to paste across a single spreadsheet row.

  ```text
  679	712	759	889	1037	1120	1300	1478	1480	1679	1879	1989	2382	2475	2476	3228	6088	6951	8070	8286	8375
  ```

> **Note:** Numeric symbols are sorted as strings, so `679` appears before `1037` and `2476` appears after `2475`. This matches the natural ordering of the source columns and is what most spreadsheet users expect for ticker lists.

### Detection Rules

The extractor applies the following rules to every line of the input:

1. **Pattern match** — The trimmed line must match one of:
   - An alphabetic ticker: starts with a letter A–Z, followed by 1–5 uppercase letters or digits (total length 2–6).
   - A numeric ticker: 3–6 digits (e.g., `679`, `2475`, `103700`).
2. **Noise filter** — The line must not be one of the reserved header abbreviations (`TTM`, `EPS`, `YOY`, `QOQ`, `ETF`, `IPO`, `CEO`, `CFO`, `ROE`, `ROA`, `ROI`, `NAV`, `ALL`, `NONE`, `NA`).
3. **Context confirmation** — The next non-empty line must either:
   - Contain at least one lowercase letter (i.e., look like a company name), **or**
   - Be exactly `D` (the market marker), **or**
   - Be followed by a line that is exactly `D`.
4. **Deduplication (optional)** — If **Remove duplicates** is enabled (default), only the first occurrence of each ticker is kept.

Only lines that satisfy all four rules are emitted.

### Ticker Extractor Options

| Option                         | Default | Effect                                                                                  |
| ------------------------------ | ------- | --------------------------------------------------------------------------------------- |
| **Remove duplicates**          | ✅ On   | Only the first occurrence of each ticker is kept. Uncheck to preserve every occurrence. |
| **Sort Z → A**                 | Off     | Reverses the alphabetical sort order.                                                   |
| **Tab-separated (single row)** | Off     | Joins the output with `\t` (single row) instead of `\n` (one per line).                 |

### Ticker Extractor How It Works

1. **Line splitting** — The input is split on `\r\n` or `\n`, and carriage returns are stripped.
2. **Trim & match** — Each line is trimmed and tested against the ticker regex.
3. **Noise rejection** — Reserved header words are skipped.
4. **Context lookahead** — The next two non-empty lines are inspected to confirm the current line is genuinely a ticker (and not a stray numeric cell or unrelated short word).
5. **Dedup collection** — Surviving tickers are pushed into the result array, optionally deduplicated using an internal `seen` map.
6. **Sort** — The result array is sorted lexicographically (A → Z by default; Z → A if the reverse checkbox is on).
7. **Join** — The sorted array is joined with `\n` (column mode) or `\t` (row mode) and written to the output textarea.
8. **Statistics** — The stats badge is updated with the total count and active sort direction.

### Ticker Extractor Examples

**Input fragment:**

```text
2475
Luxshare Precision Industry Co., Ltd. Class H
D
446.21 B HKD	…

6951
Chaozhou Three-Circle (Group) Co., Ltd. Class H
D
272.95 B HKD	…
```

**Output (A → Z, deduplicated, column mode):**

```text
2475
6951
```

**Same fragment, Z → A + tab-separated:**

```text
6951	2475
```

**Header-only input (no tickers present):**

```text
Symbol
Mkt cap
Price
Chg %
Vol
Rel vol
P/E
EPS dil
TTM
```

**Output:** _(empty)_ — the stats badge displays `no tickers detected`.

---

## Customization

You can easily modify the tools to suit your needs by editing the source in `app.py`:

- **Sample data (Financial Shorthand Converter)** — Change the `SAMPLE` array in the Financial Shorthand Converter IIFE.
- **Sample data (Ticker Symbol Extractor)** — Change the `SAMPLE` array inside the Ticker Symbol Extractor IIFE to load your own example.
- **Ticker detection rules** — Adjust the `TICKER_RE` regex and the `NOISE` object in the Ticker Symbol Extractor IIFE to add or remove accepted patterns and header words.
- **Ticker context confirmation** — Edit the `looksLikeTicker` condition to change how the extractor validates candidate lines (e.g., allow lines followed by a numeric ID instead of a company name).
- **Multipliers (Financial Shorthand Converter)** — Adjust the `MULT` object if you need different scaling factors.
- **Placeholder text** — Update the `placeholder` attributes on any textarea.
- **Styling** — All CSS is embedded in the `<style>` block inside `HTML_PAGE`; feel free to tweak colors, fonts, or layout.
- **Historical table layout** — The transposed Historical Data table (Period / Actual Date / Close Price, with a _Latest_ column first) is generated inside `openHistoryTab()` in `app.py`. Adjust the period-label logic in `getPeriodLabel()` or the row order in the HTML template to change its structure.
- **Default historical frequency** — The popup opens in **Quarterly** mode by default. To change the default, modify the `let freq = (initialFreq === "semiannual") ? "semiannual" : "quarterly";` line at the top of `openHistoryTab()`, or change the value passed in `processSearch()` (`const freq = "quarterly";`).
- **Quarterly / Semiannual grouping logic** — Both frequencies are handled inside `processPeriodData(timestamps, closes, freq)`. To add a new frequency (e.g., monthly), extend this function and add a corresponding button in the popup header.
- **Package tab delay** — Adjust the `350` millisecond timeout inside `processSearch()` to change the delay between opening bundled Package tabs.
- **Proxy timeout** — The `/proxy` route uses a 15-second timeout to Yahoo Finance; adjust as needed for slower networks.
- **Refresh shortcut interception** — The `keydown` listener in the main page script uses a capture-phase handler to block `Ctrl+R`, `Ctrl+Shift+R`, `F5`, `Ctrl+F5`, and `Shift+F5`. To modify which combinations are blocked, edit the `isRefreshCombo` condition inside that listener.

No build step is required — the Flask server hosts the single-file frontend.

---

## Browser Support

The tool works in all modern browsers that support:

- ES6+ (arrow functions, `const`/`let`, template literals are not used extensively, but BigInt is required).
- BigInt (Chrome 67+, Firefox 68+, Safari 14+, Edge 79+).
- Async clipboard API (or falls back to `document.execCommand('copy')`).
- `fetch` API for the local Historical Data proxy.

For older browsers, the fallback copy method may work, but BigInt support is essential.

---

## Troubleshooting

> **Note:** The main application page intercepts refresh shortcuts (`Ctrl+R`, `Ctrl+Shift+R`, `F5`, `Ctrl+F5`, `Shift+F5`). If you need to force a refresh to clear a cache, use your browser's menu (e.g., View → Reload) or open the page in a new incognito window. Inside the Historical Data popup, refresh shortcuts are **not** intercepted.

| Issue                                          | Possible Cause                               | Solution                                                                                                                                                                      |
| ---------------------------------------------- | -------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Copy button does nothing                       | Browser blocks clipboard access              | Use a secure context (HTTPS or localhost) or copy manually from the output textarea.                                                                                          |
| Values not pasting horizontally                | Spreadsheet settings                         | Ensure you paste into a single cell and that the tab character is preserved. Some apps may convert tabs to spaces.                                                            |
| Wrong number of columns (Shorthand Converter)  | Input contains unrecognised lines            | Check the stats indicator (e.g., "8 converted · 8 skipped"). Unrecognised lines are silently ignored.                                                                         |
| Reverse order not working                      | Checkbox state                               | Make sure the checkbox is checked if you need reversed output.                                                                                                                |
| Large numbers lose precision                   | JavaScript number limitations                | The tool uses BigInt, so precision is maintained. If you see incorrect values, ensure you are using a modern browser.                                                         |
| `Enter` does not trigger search                | Focused inside a `<textarea>`                | Textareas (Financial Shorthand Converter, Text Case Converter, Ticker Symbol Extractor) intentionally keep native newline behaviour. Move focus to the Exchange/Ticker field. |
| Package mode launched too few tabs             | Fixed bundle of 6 tabs is expected           | This is by design. Switch to StockAnalysis or TradingView mode if you prefer granular checklist control.                                                                      |
| Historical Data tab shows error                | Flask `/proxy` unreachable or ticker invalid | Ensure `python app.py` is running and the page is loaded from `http://localhost:5000`. Verify the ticker and exchange code.                                                   |
| Historical Data favicon still shows old emoji  | Browser favicon cache                        | Open the popup in an incognito window, or use the browser menu to force a full reload of the main page.                                                                       |
| Historical table dates not aligned with prices | Horizontal scrolling is expected             | The table is intentionally transposed. The leftmost label column (`Period` / `Actual Date` / `Close Price`) stays sticky on the left while you scroll to compare periods.     |
| Quarterly / Semiannual toggle not visible      | Browser cached the old popup template        | Open the main page in an incognito window or use the browser menu to reload the page, then reopen the popup. The toggle lives inside the blue popup header.                   |
| Semiannual mode shows fewer rows than expected | Only June & December are kept                | This is by design — Semiannual mode keeps exactly the two half-year ends per year (June and December).                                                                        |
| Latest column style looks different            | Browser cache                                | Open the main page in an incognito window or use the browser menu to reload the page. The Latest column is styled identically to all other columns in the current release.    |
| Ticker Extractor returns 0 tickers             | Input format doesn't match detection rules   | Click **Load sample** to compare shapes. Ensure ticker lines are followed by a company name or the `D` marker. Adjust `TICKER_RE` if your market uses a different format.     |
| Ticker Extractor includes false positives      | Header word not in the noise list            | Add the word to the `NOISE` object inside the Ticker Symbol Extractor IIFE.                                                                                                   |
| Ticker Extractor misses some symbols           | Symbol format not matched by the regex       | Extend `TICKER_RE` to include the missing format (e.g., allow a leading digit for markets that use alphanumeric codes).                                                       |
| Ticker Extractor output order looks odd        | Numeric sorting is lexicographic             | By design, tickers are sorted as strings. This matches typical spreadsheet column ordering for numeric codes.                                                                 |

---

## Unified Architecture & Technologies Used

- **Flask (Python) Backend:** `app.py` serves the single-file frontend via `render_template_string` and exposes a `/proxy` endpoint that forwards requests to Yahoo Finance for historical price data. This is the only server-side component.
- **HTML5 Elements:** Structured content layout separating input contexts from interactive control modules.
- **CSS3 Variables & Responsive Design:** Centralized color variables handle real-time theme swapping, while a mobile-first layout engine guarantees responsive adaptations — including the transposed, horizontally scrollable Historical Data table (Period / Actual Date / Close Price rows with a leading _Latest_ column).
- **Vanilla JavaScript (ES6+):** Manages local caching layers, handles typography transformations, monitors tracking variables, maps data parameters into targeted financial URL strings, renders the local Historical Data tab (including the period-label derivation logic, the in-popup Quarterly / Semiannual toggle, and the cached daily-close dataset), and runs the Ticker Symbol Extractor (regex detection, contextual confirmation, dedup, sort, and format). The main page also runs a capture-phase `keydown` listener to intercept refresh shortcuts.
- **SweetAlert2 Library Integration:** Leveraged for modern, non-blocking toast popups and validation dialogs that automatically match the selected system theme.
- **BigInt Arithmetic:** Used by the Financial Shorthand Converter for exact financial suffix conversion without floating-point precision loss.
- **Regex-Based Parsing:** The Ticker Symbol Extractor uses a compact regex (`^([A-Z][A-Z0-9]{1,5}|\d{3,6})$`) to accept both alphabetic and numeric ticker formats in a single pass.
- **Clipboard API Integration:** Enables one-click copy operations across the suite, with fallback support where needed.
- **`requests` (Python):** Used by the Flask `/proxy` route to make outbound HTTP calls to Yahoo Finance with a desktop User-Agent header.

---

## License

This suite is provided as-is for personal and commercial use. No warranty is expressed or implied. You are free to modify and distribute it.
