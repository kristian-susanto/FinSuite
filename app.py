from flask import Flask, request, jsonify, render_template_string
import requests

app = Flask(__name__)

HTML_PAGE = r'''<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>FinSuite</title>
    <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>💼</text></svg>" />
    <script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>
    <style>
      :root {
        --bg-body: #f1f5f9; --bg-card: #ffffff; --text-main: #1e293b;
        --text-secondary: #64748b; --border: #e2e8f0; --primary: #2563eb;
        --primary-hover: #1d4ed8; --success: #10b981; --danger: #ef4444;
        --counter-color: #6c5ce7; --input-bg: #ffffff; --output-bg: #f8fafc;
        --radio-bg: #f8f9fa; --link-bg: #f8f9fa; --link-text: #34495e;
      }
      [data-theme="dark"] {
        --bg-body: #0f172a; --bg-card: #1e293b; --text-main: #f1f5f9;
        --text-secondary: #94a3b8; --border: #334155; --primary: #3b82f6;
        --primary-hover: #2563eb; --counter-color: #a29bfe; --input-bg: #334155;
        --output-bg: #0f172a; --radio-bg: #334155; --link-bg: #334155; --link-text: #f1f5f9;
      }
      * { margin: 0; padding: 0; box-sizing: border-box;
        font-family: "Inter", system-ui, -apple-system, sans-serif;
        transition: background-color 0.3s ease, color 0.3s ease, border-color 0.3s ease; }
      body { background-color: var(--bg-body); color: var(--text-main); min-height: 100vh; padding: 30px 15px 60px; }
      header { max-width: 1200px; margin: 0 auto 2rem auto; display: flex;
        justify-content: space-between; align-items: center; gap: 12px;
        flex-wrap: wrap; border-bottom: 2px solid var(--border); padding-bottom: 1rem; }
      header h1 { font-size: clamp(1.4rem, 3.2vw, 1.8rem); font-weight: 800; letter-spacing: -0.5px; }
      .theme-toggle { background-color: var(--bg-card); color: var(--text-main);
        border: 1px solid var(--border); padding: 8px 16px; border-radius: 20px;
        font-size: 0.9rem; font-weight: 600; cursor: pointer; display: flex;
        align-items: center; gap: 6px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); }
      .theme-toggle:hover { opacity: 0.9; }
      .dashboard-grid { max-width: 1200px; margin: 0 auto; display: grid;
        grid-template-columns: repeat(12, 1fr); gap: 20px; }
      .card { background: var(--bg-card); padding: 25px; border-radius: 16px;
        box-shadow: 0 10px 25px -5px rgba(0,0,0,0.1); border: 1px solid var(--border); }
      .card h2 { font-size: 1.3rem; font-weight: 700; margin-bottom: 1.2rem;
        border-bottom: 1px solid var(--border); padding-bottom: 0.5rem; }
      .stock-card { grid-column: span 7; }
      .side-panel { grid-column: span 5; display: flex; flex-direction: column; gap: 20px; }
      .converter-card { grid-column: span 12; }
      .ticker-card { grid-column: span 12; }
      @media (max-width: 992px) { .stock-card, .side-panel { grid-column: span 12; } }
      .input-group { margin-bottom: 15px; }
      label { display: block; margin-bottom: 6px; font-weight: 600; font-size: 14px; color: var(--text-secondary); }
      input[type="text"] { width: 100%; padding: 12px; border: 2px solid var(--border);
        background-color: var(--input-bg); color: var(--text-main); border-radius: 8px; font-size: 15px; }
      input[type="text"]:focus, textarea:focus { border-color: var(--primary); outline: none; }
      .checkbox-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(130px, 1fr));
        gap: 8px; background: var(--radio-bg); padding: 12px; border: 1px solid var(--border);
        border-radius: 8px; max-height: 150px; overflow-y: auto; }
      .checkbox-grid.is-disabled { opacity: 0.45; pointer-events: none; user-select: none; }
      .check-option, .radio-option { font-size: 13px; color: var(--text-main);
        display: flex; align-items: center; cursor: pointer; }
      .check-option input, .radio-option input { margin-right: 8px; cursor: pointer; }
      .radio-group { display: flex; gap: 15px; background: var(--radio-bg);
        padding: 10px; border-radius: 8px; border: 1px solid var(--border); flex-wrap: wrap; }
      .source-note { display: block; margin-top: 8px; font-size: 11.5px;
        line-height: 1.55; color: var(--text-secondary); text-align: left;
        background: var(--radio-bg); border: 1px dashed var(--border);
        border-radius: 8px; padding: 8px 10px; }
      button.btn-action { padding: 12px 20px; font-size: 14px; font-weight: 600;
        border: none; border-radius: 8px; cursor: pointer; display: inline-flex;
        align-items: center; justify-content: center; gap: 5px; }
      .btn-primary { background-color: var(--primary); color: #ffffff; }
      .btn-primary:hover { background-color: var(--primary-hover); }
      .btn-danger { background-color: var(--danger); color: #ffffff; }
      .btn-danger:hover { opacity: 0.9; }
      .btn-success { background-color: var(--success); color: #ffffff; }
      .btn-success:hover { opacity: 0.9; }
      .btn-ghost { background-color: var(--bg-card); color: var(--text-main); border: 1px solid var(--border); }
      .btn-ghost:hover { background-color: var(--radio-bg); }
      #linkContainer { margin-top: 15px; padding-top: 15px; border-top: 1px solid var(--border); display: none; }
      .link-item { display: block; background: var(--link-bg); margin-bottom: 6px;
        padding: 8px 12px; text-decoration: none; color: var(--link-text);
        border-radius: 6px; font-size: 13px; border-left: 4px solid var(--primary); }
      .link-item:hover { background: var(--primary); color: #ffffff; }
      .hint { font-size: 11px; color: var(--text-secondary); text-align: center; margin-top: 10px; }
      .counter-display { font-size: 3.5rem; font-weight: 800; color: var(--counter-color);
        margin: 10px 0; text-align: center; transition: transform 0.1s ease; }
      .counter-buttons { display: flex; gap: 10px; }
      .case-card textarea { width: 100%; height: 120px; padding: 12px;
        border: 2px solid var(--border); border-radius: 8px; font-size: 14px;
        background: var(--input-bg); color: var(--text-main); margin-bottom: 10px;
        resize: vertical; outline: none; }
      .text-controls { display: grid; grid-template-columns: repeat(2, 1fr);
        gap: 8px; margin-bottom: 12px; }
      .text-controls button { padding: 10px 6px; border: 1px solid var(--border);
        border-radius: 6px; background: var(--radio-bg); color: var(--text-main);
        cursor: pointer; font-size: 12px; font-weight: 600; }
      .text-controls button:hover { background: var(--primary); color: #ffffff; }
      .text-actions { display: flex; gap: 10px; }
      .legend { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 18px; }
      .chip { font-size: 12.5px; color: var(--primary); background: var(--radio-bg);
        border: 1px solid var(--border); padding: 5px 10px; border-radius: 999px;
        font-variant-numeric: tabular-nums; white-space: nowrap; }
      .chip b { color: var(--primary); font-weight: 700; }
      .converter-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 18px; }
      @media (max-width: 820px) { .converter-grid { grid-template-columns: 1fr; } }
      .panel { display: flex; flex-direction: column; min-width: 0; }
      .panel-head { display: flex; justify-content: space-between; align-items: baseline; gap: 10px; margin-bottom: 8px; }
      .panel-head label { font-weight: 600; font-size: 14px; color: var(--text-secondary); margin-bottom: 0; }
      .panel-meta { font-size: 12px; color: var(--text-secondary); text-align: right; }
      .converter-card textarea, .ticker-card textarea { width: 100%; min-height: min(40vh, 300px); padding: 14px 16px;
        border: 2px solid var(--border); border-radius: 12px; background: var(--input-bg);
        color: var(--text-main); font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
        font-size: 14.5px; line-height: 1.7; resize: vertical; outline: none; }
      #output, #tickerOutput { background: var(--output-bg); }
      .options { margin-top: 14px; display: flex; align-items: center; gap: 8px;
        font-size: 14px; color: var(--text-secondary); cursor: pointer; user-select: none; }
      .options input[type="checkbox"] { width: 17px; height: 17px; accent-color: var(--primary); cursor: pointer; }
      .actions { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 18px; }
      .foot { margin: 18px 2px 0; font-size: 12.5px; color: var(--text-secondary); line-height: 1.6; }
      .ticker-options { display: flex; flex-wrap: wrap; gap: 8px 20px; margin-top: 14px; }
      .ticker-options .options { margin-top: 0; }
    </style>
  </head>
  <body>
    <header>
      <h1>FinSuite</h1>
      <button class="theme-toggle" id="themeMasterBtn" title="Switch Global Interface Theme">
        <span id="themeMasterText">🌙 Dark Mode</span>
      </button>
    </header>

    <main class="dashboard-grid">
      <section class="card stock-card">
        <h2>📊 Stock Multi-Tab Researcher</h2>
        <div class="input-group">
          <label for="exchange_name">Exchange Name</label>
          <input type="text" id="exchange_name" list="exchange_list" placeholder="Search Country or Exchange..." />
          <datalist id="exchange_list"></datalist>
        </div>
        <div class="input-group">
          <label for="ticker_symbol">Ticker Symbol</label>
          <input type="text" id="ticker_symbol" placeholder="Example: 0700" />
        </div>
        <div class="input-group">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
            <label style="margin-bottom: 0">Select Data Points</label>
            <div style="font-size: 11px; font-weight: bold">
              <span onclick="toggleAllCheckboxes(true)" style="cursor: pointer; color: var(--primary)">All</span>
              |
              <span onclick="toggleAllCheckboxes(false)" style="cursor: pointer; color: var(--primary)">None</span>
            </div>
          </div>
          <div class="checkbox-grid" id="checkboxGrid">
            <label class="check-option"><input type="checkbox" value="news" /> Latest News</label>
            <label class="check-option"><input type="checkbox" value="overview" /> Overview</label>
            <label class="check-option"><input type="checkbox" value="history" /> Historical Data</label>
            <label class="check-option"><input type="checkbox" value="income" /> Income Statement</label>
            <label class="check-option"><input type="checkbox" value="balance" /> Balance Sheet</label>
            <label class="check-option"><input type="checkbox" value="cash" /> Cash Flow</label>
            <label class="check-option"><input type="checkbox" value="stats" /> Ratios</label>
            <label class="check-option"><input type="checkbox" value="revenue" /> Revenue</label>
            <label class="check-option"><input type="checkbox" value="dividends" /> Dividends</label>
          </div>
        </div>
        <div class="input-group">
          <label>Data Source Support</label>
          <div class="radio-group">
            <label class="radio-option"><input type="radio" name="source" value="quarterly_package" checked /> Quarterly Package</label>
            <label class="radio-option"><input type="radio" name="source" value="semester_package" /> Semester Package</label>
            <label class="radio-option"><input type="radio" name="source" value="tradingview" /> TradingView</label>
            <label class="radio-option"><input type="radio" name="source" value="stockanalysis" /> StockAnalysis</label>
          </div>
          <p class="source-note">
            <b>Package mode</b> opens a fixed bundle of <b>6 tabs</b>:
            <br />• 🏢 Overview — StockAnalysis &amp; TradingView
            <br />• ⏳ Historical Data — Python (yfinance)
            <br />• 📑 Income Statement — TradingView
            <br />• ⚖️ Balance Sheet — TradingView
            <br />• 📊 Ratios — TradingView
          </p>
        </div>

        <div style="display: flex; gap: 10px; margin-top: 15px">
          <button class="btn-action btn-primary" style="flex: 2" onclick="processSearch()">Open All Selected Tabs</button>
          <button class="btn-action btn-danger" style="flex: 1" onclick="resetStockForm()">Reset</button>
        </div>
        <div id="linkContainer"><label>Manual Generated Links:</label><div id="linkList"></div></div>
        <p id="hintText" class="hint" style="display: none">If tabs do not open automatically, please <b>Allow Pop-ups</b>.</p>
      </section>

      <div class="side-panel">
        <section class="card">
          <h2>🖱️ Click Counter</h2>
          <div class="counter-display" id="counter-value">0</div>
          <div class="counter-buttons">
            <button class="btn-action btn-primary" id="click-btn" style="flex: 2">CLICK HERE</button>
            <button class="btn-action btn-ghost" id="decrement-btn" style="flex: 1; font-size: 20px; font-weight: 800" title="Decrement by 1">−</button>
            <button class="btn-action btn-danger" id="reset-counter-btn" style="flex: 1">Reset</button>
          </div>
        </section>
        <section class="card case-card">
          <h2>🔤 Text Case Converter</h2>
          <textarea id="textInput" placeholder="Type or paste alphanumeric string data records here..."></textarea>
          <div class="text-controls">
            <button onclick="transformText('upper')">UPPERCASE</button>
            <button onclick="transformText('lower')">lowercase</button>
            <button onclick="transformText('capitalize')">Capitalize Word</button>
            <button onclick="transformText('sentence')">Sentence case</button>
            <!-- REMOVED: Toggle Case button -->
          </div>
          <div class="text-actions">
            <button class="btn-action btn-success" style="flex: 2" onclick="copyText()">Copy to Clipboard</button>
            <button class="btn-action btn-danger" style="flex: 1" onclick="clearText()">Clear</button>
          </div>
        </section>
      </div>

      <section class="card converter-card">
        <h2>🔢 Financial Shorthand Converter</h2>
        <div class="legend">
          <span class="chip"><b>K</b> ×1,000</span>
          <span class="chip"><b>M</b> ×1,000,000</span>
          <span class="chip"><b>B</b> ×1,000,000,000</span>
          <span class="chip"><b>T</b> ×1,000,000,000,000</span>
        </div>
        <div class="converter-grid">
          <div class="panel">
            <div class="panel-head"><label for="input">Input</label><span class="panel-meta">one value per line</span></div>
            <textarea id="input" spellcheck="false" placeholder="9.26 T&#10;−2.05%&#10;9.70 T&#10;+4.25%"></textarea>
          </div>
          <div class="panel">
            <div class="panel-head"><label for="output">Output</label><span class="panel-meta" id="stats"></span></div>
            <textarea id="output" spellcheck="false" readonly wrap="off" placeholder="Converted values will appear here…"></textarea>
          </div>
        </div>
        <label class="options">
          <input type="checkbox" id="reverseOrder" checked />
          Reverse order (Right-to-Left paste) — Adjust according to your sheet
        </label>
        <div class="actions">
          <button id="copyBtn" class="btn-action btn-primary" type="button">Copy result</button>
          <button id="sampleBtn" class="btn-action btn-ghost" type="button">Load sample</button>
          <button id="clearBtn" class="btn-action btn-ghost" type="button">Clear</button>
        </div>
        <p class="foot">Output values are separated by tabs. Paste into a spreadsheet row. Commas as thousand separators, no decimal point. Percentage lines ignored.</p>
      </section>

      <section class="card ticker-card">
        <h2>📋 Ticker Symbol Extractor</h2>
        <div class="converter-grid">
          <div class="panel">
            <div class="panel-head"><label for="tickerInput">Input — paste screener data</label><span class="panel-meta">auto-detects tickers</span></div>
            <textarea id="tickerInput" spellcheck="false" placeholder="Paste rows copied from your screener here (StockAnalysis, TradingView, etc.)…"></textarea>
          </div>
          <div class="panel">
            <div class="panel-head"><label for="tickerOutput">Output — sorted tickers</label><span class="panel-meta" id="tickerStats"></span></div>
            <textarea id="tickerOutput" spellcheck="false" readonly wrap="off" placeholder="Tickers A → Z will appear here…"></textarea>
          </div>
        </div>
        <div class="ticker-options">
          <label class="options"><input type="checkbox" id="tickerDedupe" checked /> Remove duplicates</label>
          <label class="options"><input type="checkbox" id="tickerDesc" /> Sort Z → A</label>
          <label class="options"><input type="checkbox" id="tickerTabbed" /> Tab-separated (single row)</label>
        </div>
        <div class="actions">
          <button id="tickerCopyBtn" class="btn-action btn-primary" type="button">Copy result</button>
          <button id="tickerSampleBtn" class="btn-action btn-ghost" type="button">Load sample</button>
          <button id="tickerClearBtn" class="btn-action btn-ghost" type="button">Clear</button>
        </div>
        <p class="foot">Paste screener output containing standalone ticker lines. The extractor detects standalone uppercase symbols and numeric ticker codes (2–6 digits), sorts them in strict A → Z / 0 → 9 order, and formats them for clean spreadsheet pasting. Use <b>one per line</b> for a column, or <b>tab-separated</b> for a single row.</p>
      </section>
    </main>

    <script>
      const exchangeInput = document.getElementById("exchange_name");
      const tickerInput = document.getElementById("ticker_symbol");
      const radioButtons = document.querySelectorAll('input[name="source"]');
      const checkboxGrid = document.getElementById("checkboxGrid");
      const textInput = document.getElementById("textInput");
      const themeMasterBtn = document.getElementById("themeMasterBtn");
      const themeMasterText = document.getElementById("themeMasterText");
      const counterDisplay = document.getElementById("counter-value");
      const clickBtn = document.getElementById("click-btn");
      const resetCounterBtn = document.getElementById("reset-counter-btn");
      const decrementBtn = document.getElementById("decrement-btn");
      let count = 0;

      const exchanges = [
        // A
        { name: "Abu Dhabi Securities Exchange — United Arab Emirates", code: "ADX" },
        { name: "Aquis Exchange — United Kingdom", code: "AQUIS" },
        { name: "Athens Stock Exchange — Greece", code: "ATHEX" },
        { name: "Australian Securities Exchange — Australia", code: "ASX" },
        // B
        { name: "B3 (Bovespa) — Brazil", code: "BMFBOVESPA" },
        { name: "Bahrain Bourse — Bahrain", code: "BAHRAIN" },
        { name: "Belgrade Stock Exchange — Serbia", code: "BELEX" },
        { name: "Bolsa de Comercio de Buenos Aires — Argentina", code: "BCBA" },
        { name: "Bolsa de Comercio de Santiago — Chile", code: "BCS" },
        { name: "Bolsa de Madrid — Spain", code: "BME" },
        { name: "Bolsa de Valores de Caracas — Venezuela", code: "BVCV" },
        { name: "Bolsa de Valores de Colombia — Colombia", code: "BVC" },
        { name: "Bolsa de Valores de Lima — Peru", code: "BVL" },
        { name: "Bolsa Institucional de Valores — Mexico", code: "BIVA" },
        { name: "Bolsa Mexicana de Valores — Mexico", code: "BMV" },
        { name: "Bombay Stock Exchange — India", code: "BSE" },
        { name: "Borsa Istanbul — Turkey", code: "BIST" },
        { name: "Borsa Italiana — Italy", code: "MIL" },
        { name: "Boursa Kuwait — Kuwait", code: "KSE" },
        { name: "Bourse de Tunis — Tunisia", code: "BVMT" },
        { name: "Bratislava Stock Exchange — Slovakia", code: "BSSE" },
        { name: "Bucharest Stock Exchange — Romania", code: "BVB" },
        { name: "Budapest Stock Exchange — Hungary", code: "BET" },
        { name: "Buenos Aires Stock Exchange (BYMA) — Argentina", code: "BYMA" },
        { name: "Bulgarian Stock Exchange — Bulgaria", code: "BSESOF" },
        { name: "Bursa Malaysia — Malaysia", code: "MYX" },
        { name: "BX Swiss — Switzerland", code: "BX" },
        // C
        { name: "Canadian Securities Exchange — Canada", code: "CSE" },
        { name: "Casablanca Stock Exchange — Morocco", code: "CSEMA" },
        { name: "Cboe Canada (NEO) — Canada", code: "NEO" },
        { name: "China Financial Futures Exchange — Mainland China", code: "CFFEX" },
        { name: "Colombo Stock Exchange — Sri Lanka", code: "CSELK" },
        { name: "Cyprus Stock Exchange — Cyprus", code: "CSECY" },
        // D
        { name: "Dhaka Stock Exchange — Bangladesh", code: "DSEBD" },
        { name: "Dubai Financial Market — United Arab Emirates", code: "DFM" },
        { name: "Düsseldorf Stock Exchange — Germany", code: "DUS" },
        // E
        { name: "Egyptian Exchange — Egypt", code: "EGX" },
        { name: "Euronext Amsterdam — Netherlands", code: "EURONEXTAMS" },
        { name: "Euronext Brussels — Belgium", code: "EURONEXTBRU" },
        { name: "Euronext Dublin — Ireland", code: "EURONEXTDUB" },
        { name: "Euronext Lisbon — Portugal", code: "EURONEXTLIS" },
        { name: "Euronext Oslo — Norway", code: "EURONEXTOSE" },
        { name: "Euronext Paris — France", code: "EURONEXTPAR" },
        { name: "EuroTLX — Italy", code: "EUROTLX" },
        // F
        { name: "Frankfurt Stock Exchange — Germany", code: "FWB" },
        { name: "Fukuoka Stock Exchange — Japan", code: "FSE" },
        // H
        { name: "Hamburg Stock Exchange — Germany", code: "HAM" },
        { name: "Hanoi Stock Exchange — Vietnam", code: "HNX" },
        { name: "Hanover Stock Exchange — Germany", code: "HAN" },
        { name: "Ho Chi Minh Stock Exchange — Vietnam", code: "HOSE" },
        { name: "Hong Kong Stock Exchange — Hong Kong", code: "HKEX" },
        // I
        { name: "Indonesia Stock Exchange — Indonesia", code: "IDX" },
        // J
        { name: "Johannesburg Stock Exchange — South Africa", code: "JSE" },
        // K
        { name: "Korea Exchange — South Korea", code: "KRX" },
        // L
        { name: "Lang & Schwarz — Germany", code: "LS" },
        { name: "Ljubljana Stock Exchange — Slovenia", code: "LJSE" },
        { name: "London Stock Exchange — United Kingdom", code: "LSE" },
        { name: "LS Exchange — Germany", code: "LSX" },
        { name: "LSE International — United Kingdom", code: "LSIN" },
        { name: "Luxembourg Stock Exchange — Luxembourg", code: "LUXSE" },
        // M
        { name: "Moscow Exchange — Russia", code: "RUS" },
        { name: "Munich Stock Exchange — Germany", code: "MUN" },
        // N
        { name: "Nagoya Stock Exchange — Japan", code: "NAG" },
        { name: "Nairobi Securities Exchange — Kenya", code: "NSEKE" },
        { name: "Nasdaq — United States", code: "NASDAQ" },
        { name: "Nasdaq Copenhagen — Denmark", code: "OMXCOP" },
        { name: "Nasdaq Dubai — United Arab Emirates", code: "NASDAQDUBAI" },
        { name: "Nasdaq Helsinki — Finland", code: "OMXHEX" },
        { name: "Nasdaq Iceland — Iceland", code: "OMXICE" },
        { name: "Nasdaq Riga — Latvia", code: "OMXRSE" },
        { name: "Nasdaq Stockholm — Sweden", code: "OMXSTO" },
        { name: "Nasdaq Tallinn — Estonia", code: "OMXTSE" },
        { name: "Nasdaq Vilnius — Lithuania", code: "OMXVSE" },
        { name: "National Stock Exchange of India — India", code: "NSE" },
        { name: "New York Stock Exchange — United States", code: "NYSE" },
        { name: "New York Stock Exchange Arca — United States", code: "NYSEARCA" },
        { name: "New Zealand Exchange — New Zealand", code: "NZX" },
        { name: "NewConnect — Poland", code: "NEWCONNECT" },
        { name: "Nigerian Exchange — Nigeria", code: "NSENG" },
        { name: "Nordic Growth Market — Sweden", code: "NGM" },
        // O
        { name: "OTC Markets — United States", code: "OTC" },
        // P
        { name: "Pakistan Stock Exchange — Pakistan", code: "PSX" },
        { name: "Philippine Stock Exchange — Philippines", code: "PSE" },
        { name: "Prague Stock Exchange — Czech Republic", code: "PSECZ" },
        // Q
        { name: "Qatar Stock Exchange — Qatar", code: "QSE" },
        // S
        { name: "Sapporo Securities Exchange — Japan", code: "SAPSE" },
        { name: "Saudi Stock Exchange (Tadawul) — Saudi Arabia", code: "TADAWUL" },
        { name: "Shanghai Futures Exchange — Mainland China", code: "SHFE" },
        { name: "Shanghai Stock Exchange — Mainland China", code: "SSE" },
        { name: "Shenzhen Stock Exchange — Mainland China", code: "SZSE" },
        { name: "Singapore Exchange — Singapore", code: "SGX" },
        { name: "SIX Swiss Exchange — Switzerland", code: "SIX" },
        { name: "Stock Exchange of Thailand — Thailand", code: "SET" },
        { name: "Stuttgart Stock Exchange — Germany", code: "SWB" },
        // T
        { name: "Taipei Exchange — Taiwan", code: "TPEX" },
        { name: "Taiwan Stock Exchange — Taiwan", code: "TWSE" },
        { name: "Tel Aviv Stock Exchange — Israel", code: "TASE" },
        { name: "Tokyo Stock Exchange — Japan", code: "TSE" },
        { name: "Toronto Stock Exchange — Canada", code: "TSX" },
        { name: "Tradegate — Germany", code: "TRADEGATE" },
        { name: "TSX Venture Exchange — Canada", code: "TSXV" },
        // U
        { name: "UPCoM — Vietnam", code: "UPCOM" },
        // V
        { name: "Vienna Stock Exchange — Austria", code: "VIE" },
        // W
        { name: "Warsaw Stock Exchange — Poland", code: "GPW" },
        // X
        { name: "Xetra — Germany", code: "XETR" },
        // Z
        { name: "Zagreb Stock Exchange — Croatia", code: "ZSE" },
        { name: "Zhengzhou Commodity Exchange — Mainland China", code: "ZCE" },
      ];

      const YAHOO_SUFFIX_MAP = {
        // A
        ADX: ".AE",
        AQUIS: ".L",
        ASX: ".AX",
        ATHEX: ".AT",
        // B
        BAHRAIN: ".BH",
        BCBA: ".BA",
        BCS: ".SN",
        BELEX: ".BE",
        BET: ".BD",
        BIST: ".IS",
        BIVA: ".MX",
        BME: ".MC",
        BMFBOVESPA: ".SA",
        BMV: ".MX",
        BSE: ".BO",
        BSESOF: ".SO",
        BSSE: ".BS",
        BVC: ".CL",
        BVCV: ".CC",
        BVL: ".LM",
        BVB: ".RO",
        BYMA: ".BA",
        // C
        CSECY: ".CY",
        CSE: ".CN",
        CSEMA: ".MA",
        CSELK: ".CM",
        // D
        DFM: ".AE",
        DUS: ".DU",
        DSEBD: ".BD",
        // E
        EGX: ".CA",
        EURONEXTAMS: ".AS",
        EURONEXTBRU: ".BR",
        EURONEXTOSE: ".OL",
        EURONEXTPAR: ".PA",
        EURONEXTDUB: ".IR",
        EURONEXTLIS: ".LS",
        EUROTLX: ".MI",
        // F
        FSE: ".F",
        FWB: ".F",
        // G
        GPW: ".WA",
        // H
        HAM: ".HM",
        HAN: ".HA",
        HNX: ".VN",
        HKEX: ".HK",
        HOSE: ".VN",
        // I
        IDX: ".JK",
        // J
        JSE: ".JO",
        // K
        KRX: ".KS",
        KSE: ".KW",
        // L
        LJSE: ".LJ",
        LSE: ".L",
        LS: ".LS",
        LSIN: ".L",
        LSX: ".LS",
        LUXSE: ".LU",
        // M
        MIL: ".MI",
        MUN: ".MU",
        MYX: ".KL",
        // N
        NAG: ".N",
        NASDAQ: "",
        NASDAQDUBAI: ".AE",
        NEWCONNECT: ".WA",
        NEO: ".NE",
        NGM: ".ST",
        NSE: ".NS",
        NSEKE: ".NR",
        NSENG: ".LG",
        NZX: ".NZ",
        // O
        OMXCOP: ".CO",
        OMXHEX: ".HE",
        OMXICE: ".IC",
        OMXRSE: ".RG",
        OMXSTO: ".ST",
        OMXTSE: ".TL",
        OMXVSE: ".VS",
        OTC: "",
        // P
        PSECZ: ".PR",
        PSE: ".PS",
        PSX: ".KA",
        // Q
        QSE: ".QA",
        // R
        RUS: ".ME",
        // S
        SAPSE: ".S",
        SET: ".BK",
        SGX: ".SI",
        SIX: ".SW",
        SSE: ".SS",
        SWB: ".SG",
        SZSE: ".SZ",
        // T
        TADAWUL: ".SR",
        TASE: ".TA",
        TRADEGATE: ".TG",
        TSX: ".TO",
        TSXV: ".V",
        TPEX: ".TWO",
        TSE: ".T",
        TWSE: ".TW",
        // U
        UPCOM: ".VN",
        // V
        VIE: ".VI",
        // X
        XETR: ".DE",
        // Z
        ZSE: ".ZG",
      };

      window.addEventListener("DOMContentLoaded", () => {
        const list = document.getElementById("exchange_list");
        exchanges.forEach((ex) => {
          const option = document.createElement("option");
          option.value = ex.name;
          option.setAttribute("data-code", ex.code);
          list.appendChild(option);
        });
        updateSourceUI();
      });

      function setTheme(theme) {
        document.documentElement.setAttribute("data-theme", theme);
        localStorage.setItem("theme", theme);
        themeMasterText.innerText = theme === "dark" ? "☀️ Light Mode" : "🌙 Dark Mode";
      }
      themeMasterBtn.addEventListener("click", () => {
        const currentTheme = document.documentElement.getAttribute("data-theme");
        setTheme(currentTheme === "dark" ? "light" : "dark");
      });
      setTheme(localStorage.getItem("theme") || "light");

      function getToastConfig(icon, title) {
        const isDark = document.documentElement.getAttribute("data-theme") === "dark";
        return { toast: true, position: "top", showConfirmButton: false, timer: 3000,
          timerProgressBar: true, background: isDark ? "#1e293b" : "#ffffff",
          color: isDark ? "#f1f5f9" : "#1e293b", icon: icon, title: title };
      }

      const SA_EXCHANGE_MAP = {
        // A
        ADX: "ADX",
        AQUIS: "AQU",
        ASX: "ASX",
        ATHEX: "ATH",
        // B
        BAHRAIN: "BAX",
        BCBA: "BCBA",
        BELEX: "BELEX",
        BET: "BUD",
        BIST: "IST",
        BME: "BME",
        BMFBOVESPA: "BVMF",
        BMV: "BMV",
        BSE: "BOM",
        BSESOF: "BUL",
        BSSE: "BSSE",
        BVC: "BVC",
        BVCV: "CCSE",
        BVL: "BVL",
        BYMA: "BCBA",
        BVB: "BVB",
        // C
        CSE: "CSE",
        CSECY: "CYS",
        CSEMA: "CBSE",
        CSELK: "COSE",
        // D
        DFM: "DFM",
        DSEBD: "DSE",
        DUS: "DUSE",
        // E
        EGX: "EGX",
        EURONEXTAMS: "AMS",
        EURONEXTBRU: "EBR",
        EURONEXTDUB: "ISE",
        EURONEXTLIS: "ELI",
        EURONEXTOSE: "OSL",
        EURONEXTPAR: "EPA",
        EUROTLX: "BIT",
        // F
        FSE: "FKSE",
        FWB: "FRA",
        // G
        GPW: "WSE",
        // H
        HAM: "HAM",
        HAN: "HAM",
        HNX: "HNX",
        HKEX: "HKG",
        HOSE: "HOSE",
        // I
        IDX: "IDX",
        // J
        JSE: "JSE",
        // K
        KRX: "KRX",
        KSE: "KWSE",
        // L
        LJSE: "LJSE",
        LS: "FRA",
        LSE: "LON",
        LSIN: "LON",
        LSX: "FRA",
        LUXSE: "LUX",
        // M
        MIL: "BIT",
        MUN: "MUN",
        MYX: "KLSE",
        // N
        NAG: "XNGO",
        NASDAQ: "NASDAQ",
        NASDAQDUBAI: "DFM",
        NEO: "NEO",
        NEWCONNECT: "WSE",
        NGM: "NGM",
        NSE: "NSE",
        NSEKE: "NASE",
        NSENG: "NGX",
        NZX: "NZE",
        // O
        OMXCOP: "CPH",
        OMXHEX: "HEL",
        OMXICE: "ICE",
        OMXRSE: "RSE",
        OMXSTO: "STO",
        OMXTSE: "TAL",
        OMXVSE: "VSE",
        OTC: "OTC",
        // P
        PSECZ: "PRA",
        PSE: "PSE",
        PSX: "PSX",
        // Q
        QSE: "QSE",
        // R
        RUS: "MOEX",
        // S
        SAPSE: "SPSE",
        SET: "BKK",
        SGX: "SGX",
        SIX: "SWX",
        SSE: "SHA",
        SWB: "BST",
        SZSE: "SHE",
        // T
        TADAWUL: "TADAWUL",
        TASE: "TLV",
        TRADEGATE: "FRA",
        TSX: "TSX",
        TSXV: "TSXV",
        TSE: "TYO",
        TPEX: "TPEX",
        TWSE: "TPE",
        // U
        UPCOM: "HNX",
        // V
        VIE: "VIE",
        // X
        XETR: "ETR",
        // Z
        ZSE: "ZSE",
      };

      function toTitleCase(str) { return str.toLowerCase().replace(/\b\w/g, (c) => c.toUpperCase()); }
      function getSelectedSource() { return document.querySelector('input[name="source"]:checked').value; }
      function getSelectedDataPoints() {
        return Array.from(document.querySelectorAll("#checkboxGrid input:checked")).map((cb) => cb.value);
      }
      function resolveExchangeCode(rawValue) {
        const raw = String(rawValue || "").trim();
        const found = exchanges.find((ex) => ex.name.toLowerCase() === raw.toLowerCase());
        return found ? found.code : raw;
      }
      function saExchangeCode(tvCode) {
        const tv = String(tvCode).toUpperCase();
        return SA_EXCHANGE_MAP[tv] || tv;
      }
      function saBaseUrl(exchangeCode, ticker) {
        const tv = String(exchangeCode).toUpperCase();
        const ex = saExchangeCode(exchangeCode).toLowerCase();
        let tk = String(ticker).toLowerCase();

        // ── Hong Kong tickers: pad to 4 digits ──
        //    2-digit  → prepend "00"
        //    3-digit  → prepend "0"
        if (tv === "HKEX" && /^\d{2,3}$/.test(tk)) {
          tk = tk.padStart(4, "0");
        }

        const usExchanges = ["otc", "nasdaq", "nyse", "amex"];
        return usExchanges.includes(ex)
          ? `https://www.stockanalysis.com/stocks/${tk}`
          : `https://www.stockanalysis.com/quote/${ex}/${tk}`;
      }
      function mapTvExchange(exchangeCode) {
        return String(exchangeCode).toUpperCase();
      }
      function tvSymbol(exchangeCode, ticker) {
        return `${mapTvExchange(exchangeCode)}-${String(ticker).toUpperCase()}`;
      }

      function buildPackageTargets(exchangeCode, ticker, isSemester) {
        const sa = saBaseUrl(exchangeCode, ticker);
        const tv = `https://www.tradingview.com/symbols/${tvSymbol(exchangeCode, ticker)}`;
        // FH for Semester, FQ for Quarterly
        const period = isSemester ? "FH" : "FQ";
        return [
          { id: "pkg-overview-sa", name: "🏢 Overview — StockAnalysis", url: `${sa}/company` },
          { id: "pkg-overview-tv", name: "🏢 Overview — TradingView", url: `${tv}/` },
          { id: "pkg-history-py", name: "⏳ Historical Data — Python (yfinance quarterly / semiannual closes)", url: "local", local: true },
          { id: "pkg-income-tv", name: "📑 Income Statement — TradingView", url: `${tv}/financials-income-statement/?statements-period=${period}&selected=total_revenue%2Cnet_revenue%2Cnet_income%2Cdiluted_shares_outstanding` },
          { id: "pkg-balance-tv", name: "⚖️ Balance Sheet — TradingView", url: `${tv}/financials-balance-sheet/?statements-period=${period}&selected=total_equity` },
          { id: "pkg-ratios-tv", name: "📊 Ratios — TradingView", url: `${tv}/financials-statistics-and-ratios/?statistics-period=${period}&selected=price_earnings%2Cprice_book%2Cnet_margin` },
        ];
      }

      function buildTradingViewTargets(exchangeCode, ticker) {
        const tvEx = mapTvExchange(exchangeCode);
        const tk = String(ticker).toUpperCase();
        const base = `https://www.tradingview.com/symbols/${tvEx}-${tk}`;
        return [
          { id: "news", name: "📰 Latest News", url: `https://www.google.com/search?q=${tvEx}:%20${tk}&tbm=nws` },
          { id: "overview", name: "🏢 Overview", url: `${base}/` },
          { id: "history", name: "⏳ Historical Data", url: `${base}/?timeframe=120M` },
          { id: "income", name: "📑 Income Statement", url: `${base}/financials-income-statement/?statements-period=FQ&selected=total_revenue%2Cnet_revenue%2Cnet_income%2Cdiluted_shares_outstanding` },
          { id: "balance", name: "⚖️ Balance Sheet", url: `${base}/financials-balance-sheet/?statements-period=FQ&selected=total_equity` },
          { id: "cash", name: "🔄 Cash Flow", url: `${base}/financials-cash-flow/?statements-period=FQ` },
          { id: "stats", name: "📊 Financial Stats", url: `${base}/financials-statistics-and-ratios/?statistics-period=FQ&selected=price_earnings%2Cprice_book%2Cnet_margin` },
          { id: "revenue", name: "💰 Revenue", url: `${base}/financials-revenue/` },
          { id: "dividends", name: "💸 Dividends", url: `${base}/financials-dividends/` },
        ];
      }

      function buildStockAnalysisTargets(exchangeCode, ticker) {
        const ex = String(exchangeCode).toLowerCase();
        const tk = String(ticker).toLowerCase();
        const baseUrl = saBaseUrl(ex, tk);
        return [
          { id: "news", name: "📰 Latest News", url: `https://www.google.com/search?q=${ex}:%20${tk}&tbm=nws` },
          { id: "overview", name: "🏢 Overview", url: `${baseUrl}/company` },
          { id: "history", name: "⏳ Historical Data", url: `${baseUrl}/history/` },
          { id: "income", name: "📑 Income Statement", url: `${baseUrl}/financials/income-statement/?p=quarterly` },
          { id: "balance", name: "⚖️ Balance Sheet", url: `${baseUrl}/financials/balance-sheet/?p=quarterly` },
          { id: "cash", name: "🔄 Cash Flow", url: `${baseUrl}/financials/cash-flow-statement/?p=quarterly` },
          { id: "stats", name: "📊 Financial Ratios", url: `${baseUrl}/financials/ratios/?p=quarterly` },
          { id: "revenue", name: "💰 Revenue", url: `${baseUrl}/financials/metrics/` },
          { id: "dividends", name: "💸 Dividends", url: `${baseUrl}/dividend/` },
        ];
      }

      // --- Event listeners for automatic formatting ---
      exchangeInput.addEventListener("input", (e) => {
        const start = e.target.selectionStart;
        const end = e.target.selectionEnd;
        e.target.value = toTitleCase(e.target.value);
        e.target.setSelectionRange(start, end);
      });

      tickerInput.addEventListener("input", (e) => {
        const start = e.target.selectionStart;
        const end = e.target.selectionEnd;
        e.target.value = e.target.value.toUpperCase();
        e.target.setSelectionRange(start, end);
      });

      function updateSourceUI() {
        const source = getSelectedSource();
        const isPackage = source.includes("package");
        checkboxGrid.classList.toggle("is-disabled", isPackage);
        checkboxGrid.querySelectorAll('input[type="checkbox"]').forEach((cb) => (cb.disabled = isPackage));
        // Force ticker to uppercase for all source types
        tickerInput.value = tickerInput.value.toUpperCase();
      }
      radioButtons.forEach((r) => r.addEventListener("change", updateSourceUI));

      function toggleAllCheckboxes(selectAll) {
        if (getSelectedSource().includes("package")) return;
        checkboxGrid.querySelectorAll('input[type="checkbox"]').forEach((cb) => (cb.checked = selectAll));
      }

      function getPeriodLabel(dateStr, freq) {
        const dt = new Date(dateStr + "T00:00:00");
        const y = dt.getFullYear();
        const m = dt.getMonth() + 1;

        if (m === 3) return `1Q${y}`;
        if (m === 6) return `1H${y}`;
        if (m === 9) return `9M${y}`;
        if (m === 12) return `FY${y}`;
        return ""; // fallback (will not be called because it has already been filtered)
      }

      function processPeriodData(timestamps, closes, freq) {
        // 1) Find latest close (most recent valid trading day)
        let latest = null;
        for (let i = timestamps.length - 1; i >= 0; i--) {
          if (closes[i] === null || closes[i] === undefined) continue;
          const d = new Date(timestamps[i] * 1000);
          latest = {
            date: d.toISOString().split("T")[0],
            close: closes[i],
          };
          break;
        }

        // 2) Group by period (quarterly or semiannual), keep last close per period
        const grouped = {};
        const order = [];
        for (let i = 0; i < timestamps.length; i++) {
          if (closes[i] === null || closes[i] === undefined) continue;
          const d = new Date(timestamps[i] * 1000);
          const y = d.getFullYear();
          const m = d.getMonth(); // 0-11

          let key;
          if (freq === "semiannual") {
            // Keep only June (index 5) and December (index 11)
            if (m !== 5 && m !== 11) continue;
            key = `${y}-H${m === 5 ? 1 : 2}`;
          } else {
            // Quarterly — keep only standard quarter-end months: Mar (2), Jun (5), Sep (8), Dec (11)
            // This filters out October so neither 10M2026 nor 4Q2026 appears.
            if (m !== 2 && m !== 5 && m !== 8 && m !== 11) continue;
            key = `${y}-Q${Math.floor(m / 3) + 1}`;
          }

          if (!grouped[key]) order.push(key);
          grouped[key] = {
            date: d.toISOString().split("T")[0],
            close: closes[i],
            period: getPeriodLabel(d.toISOString().split("T")[0], freq),
          };
        }

        const periodData = order.map((k) => grouped[k]);
        // 3) Sort newest → oldest
        periodData.sort((a, b) => new Date(b.date) - new Date(a.date));

        return { latest, periodData };
      }

      async function openHistoryTab(exchangeCode, ticker, initialFreq) {
        let freq = (initialFreq === "semiannual") ? "semiannual" : "quarterly";
        let cachedTimestamps = null;
        let cachedCloses = null;
        let cachedSymbol = null;

        const newTab = window.open("", "_blank");
        if (!newTab) {
          Swal.fire(getToastConfig("error", "Popup blocked! Please allow popups for this site."));
          return;
        }

        const suffix = YAHOO_SUFFIX_MAP[exchangeCode.toUpperCase()] || "";
        let baseTicker = ticker.toUpperCase();

        // ── Hong Kong tickers: pad to 4 digits ──
        //    2-digit  → prepend "00"
        //    3-digit  → prepend "0"
        if (exchangeCode.toUpperCase() === "HKEX" && /^\d{2,3}$/.test(baseTicker)) {
          baseTicker = baseTicker.padStart(4, "0");
        }

        const symbol = baseTicker + suffix;

        newTab.document.write(`<html><head><title>Loading...</title></head><body style="font-family:system-ui;padding:40px;text-align:center;background:#f1f5f9"><h2>Fetching historical data for ${symbol}...</h2><p>Please wait.</p></body></html>`);

        const proxyUrl = `/proxy?symbol=${encodeURIComponent(symbol)}&range=10y&interval=1d`;

        // ── Build the full popup page HTML for current `freq` ─────────
        function buildPageHtml() {
          const freqTitle = freq === "semiannual" ? "Semiannual" : "Quarter-End";
          const { latest, periodData } = processPeriodData(cachedTimestamps, cachedCloses, freq);
          if (!periodData || periodData.length === 0) {
            return `<!DOCTYPE html><html><head><meta charset="UTF-8"><title>No Data</title></head>
              <body style="font-family:system-ui;padding:40px;text-align:center;background:#f1f5f9;color:#1e293b">
              <h2 style="color:#ef4444">No ${freqTitle.toLowerCase()} data available for this ticker.</h2>
              <p>Try switching to the other frequency.</p>
              <div style="margin-top:20px">
                <button data-freq="quarterly" style="padding:10px 18px;margin:4px;border:none;border-radius:8px;background:#2563eb;color:#fff;font-weight:700;cursor:pointer">Quarterly</button>
                <button data-freq="semiannual" style="padding:10px 18px;margin:4px;border:none;border-radius:8px;background:#2563eb;color:#fff;font-weight:700;cursor:pointer">Semiannual</button>
              </div></body></html>`;
          }

          const fmtClose = (v) =>
            v.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 5 });

          const latestDateCell = latest ? latest.date : "—";
          const latestCloseCell = latest ? fmtClose(latest.close) : "—";
          const latestHeader = latest ? latest.date : "—";

          return `<!DOCTYPE html>
            <html lang="en">
            <head>
            <meta charset="UTF-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1.0" />
            <title>Historical Data — ${symbol}</title>
            <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>💼</text></svg>" />
            <style>
              :root{
                --bg:#f1f5f9; --card:#ffffff; --text:#1e293b; --muted:#64748b;
                --border:#e2e8f0; --primary:#2563eb; --stripe:#f8fafc; --hover:#eff6ff;
              }
              @media (prefers-color-scheme: dark){
                :root{
                  --bg:#0f172a; --card:#1e293b; --text:#f1f5f9; --muted:#94a3b8;
                  --border:#334155; --primary:#3b82f6; --stripe:#243449; --hover:#2d3f5c;
                }
              }
              *{box-sizing:border-box}
              body{
                font-family:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;
                margin:0; padding:22px 14px 44px; background:var(--bg); color:var(--text);
                -webkit-text-size-adjust:100%;
              }
              .container{
                max-width: 98%; margin: 0 auto; background:var(--card); border-radius:14px;
                box-shadow:0 10px 25px -5px rgba(0,0,0,.15); overflow:hidden;
              }
              .header{background:var(--primary); color:#fff; padding:22px 18px; text-align:center}
              .header h1{margin:0; font-size:clamp(1.05rem,3.4vw,1.5rem); font-weight:800; word-break:break-word}
              .header p{margin:6px 0 0; font-size:clamp(.74rem,2.4vw,.9rem); opacity:.88}

              /* ── Frequency toggle inside popup ── */
              .freq-switch{
                display:inline-flex; gap:4px; margin-top:14px;
                background:rgba(255,255,255,0.16); padding:4px; border-radius:10px;
              }
              .freq-btn{
                padding:8px 16px; border:none; border-radius:8px; background:transparent;
                color:#fff; font-weight:700; font-size:0.82rem; cursor:pointer;
                transition: all .2s ease; letter-spacing:.2px;
              }
              .freq-btn:hover{ background:rgba(255,255,255,0.18); }
              .freq-btn.active{ background:#fff; color:var(--primary); }

              .table-wrap{width:100%; overflow-x:auto; -webkit-overflow-scrolling:touch}
              table{border-collapse:collapse; width:100%; min-width:max-content}
              th,td{
                padding: 8px 10px; border-bottom:1px solid var(--border); white-space:nowrap;
                font-variant-numeric:tabular-nums;
              }
              thead th{
                background:var(--stripe); color:var(--muted);
                font-size: 0.75rem; font-weight:700; letter-spacing:.4px;
                text-transform:uppercase; text-align:center;
                position:sticky; top:0; z-index:3;
              }
              thead th:first-child{
                left:0; z-index:4; text-align:left; padding-left: 12px;
                font-size: 0.75rem; font-weight:700;
                text-transform:uppercase; color:var(--muted); letter-spacing:.4px;
              }
              thead th.period-value{
                text-align:center; color:var(--text);
                font-size: 0.8rem; font-weight:600;
                letter-spacing:0; text-transform:none;
              }
              thead th.latest-head{
                background: var(--stripe); color: var(--muted);
                border-bottom: 1px solid var(--border);
                text-transform: uppercase; font-size: 0.75rem;
                font-weight: 700; letter-spacing:.4px;
              }
              tbody td.latest-cell{
                background: transparent;
                font-weight: 600;
                color: var(--text);
              }
              tbody th{
                position:sticky; left:0; z-index:2; background:var(--stripe); text-align:left;
                font-size: 0.75rem; font-weight:700; color:var(--muted);
                text-transform:uppercase; letter-spacing:.4px;
                border-right:1px solid var(--border); padding-left: 12px;
              }
              tbody td{
                text-align:center; font-size: 0.85rem; font-weight:600; color:var(--text);
              }
              tbody tr:hover td{background:var(--hover)}
              tbody tr:hover td.latest-cell{background: var(--hover);}
              tbody tr:last-child th, tbody tr:last-child td{border-bottom:none}
              .foot{padding:14px 18px; font-size:.75rem; color:var(--muted); text-align:center; line-height:1.6}

              @media (max-width:600px){
                body{padding:10px 5px 20px}
                .header{padding:15px 10px}
                th,td{padding:6px 8px}
                thead th, thead th:first-child, tbody th{ font-size:0.65rem; }
                thead th.period-value, tbody td{ font-size:0.75rem; }
                .foot{font-size:.65rem; padding:10px}
                .freq-btn{ padding:6px 12px; font-size:0.72rem; }
              }
            </style>
            </head>
            <body>
              <div class="container">
                <div class="header">
                  <h1>${symbol} — Historical Data</h1>
                  <p>${freqTitle} Closing Prices &middot; Last 10 Years &middot; Newest First &middot; Includes Current Close</p>
                  <div class="freq-switch">
                    <button data-freq="quarterly" class="freq-btn ${freq === "quarterly" ? "active" : ""}">Quarterly</button>
                    <button data-freq="semiannual" class="freq-btn ${freq === "semiannual" ? "active" : ""}">Semiannual</button>
                  </div>
                </div>
                <div class="table-wrap">
                  <table>
                    <thead>
                      <tr>
                        <th scope="col">Period</th>
                        <th scope="col" class="period-value">Current</th>
                        ${periodData.map((d) => `<th scope="col" class="period-value">${d.period}</th>`).join("")}
                      </tr>
                    </thead>
                    <tbody>
                      <tr>
                        <th scope="row">Actual Date</th>
                        <td class="latest-cell">${latestDateCell}</td>
                        ${periodData.map((d) => `<td>${d.date}</td>`).join("")}
                      </tr>
                      <tr>
                        <th scope="row">Close Price</th>
                        <td class="latest-cell">${latestCloseCell}</td>
                        ${periodData.map((d) => `<td>${fmtClose(d.close)}</td>`).join("")}
                      </tr>
                    </tbody>
                  </table>
                </div>
                <p class="foot">Swipe horizontally to view every period. All figures are period-end closing prices in the listing currency. The <b>Current</b> column shows the most recent trading day close (${latestHeader}).</p>
              </div>
            </body>
            </html>`;
        }

        // Paint the popup and re-attach toggle handlers
        function paint() {
          newTab.document.open();
          newTab.document.write(buildPageHtml());
          newTab.document.close();
          // Re-attach click handlers to the toggle buttons
          newTab.document.querySelectorAll("[data-freq]").forEach((btn) => {
            btn.addEventListener("click", (e) => {
              e.preventDefault();
              const f = btn.getAttribute("data-freq");
              if (f === freq) return;
              freq = f;
              paint();
            });
          });
        }

        try {
          const response = await fetch(proxyUrl);
          if (!response.ok) {
            const errText = await response.text();
            throw new Error(`Server returned ${response.status}: ${errText.slice(0, 200)}`);
          }
          const data = await response.json();
          if (!data.chart || !data.chart.result || data.chart.result.length === 0) {
            throw new Error("No data found for this ticker symbol.");
          }
          const result = data.chart.result[0];
          cachedTimestamps = result.timestamp;
          cachedCloses = result.indicators.quote[0].close;
          if (!cachedTimestamps || !cachedCloses) throw new Error("Incomplete data received.");
          cachedSymbol = symbol;

          paint();
        } catch (error) {
          console.error("Error fetching history:", error);
          newTab.document.open();
          newTab.document.write(`<!DOCTYPE html>
            <html lang="en">
            <head>
            <meta charset="UTF-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1.0" />
            <title>Historical Data — Error</title>
            <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>💼</text></svg>" />
            </head>
            <body style="font-family:system-ui;padding:40px 20px;text-align:center;background:#f1f5f9;color:#1e293b;margin:0">
              <h2 style="color:#ef4444;margin:0 0 10px">Error Fetching Data</h2>
              <p style="margin:0 0 8px">${error.message}</p>
              <p style="font-size:.9rem;color:#64748b;margin:0">Please check the ticker symbol and try again.</p>
            </body>
            </html>`);
          newTab.document.close();
        }
      }

      function processSearch() {
        const rawExchange = exchangeInput.value.trim();
        // Force ticker to uppercase at the start
        const ticker = tickerInput.value.trim().toUpperCase();
        const source = getSelectedSource();
        const freq = (source === "semester_package") ? "semiannual" : "quarterly";
        if (!rawExchange || !ticker) {
          Swal.fire(getToastConfig("error", "Exchange & Ticker code specifications are required!"));
          return;
        }
        const exchangeCode = resolveExchangeCode(rawExchange);
        let targets = [];
        
        if (source.includes("package")) {
          const isSemester = (source === "semester_package");
          targets = buildPackageTargets(exchangeCode, ticker, isSemester);
        } else {
          const selectedData = getSelectedDataPoints();
          if (selectedData.length === 0) {
            Swal.fire(getToastConfig("warning", "Select at least one tracking data configuration point!"));
            return;
          }
          const allTargets = source === "stockanalysis" ? buildStockAnalysisTargets(exchangeCode, ticker) : buildTradingViewTargets(exchangeCode, ticker);
          targets = allTargets.filter((t) => selectedData.includes(t.id));
        }
        Swal.fire(getToastConfig("success", `Opening ${targets.length} analysis tabs layout links window`));
        document.getElementById("hintText").style.display = "block";
        const container = document.getElementById("linkContainer");
        const list = document.getElementById("linkList");
        list.innerHTML = "";
        container.style.display = "block";

        targets.forEach((item, index) => {
          const a = document.createElement("a");
          a.href = item.local ? "#" : item.url;
          a.target = item.local ? "_self" : "_blank";
          a.className = "link-item";
          a.innerText = item.name;
          if (item.local) {
            a.addEventListener("click", (e) => { e.preventDefault(); openHistoryTab(exchangeCode, ticker, freq); });
          }
          list.appendChild(a);
          setTimeout(() => {
            if (item.local) { openHistoryTab(exchangeCode, ticker, freq); }
            // ── pass freq
            else { window.open(item.url, "_blank"); }
          }, index * 350);
        });
      }

      function resetStockForm() {
        exchangeInput.value = "";
        tickerInput.value = "";
        checkboxGrid.querySelectorAll('input[type="checkbox"]').forEach((cb) => (cb.checked = false));
        document.getElementById("linkContainer").style.display = "none";
        document.getElementById("hintText").style.display = "none";
        Swal.fire(getToastConfig("success", "Stock profile inputs configuration reset."));
      }

      clickBtn.addEventListener("click", () => {
        count++;
        counterDisplay.textContent = count;
        counterDisplay.style.transform = "scale(1.15)";
        setTimeout(() => { counterDisplay.style.transform = "scale(1)"; }, 100);
      });
      resetCounterBtn.addEventListener("click", () => {
        const currentTheme = document.documentElement.getAttribute("data-theme");
        Swal.fire({ title: "Reset counter metrics?", icon: "warning", showCancelButton: true,
          confirmButtonText: "Yes", confirmButtonColor: "#ef4444", cancelButtonColor: "#64748b",
          background: currentTheme === "dark" ? "#1e293b" : "#ffffff",
          color: currentTheme === "dark" ? "#f1f5f9" : "#1e293b" }).then((result) => {
          if (result.isConfirmed) { count = 0; counterDisplay.textContent = count; Swal.fire(getToastConfig("success", "Metrics cleared back to zero.")); }
        });
      });

      decrementBtn.addEventListener("click", () => {
        if (count <= 0) {
          counterDisplay.style.transform = "scale(0.9)";
          setTimeout(() => { counterDisplay.style.transform = "scale(1)"; }, 100);
          return; // already 0, cannot be reduced further
        }
        count--;
        counterDisplay.textContent = count;
        counterDisplay.style.transform = "scale(0.85)";
        setTimeout(() => { counterDisplay.style.transform = "scale(1)"; }, 100);
      });

      window.addEventListener("keydown", (e) => {
        // Normalise key so "R" and "r" are treated identically
        const key = (e.key || "").toLowerCase();
        const hasModifier = e.ctrlKey || e.metaKey;

        // ── Block every known page-refresh shortcut ─────────────────────
        //   Ctrl+R / Cmd+R           → normal reload
        //   Ctrl+Shift+R / Cmd+Shift+R → hard reload (bypass cache)
        //   F5                       → normal reload
        //   Ctrl+F5 / Shift+F5       → hard reload (Windows/Linux)
        const isRefreshCombo =
          (hasModifier && key === "r") ||         // Ctrl+R, Ctrl+Shift+R, Cmd+R, Cmd+Shift+R
          e.key === "F5" ||                       // F5, Ctrl+F5, Shift+F5
          key === "f5";                           // fallback for odd layouts

        if (isRefreshCombo) {
          e.preventDefault();
          e.stopPropagation();
          Swal.fire(
            getToastConfig(
              "info",
              "Page refresh shortcuts are disabled to keep your counter and workspace state stable."
            )
          );
          return false;
        }

        // Enter triggers the stock search (unchanged)
        if (e.key === "Enter") {
          const tag = (e.target.tagName || "").toUpperCase();
          if (tag === "TEXTAREA") return;
          if (tag === "BUTTON") return;
          e.preventDefault();
          processSearch();
        }
      }, { capture: true });

      function transformText(type) {
        let str = textInput.value;
        if (!str.trim()) { Swal.fire(getToastConfig("warning", "Workspace input target value field is empty!")); return; }
        switch (type) {
          case "upper": textInput.value = str.toUpperCase(); break;
          case "lower": textInput.value = str.toLowerCase(); break;
          case "capitalize": textInput.value = str.toLowerCase().split(/\s+/).map((w) => w.charAt(0).toUpperCase() + w.slice(1)).join(" "); break;
          case "sentence": let low = str.toLowerCase().trim(); textInput.value = low.charAt(0).toUpperCase() + low.slice(1); break;
          // REMOVED: Toggle case logic
        }
      }
      function copyText() {
        if (!textInput.value.trim()) { Swal.fire(getToastConfig("error", "No printable text characters array string value found to copy inside document buffer!")); return; }
        textInput.select();
        navigator.clipboard.writeText(textInput.value).then(() => { Swal.fire(getToastConfig("success", "Value saved cleanly inside system clipboard stack!")); });
      }
      function clearText() {
        if (!textInput.value) return;
        textInput.value = "";
        Swal.fire(getToastConfig("success", "Text records purged safely."));
      }

      (function () {
        "use strict";
        var inputEl = document.getElementById("input");
        var outputEl = document.getElementById("output");
        var statsEl = document.getElementById("stats");
        var copyBtn = document.getElementById("copyBtn");
        var sampleBtn = document.getElementById("sampleBtn");
        var clearBtn = document.getElementById("clearBtn");
        var reverseCheckbox = document.getElementById("reverseOrder");
        var MULT = { K: 1000n, M: 1000000n, B: 1000000000n, T: 1000000000000n };
        var INVISIBLE = /[\u200b-\u200f\u202a-\u202e\u2066-\u2069\ufeff]/g;
        var SAMPLE = ["9.26 T","\u22122.05%","9.70 T","+4.25%","10.33 T","+9.01%","9.90 T","+1.90%","10.55 T","+13.93%","10.06 T","+3.75%","10.12 T","\u22122.02%","11.64 T","+17.60%"].join("\n");
        function groupThousands(digits) { return digits.replace(/\B(?=(\d{3})+(?!\d))/g, ","); }
        function convertLine(line) {
          var s = String(line).replace(INVISIBLE, "").trim();
          if (!s) return { skip: true };
          if (s.indexOf("%") !== -1) return { skip: true };
          s = s.replace(/\u2212/g, "-").replace(/[\u2013\u2014]/g, "-").replace(/\s+/g, "");
          var m = s.match(/^([+-]?)(\d+(?:[.,]\d+)?)([KMBT])?$/i);
          if (!m) return { invalid: true };
          var numStr = m[2];
          if (numStr.indexOf(",") !== -1 && numStr.indexOf(".") !== -1) { numStr = numStr.replace(/,/g, ""); }
          else { numStr = numStr.replace(",", "."); }
          var suffix = (m[3] || "").toUpperCase();
          var mult = MULT[suffix] || 1n;
          var isNeg = m[1] === "-";
          var parts = numStr.split(".");
          var intPart = parts[0];
          var fracPart = parts[1] || "";
          var digits = (intPart + fracPart).replace(/^0+(?=\d)/, "") || "0";
          var scale = 10n ** BigInt(fracPart.length);
          var value = (BigInt(digits) * mult) / scale;
          var out = groupThousands(value.toString());
          return { value: (isNeg && value !== 0n ? "-" : "") + out };
        }
        function render() {
          var lines = inputEl.value.split(/\r?\n/);
          var results = [];
          var converted = 0, skipped = 0, invalid = 0;
          for (var i = 0; i < lines.length; i++) {
            var r = convertLine(lines[i]);
            if (r.skip) { skipped++; continue; }
            if (r.invalid) { invalid++; continue; }
            results.push(r.value); converted++;
          }
          if (reverseCheckbox.checked) { results.reverse(); }
          outputEl.value = results.join("\t");
          if (!inputEl.value.trim()) { statsEl.textContent = ""; }
          else {
            var bits = [converted + " converted"];
            if (skipped) bits.push(skipped + " skipped");
            if (invalid) bits.push(invalid + " unrecognised");
            statsEl.textContent = bits.join(" · ");
          }
        }
        function copyTextToClipboard(text) {
          if (navigator.clipboard && window.isSecureContext) {
            return navigator.clipboard.writeText(text).then(function () { return true; }).catch(function () { return legacyCopy(text); });
          }
          return Promise.resolve(legacyCopy(text));
        }
        function legacyCopy(text) {
          var ta = document.createElement("textarea");
          ta.value = text; ta.setAttribute("readonly", "");
          ta.style.position = "fixed"; ta.style.top = "-1000px"; ta.style.opacity = "0";
          document.body.appendChild(ta); ta.select(); ta.setSelectionRange(0, ta.value.length);
          var ok = false;
          try { ok = document.execCommand("copy"); } catch (e) { ok = false; }
          document.body.removeChild(ta); return ok;
        }
        inputEl.addEventListener("input", render);
        reverseCheckbox.addEventListener("change", render);
        copyBtn.addEventListener("click", function () {
          var text = outputEl.value.trim();
          if (!text) { Swal.fire(getToastConfig("warning", "Nothing to copy yet.")); return; }
          copyTextToClipboard(text).then(function (ok) {
            Swal.fire(getToastConfig(ok ? "success" : "error", ok ? "Copied! Paste it into your spreadsheet row." : "Copy failed — please select and copy manually."));
          });
        });
        sampleBtn.addEventListener("click", function () { inputEl.value = SAMPLE; render(); inputEl.focus(); });
        clearBtn.addEventListener("click", function () { inputEl.value = ""; outputEl.value = ""; statsEl.textContent = ""; inputEl.focus(); });
        render();
      })();

      // ─────────────────────────────────────────────────────────────
      //  TICKER SYMBOL EXTRACTOR
      // ─────────────────────────────────────────────────────────────
      (function () {
        "use strict";
        var inputEl = document.getElementById("tickerInput");
        var outputEl = document.getElementById("tickerOutput");
        var statsEl = document.getElementById("tickerStats");
        var copyBtn = document.getElementById("tickerCopyBtn");
        var sampleBtn = document.getElementById("tickerSampleBtn");
        var clearBtn = document.getElementById("tickerClearBtn");
        var dedupeBox = document.getElementById("tickerDedupe");
        var descBox = document.getElementById("tickerDesc");
        var tabbedBox = document.getElementById("tickerTabbed");

        // Ticker line = alphabetic (2-6 chars) OR numeric (2-6 digits)
        var TICKER_RE = /^([A-Z][A-Z0-9]{1,5}|\d{2,6})$/;

        // Common financial abbreviations that could appear on their own line.
        var NOISE = {
          TTM: 1, EPS: 1, YOY: 1, QOQ: 1, ETF: 1, IPO: 1, CEO: 1, CFO: 1,
          ROE: 1, ROA: 1, ROI: 1, NAV: 1, ALL: 1, NONE: 1, NA: 1
        };

        var SAMPLE = [
          "Symbol",
          "Mkt cap",
          "Price",
          "Chg %",
          "Vol",
          "Rel vol",
          "P/E",
          "EPS dil",
          "TTM",
          "EPS dil growth",
          "TTM YoY",
          "Div yield %",
          "TTM",
          "Sector",
          "Analyst rating",
          "Symbol",
          "Mkt cap",
          "Price",
          "Chg %",
          "Vol",
          "Rel vol",
          "P/E",
          "EPS dil",
          "TTM",
          "EPS dil growth",
          "TTM YoY",
          "Div yield %",
          "TTM",
          "Sector",
          "Analyst rating",
          "2",
          "2475",
          "Luxshare Precision Industry Co., Ltd. Class H",
          "D",
          "446.21 B HKD\t52.95 HKD\t-1.12%\t436.69 K\t0.19\t—\t—\t—\t0.00%\tElectronic technology",
          "Strong buy",
          "6",
          "6951",
          "Chaozhou Three-Circle (Group) Co., Ltd. Class H",
          "D",
          "272.95 B HKD\t124.1 HKD\t-2.90%\t173.86 K\t0.11\t—\t—\t—\t0.00%\tElectronic technology",
          "Strong buy",
          "",
          "2476",
          "Victory Giant Technology (HuiZhou) Co., Ltd. Class H",
          "D",
          "194.06 B HKD\t195.1 HKD\t-1.22%\t546.33 K\t0.16\t32.72\t5.96 HKD\t—\t0.00%\tElectronic technology",
          "Strong buy",
          "3",
          "3228",
          "Shenzhen Kinwong Electronic Co., Ltd. Class H",
          "D",
          "121.15 B HKD\t74.40 HKD\t-3.19%\t522.7 K\t—\t54.25\t1.37 HKD\t-0.06%\t0.00%\tElectronic technology",
          "No rating",
          "",
          "1989",
          "Delton Technology (Guangzhou) Inc. Class H",
          "D",
          "69.2 B HKD\t118.1 HKD\t-1.25%\t214.2 K\t0.06\t33.36\t3.54 HKD\t—\t0.62%\tElectronic technology",
          "Strong buy",
          "",
          "2382",
          "Sunny Optical Technology (Group) Co., Ltd.",
          "D",
          "69.2 B HKD\t62.05 HKD\t-2.05%\t4.96 M\t0.81\t12.64\t4.91 HKD\t+51.68%\t1.90%\tElectronic technology",
          "Buy",
          "",
          "6088",
          "FIT Hon Teng Limited",
          "D",
          "35.09 B HKD\t4.845 HKD\t-2.02%\t7.95 M\t0.35\t27.10\t0.18 HKD\t+6.56%\t0.00%\tElectronic technology",
          "Strong buy",
          "",
          "1879",
          "Shanghai Xizhi Technology Co., Ltd Class H",
          "D",
          "26.5 B HKD\t280.0 HKD\t-0.64%\t33.41 K\t0.07\t—\t—\t—\t0.00%\tElectronic technology",
          "Strong buy",
          "",
          "1478",
          "Q Technology (Group) Co. Ltd.",
          "D",
          "6.05 B HKD\t5.060 HKD\t0.00%\t2.68 M\t0.78\t3.75\t1.35 HKD\t+214.98%\t10.87%\tElectronic technology",
          "Buy",
          "",
          "1300",
          "Trigiant Group Ltd.",
          "D",
          "5.06 B HKD\t2.625 HKD\t-8.22%\t9.04 M\t0.68\t14.26\t0.18 HKD\t—\t0.00%\tElectronic technology",
          "No rating",
          "",
          "679",
          "Asia Tele-Net and Technology Corp Ltd",
          "D",
          "1.73 B HKD\t4.200 HKD\t-8.10%\t350 K\t0.54\t—\t-0.12 HKD\t-66.36%\t0.88%\tElectronic technology",
          "No rating",
          "",
          "1037",
          "Maxnerva Technology Services Limited",
          "D",
          "444.89 M HKD\t0.620 HKD\t-1.59%\t1.36 M\t3.44\t—\t-0.00 HKD\t-313.64%\t0.00%\tElectronic technology",
          "No rating",
          "",
          "567",
          "Jsmart Technologies Group Limited",
          "D",
          "435.59 M HKD\t0.270 HKD\t0.00%\t180 K\t0.41\t—\t-0.01 HKD\t-0.76%\t0.00%\tElectronic technology",
          "No rating",
          "",
          "1679",
          "Risecomm Group Holdings Limited",
          "D",
          "374.18 M HKD\t1.320 HKD\t+0.76%\t92 K\t1.59\t—\t-0.13 HKD\t+78.80%\t0.00%\tElectronic technology",
          "No rating",
          "",
          "8375",
          "Data Union Capital International Holdings Group Limited",
          "D",
          "317.95 M HKD\t0.800 HKD\t-13.04%\t50 K\t0.40\t—\t-0.05 HKD\t-8.21%\t0.00%\tElectronic technology",
          "No rating",
          "",
          "1480",
          "Yan Tat Group Holdings Limited",
          "D",
          "240 M HKD\t1.000 HKD\t0.00%\t22 K\t0.24\t—\t-0.13 HKD\t-172.50%\t3.00%\tElectronic technology",
          "No rating",
          "",
          "1120",
          "Arts Optical International Holdings Limited",
          "D",
          "231.76 M HKD\t0.540 HKD\t-10.00%\t302 K\t2.57\t9.33\t0.06 HKD\t—\t0.00%\tElectronic technology",
          "No rating",
          "",
          "8070",
          "Keen Ocean International Holding Ltd.",
          "D",
          "215 M HKD\t1.075 HKD\t-2.27%\t20 K\t0.10\t3.90\t0.28 HKD\t+239.53%\t0.00%\tElectronic technology",
          "No rating",
          "",
          "759",
          "CEC International Holdings Limited",
          "D",
          "156.55 M HKD\t0.227 HKD\t-3.40%\t46 K\t0.94\t—\t-0.06 HKD\t+10.64%\t0.00%\tElectronic technology",
          "No rating",
          "",
          "889",
          "Datronix Holdings Limited",
          "D",
          "124.8 M HKD\t0.340 HKD\t-12.82%\t486 K\t1.77\t—\t-0.06 HKD\t+52.54%\t0.00%\tElectronic technology",
          "No rating",
          "",
          "712",
          "Comtec Solar Systems Group Ltd.",
          "D",
          "59.36 M HKD\t0.056 HKD\t-6.67%\t420 K\t1.40\t—\t-0.04 HKD\t+5.56%\t0.00%\tElectronic technology",
          "No rating",
          "",
          "8286",
          "Shanxi Changcheng Microlight Equipment Co. Ltd. Class H",
          "D",
          "43.86 M HKD\t0.142 HKD\t+22.41%\t270 K\t1.55\t—\t-0.11 HKD\t+10.05%\t0.00%\tElectronic technology",
          "No rating"
        ].join("\n");

        function extractTickers(raw) {
          var lines = String(raw).replace(/\r/g, "").split("\n");
          var out = [];
          var seen = Object.create(null);
          for (var i = 0; i < lines.length; i++) {
            var cur = lines[i].trim();
            if (!TICKER_RE.test(cur)) continue;
            if (NOISE[cur]) continue;

            // Next non-empty line
            var j = i + 1;
            while (j < lines.length && !lines[j].trim()) j++;
            var next = j < lines.length ? lines[j].trim() : "";

            // Line after that
            var k = j + 1;
            while (k < lines.length && !lines[k].trim()) k++;
            var after = k < lines.length ? lines[k].trim() : "";

            // Confirm: next line looks like a company name (has lowercase),
            // or the next / next-next line is the "D" market marker.
            var looksLikeTicker =
              /[a-z]/.test(next) || next === "D" || after === "D";
            if (!looksLikeTicker) continue;

            if (dedupeBox.checked) {
              if (seen[cur]) continue;
              seen[cur] = 1;
            }
            out.push(cur);
          }
          return out;
        }

        function render() {
          var raw = inputEl.value;
          var list = extractTickers(raw);

          // A → Z lexicographic order (digits first, then letters)
          list.sort();
          if (descBox.checked) list.reverse();

          outputEl.value = tabbedBox.checked ? list.join("\t") : list.join("\n");

          if (!raw.trim()) {
            statsEl.textContent = "";
          } else if (list.length === 0) {
            statsEl.textContent = "no tickers detected";
          } else {
            statsEl.textContent =
              list.length + (list.length === 1 ? " ticker" : " tickers") +
              " · " + (descBox.checked ? "Z → A" : "A → Z");
          }
        }

        function copyToClipboard(text) {
          if (navigator.clipboard && window.isSecureContext) {
            return navigator.clipboard.writeText(text)
              .then(function () { return true; })
              .catch(function () { return legacyCopy(text); });
          }
          return Promise.resolve(legacyCopy(text));
        }
        function legacyCopy(text) {
          var ta = document.createElement("textarea");
          ta.value = text;
          ta.setAttribute("readonly", "");
          ta.style.position = "fixed";
          ta.style.top = "-1000px";
          ta.style.opacity = "0";
          document.body.appendChild(ta);
          ta.select();
          ta.setSelectionRange(0, ta.value.length);
          var ok = false;
          try { ok = document.execCommand("copy"); } catch (e) { ok = false; }
          document.body.removeChild(ta);
          return ok;
        }

        inputEl.addEventListener("input", render);
        dedupeBox.addEventListener("change", render);
        descBox.addEventListener("change", render);
        tabbedBox.addEventListener("change", render);

        copyBtn.addEventListener("click", function () {
          var text = outputEl.value.trim();
          if (!text) {
            Swal.fire(getToastConfig("warning", "Nothing to copy yet — paste some data first."));
            return;
          }
          copyToClipboard(text).then(function (ok) {
            Swal.fire(getToastConfig(
              ok ? "success" : "error",
              ok ? "Tickers copied! Paste them straight into your spreadsheet."
                 : "Copy failed — please select the output and copy manually."
            ));
          });
        });

        sampleBtn.addEventListener("click", function () {
          inputEl.value = SAMPLE;
          render();
          inputEl.focus();
        });

        clearBtn.addEventListener("click", function () {
          inputEl.value = "";
          outputEl.value = "";
          statsEl.textContent = "";
          inputEl.focus();
        });

        render();
      })();
    </script>
  </body>
</html>'''


@app.route("/")
def index():
    return render_template_string(HTML_PAGE)


@app.route("/proxy")
def proxy():
    symbol = request.args.get("symbol", "0700.HK")
    range_ = request.args.get("range", "10y")
    interval = request.args.get("interval", "1d")
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?range={range_}&interval={interval}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        resp = requests.get(url, headers=headers, timeout=15)
        return (resp.content, resp.status_code, {"Content-Type": "application/json"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    print("=" * 55)
    print("  Server Running")
    print("  Open:  http://localhost:5000")
    print("=" * 55)
    app.run(host="0.0.0.0", port=5000, debug=False)