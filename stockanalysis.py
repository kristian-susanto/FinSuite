from flask import Flask, request, jsonify, render_template_string
from werkzeug.serving import WSGIRequestHandler
import requests
import logging

logging.getLogger("werkzeug").setLevel(logging.ERROR)

class QuietRequestHandler(WSGIRequestHandler):
    def log_request(self, code="-", size="-"):
        pass
    def log_info(self, *args, **kwargs):
        pass
    def log(self, type, message, *args):
        pass

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
      header h1 .badge { font-size: 0.65em; font-weight: 700; background: var(--success); color: #fff;
        padding: 3px 10px; border-radius: 999px; margin-left: 8px; vertical-align: middle; letter-spacing: 0; }
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
      .btn-warning { background-color: #f59e0b; color: #ffffff; }
      .btn-warning:hover { opacity: 0.9; }
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
      .counter-header { display: flex; justify-content: space-between; align-items: center;
        gap: 10px; flex-wrap: wrap; border-bottom: 1px solid var(--border);
        padding-bottom: 0.5rem; margin-bottom: 1.2rem; }
      .counter-header h2 { border-bottom: none; padding-bottom: 0; margin-bottom: 0; }
      .counter-buttons { display: flex; gap: 6px; flex-wrap: wrap; }
      .counter-buttons .btn-action { padding: 6px 12px; font-size: 13px;
        font-weight: 700; min-width: 40px; line-height: 1.2; }
      .counter-buttons .btn-action.plus-btn { font-size: 20px; padding: 4px 14px; }
      @media (max-width: 380px) {
        .counter-buttons .btn-action { padding: 5px 9px; font-size: 12px; min-width: 34px; }
        .counter-buttons .btn-action.plus-btn { font-size: 17px; padding: 3px 10px; }
      }
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
      .converter-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 18px; }
      @media (max-width: 820px) { .converter-grid { grid-template-columns: 1fr; } }
      .panel { display: flex; flex-direction: column; min-width: 0; }
      .panel-head { display: flex; justify-content: space-between; align-items: baseline; gap: 10px; margin-bottom: 8px; }
      .panel-head label { font-weight: 600; font-size: 14px; color: var(--text-secondary); margin-bottom: 0; }
      .panel-meta { font-size: 12px; color: var(--text-secondary); text-align: right; }
      .ticker-card textarea { width: 100%; min-height: min(40vh, 300px); padding: 14px 16px;
        border: 2px solid var(--border); border-radius: 12px; background: var(--input-bg);
        color: var(--text-main); font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
        font-size: 14.5px; line-height: 1.7; resize: vertical; outline: none; }
      #tickerOutput { background: var(--output-bg); }
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
            <label class="radio-option"><input type="radio" name="source" value="stockanalysis" /> StockAnalysis</label>
          </div>
          <p class="source-note">
            <b>Package mode</b> opens a fixed bundle of <b>3 tabs</b>: Historical Data (Python yfinance), Income Statement, and Balance Sheet.
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
          <div class="counter-header">
            <h2>🖱️ Click Counter</h2>
            <div class="counter-buttons">
              <button class="btn-action btn-primary plus-btn" id="click-btn" title="Increment by 1">+</button>
              <button class="btn-action btn-warning" id="decrement-btn" title="Decrement by 1">−</button>
              <button class="btn-action btn-danger" id="reset-counter-btn" title="Reset counter">Reset</button>
            </div>
          </div>
          <div class="counter-display" id="counter-value">0</div>
        </section>
        <section class="card case-card">
          <h2>🔤 Text Case Converter</h2>
          <textarea id="textInput" placeholder="Type or paste alphanumeric string data records here..."></textarea>
          <div class="text-controls">
            <button onclick="transformText('upper')">UPPERCASE</button>
            <button onclick="transformText('lower')">lowercase</button>
            <button onclick="transformText('capitalize')">Capitalize Word</button>
            <button onclick="transformText('sentence')">Sentence case</button>
          </div>
          <div class="text-actions">
            <button class="btn-action btn-success" style="flex: 2" onclick="copyText()">Copy to Clipboard</button>
            <button class="btn-action btn-danger" style="flex: 1" onclick="clearText()">Clear</button>
          </div>
        </section>
      </div>

      <section class="card ticker-card">
        <h2>📋 Ticker Symbol Extractor</h2>
        <div class="converter-grid">
          <div class="panel">
            <div class="panel-head"><label for="tickerInput">Input — paste data</label><span class="panel-meta">auto-detects tickers</span></div>
            <textarea id="tickerInput" spellcheck="false" placeholder="Paste rows copied here…"></textarea>
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
        <p class="foot">Paste output containing standalone ticker lines <b>or</b> tab-separated rows (ticker in first column). The extractor detects standalone uppercase symbols (1–6 characters) and numeric ticker codes (1–6 digits), skips quote rows and market markers such as <b>D</b>, sorts them in strict A → Z / 0 → 9 order, and formats them for clean spreadsheet pasting. Use <b>one per line</b> for a column, or <b>tab-separated</b> for a single row.</p>
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
        { name: "Abu Dhabi Securities Exchange — United Arab Emirates", code: "ADX" },
        { name: "Aquis Exchange — United Kingdom", code: "AQUIS" },
        { name: "Athens Stock Exchange — Greece", code: "ATHEX" },
        { name: "Australian Securities Exchange — Australia", code: "ASX" },
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
        { name: "Canadian Securities Exchange — Canada", code: "CSE" },
        { name: "Casablanca Stock Exchange — Morocco", code: "CSEMA" },
        { name: "Cboe Canada (NEO) — Canada", code: "NEO" },
        { name: "China Financial Futures Exchange — Mainland China", code: "CFFEX" },
        { name: "Colombo Stock Exchange — Sri Lanka", code: "CSELK" },
        { name: "Cyprus Stock Exchange — Cyprus", code: "CSECY" },
        { name: "Dhaka Stock Exchange — Bangladesh", code: "DSEBD" },
        { name: "Dubai Financial Market — United Arab Emirates", code: "DFM" },
        { name: "Düsseldorf Stock Exchange — Germany", code: "DUS" },
        { name: "Egyptian Exchange — Egypt", code: "EGX" },
        { name: "Euronext Amsterdam — Netherlands", code: "EURONEXTAMS" },
        { name: "Euronext Brussels — Belgium", code: "EURONEXTBRU" },
        { name: "Euronext Dublin — Ireland", code: "EURONEXTDUB" },
        { name: "Euronext Lisbon — Portugal", code: "EURONEXTLIS" },
        { name: "Euronext Oslo — Norway", code: "EURONEXTOSE" },
        { name: "Euronext Paris — France", code: "EURONEXTPAR" },
        { name: "EuroTLX — Italy", code: "EUROTLX" },
        { name: "Frankfurt Stock Exchange — Germany", code: "FWB" },
        { name: "Fukuoka Stock Exchange — Japan", code: "FSE" },
        { name: "Hamburg Stock Exchange — Germany", code: "HAM" },
        { name: "Hanoi Stock Exchange — Vietnam", code: "HNX" },
        { name: "Hanover Stock Exchange — Germany", code: "HAN" },
        { name: "Ho Chi Minh Stock Exchange — Vietnam", code: "HOSE" },
        { name: "Hong Kong Stock Exchange — Hong Kong", code: "HKEX" },
        { name: "Indonesia Stock Exchange — Indonesia", code: "IDX" },
        { name: "Johannesburg Stock Exchange — South Africa", code: "JSE" },
        { name: "Korea Exchange — South Korea", code: "KRX" },
        { name: "Lang & Schwarz — Germany", code: "LS" },
        { name: "Ljubljana Stock Exchange — Slovenia", code: "LJSE" },
        { name: "London Stock Exchange — United Kingdom", code: "LSE" },
        { name: "LS Exchange — Germany", code: "LSX" },
        { name: "LSE International — United Kingdom", code: "LSIN" },
        { name: "Luxembourg Stock Exchange — Luxembourg", code: "LUXSE" },
        { name: "Moscow Exchange — Russia", code: "RUS" },
        { name: "Munich Stock Exchange — Germany", code: "MUN" },
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
        { name: "OTC Markets — United States", code: "OTC" },
        { name: "Pakistan Stock Exchange — Pakistan", code: "PSX" },
        { name: "Philippine Stock Exchange — Philippines", code: "PSE" },
        { name: "Prague Stock Exchange — Czech Republic", code: "PSECZ" },
        { name: "Qatar Stock Exchange — Qatar", code: "QSE" },
        { name: "Sapporo Securities Exchange — Japan", code: "SAPSE" },
        { name: "Saudi Stock Exchange (Tadawul) — Saudi Arabia", code: "TADAWUL" },
        { name: "Shanghai Futures Exchange — Mainland China", code: "SHFE" },
        { name: "Shanghai Stock Exchange — Mainland China", code: "SSE" },
        { name: "Shenzhen Stock Exchange — Mainland China", code: "SZSE" },
        { name: "Singapore Exchange — Singapore", code: "SGX" },
        { name: "SIX Swiss Exchange — Switzerland", code: "SIX" },
        { name: "Stock Exchange of Thailand — Thailand", code: "SET" },
        { name: "Stuttgart Stock Exchange — Germany", code: "SWB" },
        { name: "Taipei Exchange — Taiwan", code: "TPEX" },
        { name: "Taiwan Stock Exchange — Taiwan", code: "TWSE" },
        { name: "Tel Aviv Stock Exchange — Israel", code: "TASE" },
        { name: "Tokyo Stock Exchange — Japan", code: "TSE" },
        { name: "Toronto Stock Exchange — Canada", code: "TSX" },
        { name: "Tradegate — Germany", code: "TRADEGATE" },
        { name: "TSX Venture Exchange — Canada", code: "TSXV" },
        { name: "UPCoM — Vietnam", code: "UPCOM" },
        { name: "Vienna Stock Exchange — Austria", code: "VIE" },
        { name: "Warsaw Stock Exchange — Poland", code: "GPW" },
        { name: "Xetra — Germany", code: "XETR" },
        { name: "Zagreb Stock Exchange — Croatia", code: "ZSE" },
        { name: "Zhengzhou Commodity Exchange — Mainland China", code: "ZCE" },
      ];

      const YAHOO_SUFFIX_MAP = {
        ADX: ".AE", AQUIS: ".L", ASX: ".AX", ATHEX: ".AT",
        BAHRAIN: ".BH", BCBA: ".BA", BCS: ".SN", BELEX: ".BE",
        BET: ".BD", BIST: ".IS", BIVA: ".MX", BME: ".MC",
        BMFBOVESPA: ".SA", BMV: ".MX", BSE: ".BO", BSESOF: ".SO",
        BSSE: ".BS", BVC: ".CL", BVCV: ".CC", BVL: ".LM",
        BVB: ".RO", BYMA: ".BA",
        CSECY: ".CY", CSE: ".CN", CSEMA: ".MA", CSELK: ".CM",
        DFM: ".AE", DUS: ".DU", DSEBD: ".BD",
        EGX: ".CA", EURONEXTAMS: ".AS", EURONEXTBRU: ".BR",
        EURONEXTOSE: ".OL", EURONEXTPAR: ".PA", EURONEXTDUB: ".IR",
        EURONEXTLIS: ".LS", EUROTLX: ".MI",
        FSE: ".F", FWB: ".F", GPW: ".WA",
        HAM: ".HM", HAN: ".HA", HNX: ".VN", HKEX: ".HK", HOSE: ".VN",
        IDX: ".JK", JSE: ".JO", KRX: ".KS", KSE: ".KW",
        LJSE: ".LJ", LSE: ".L", LS: ".LS", LSIN: ".L",
        LSX: ".LS", LUXSE: ".LU",
        MIL: ".MI", MUN: ".MU", MYX: ".KL",
        NAG: ".N", NASDAQ: "", NASDAQDUBAI: ".AE",
        NEWCONNECT: ".WA", NEO: ".NE", NGM: ".ST",
        NSE: ".NS", NSEKE: ".NR", NSENG: ".LG", NZX: ".NZ",
        OMXCOP: ".CO", OMXHEX: ".HE", OMXICE: ".IC",
        OMXRSE: ".RG", OMXSTO: ".ST", OMXTSE: ".TL",
        OMXVSE: ".VS", OTC: "",
        PSECZ: ".PR", PSE: ".PS", PSX: ".KA", QSE: ".QA",
        RUS: ".ME",
        SAPSE: ".S", SET: ".BK", SGX: ".SI", SIX: ".SW",
        SSE: ".SS", SWB: ".SG", SZSE: ".SZ",
        TADAWUL: ".SR", TASE: ".TA", TRADEGATE: ".TG",
        TSX: ".TO", TSXV: ".V", TPEX: ".TWO", TSE: ".T", TWSE: ".TW",
        UPCOM: ".VN", VIE: ".VI", XETR: ".DE", ZSE: ".ZG",
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
        ADX: "ADX", AQUIS: "AQU", ASX: "ASX", ATHEX: "ATH",
        BAHRAIN: "BAX", BCBA: "BCBA", BELEX: "BELEX", BET: "BUD",
        BIST: "IST", BME: "BME", BMFBOVESPA: "BVMF", BMV: "BMV",
        BSE: "BOM", BSESOF: "BUL", BSSE: "BSSE", BVC: "BVC",
        BVCV: "CCSE", BVL: "BVL", BYMA: "BCBA", BVB: "BVB",
        CSE: "CSE", CSECY: "CYS", CSEMA: "CBSE", CSELK: "COSE",
        DFM: "DFM", DSEBD: "DSE", DUS: "DUSE",
        EGX: "EGX", EURONEXTAMS: "AMS", EURONEXTBRU: "EBR",
        EURONEXTDUB: "ISE", EURONEXTLIS: "ELI", EURONEXTOSE: "OSL",
        EURONEXTPAR: "EPA", EUROTLX: "BIT",
        FSE: "FKSE", FWB: "FRA", GPW: "WSE",
        HAM: "HAM", HAN: "HAM", HNX: "HNX", HKEX: "HKG", HOSE: "HOSE",
        IDX: "IDX", JSE: "JSE", KRX: "KRX", KSE: "KWSE",
        LJSE: "LJSE", LS: "FRA", LSE: "LON", LSIN: "LON",
        LSX: "FRA", LUXSE: "LUX",
        MIL: "BIT", MUN: "MUN", MYX: "KLSE",
        NAG: "XNGO", NASDAQ: "NASDAQ", NASDAQDUBAI: "DFM",
        NEO: "NEO", NEWCONNECT: "WSE", NGM: "NGM",
        NSE: "NSE", NSEKE: "NASE", NSENG: "NGX", NZX: "NZE",
        OMXCOP: "CPH", OMXHEX: "HEL", OMXICE: "ICE",
        OMXRSE: "RSE", OMXSTO: "STO", OMXTSE: "TAL",
        OMXVSE: "VSE", OTC: "OTC",
        PSECZ: "PRA", PSE: "PSE", PSX: "PSX", QSE: "QSE",
        RUS: "MOEX",
        SAPSE: "SPSE", SET: "BKK", SGX: "SGX", SIX: "SWX",
        SSE: "SHA", SWB: "BST", SZSE: "SHE",
        TADAWUL: "TADAWUL", TASE: "TLV", TRADEGATE: "FRA",
        TSX: "TSX", TSXV: "TSXV", TSE: "TYO", TPEX: "TPEX", TWSE: "TPE",
        UPCOM: "HNX", VIE: "VIE", XETR: "ETR", ZSE: "ZSE",
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
        if (tv === "HKEX" && /^\d{1,3}$/.test(tk)) {
          tk = tk.padStart(4, "0");
        }
        const usExchanges = ["otc", "nasdaq", "nyse", "amex"];
        return usExchanges.includes(ex)
          ? `https://www.stockanalysis.com/stocks/${tk}`
          : `https://www.stockanalysis.com/quote/${ex}/${tk}`;
      }

      function buildPackageTargets(exchangeCode, ticker, isSemester) {
        const period = "quarterly";
        const baseUrl = saBaseUrl(exchangeCode, ticker);
        return [
          { id: "pkg-history-py", name: "⏳ Historical Data — Python (yfinance quarterly / semiannual closes)", url: "local", local: true },
          { id: "pkg-income-sa", name: "📑 Income Statement — StockAnalysis", url: `${baseUrl}/financials/income-statement/?p=${period}` },
          { id: "pkg-balance-sa", name: "⚖️ Balance Sheet — StockAnalysis", url: `${baseUrl}/financials/balance-sheet/?p=${period}` }
        ];
      }

      function buildStockAnalysisTargets(exchangeCode, ticker) {
        const baseUrl = saBaseUrl(exchangeCode, ticker);
        return [
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
        tickerInput.value = tickerInput.value.toUpperCase();
      }
      radioButtons.forEach((r) => r.addEventListener("change", updateSourceUI));

      function toggleAllCheckboxes(selectAll) {
        if (getSelectedSource().includes("package")) return;
        checkboxGrid.querySelectorAll('input[type="checkbox"]').forEach((cb) => (cb.checked = selectAll));
      }

      function openHistoryTab(exchangeCode, ticker, initialFreq) {
        const suffix = YAHOO_SUFFIX_MAP[exchangeCode.toUpperCase()] || "";
        let baseTicker = ticker.toUpperCase();
        if (exchangeCode.toUpperCase() === "HKEX") {
          baseTicker = baseTicker.replace(/^0+/, '') || '0';
        }
        const symbol = baseTicker + suffix;
        const freq = (initialFreq === "semiannual") ? "semiannual" : "quarterly";
        window.open(`/history/${symbol}?freq=${freq}`, "_blank");
      }

      function processSearch() {
        const rawExchange = exchangeInput.value.trim();
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
          const allTargets = buildStockAnalysisTargets(exchangeCode, ticker);
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
            else { window.open(item.url, "_blank", "noopener"); }
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
          return;
        }
        count--;
        counterDisplay.textContent = count;
        counterDisplay.style.transform = "scale(0.85)";
        setTimeout(() => { counterDisplay.style.transform = "scale(1)"; }, 100);
      });

      window.addEventListener("keydown", (e) => {
        const key = (e.key || "").toLowerCase();
        const hasModifier = e.ctrlKey || e.metaKey;
        const isRefreshCombo = (hasModifier && key === "r") || e.key === "F5" || key === "f5";
        if (isRefreshCombo) {
          e.preventDefault();
          e.stopPropagation();
          Swal.fire(getToastConfig("info", "Page refresh shortcuts are disabled to keep your counter and workspace state stable."));
          return false;
        }
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
        var inputEl = document.getElementById("tickerInput");
        var outputEl = document.getElementById("tickerOutput");
        var statsEl = document.getElementById("tickerStats");
        var copyBtn = document.getElementById("tickerCopyBtn");
        var sampleBtn = document.getElementById("tickerSampleBtn");
        var clearBtn = document.getElementById("tickerClearBtn");
        var dedupeBox = document.getElementById("tickerDedupe");
        var descBox = document.getElementById("tickerDesc");
        var tabbedBox = document.getElementById("tickerTabbed");

        var TICKER_RE = /^([A-Z][A-Z0-9]{0,5}|\d{1,6})$/;

        function isDataRow(s) {
          if (!s) return false;
          if (s.indexOf("\t") !== -1) return true;
          if (/\d/.test(s) && /%/.test(s)) return true;
          return /\d/.test(s) && /\b(?:HKD|USD|EUR|GBP|JPY|CNY|RMB|TWD|KRW|SGD|AUD|CAD|CHF)\b/.test(s);
        }

        var NOISE = {
          TTM: 1, EPS: 1, YOY: 1, QOQ: 1, ETF: 1, IPO: 1, CEO: 1, CFO: 1,
          ROE: 1, ROA: 1, ROI: 1, NAV: 1, ALL: 1, NONE: 1, NA: 1,
          DR: 1, ADR: 1, GDR: 1, IDR: 1, CDR: 1, EDR: 1, DDR: 1
        };

        var SAMPLE = `General
Filters 1
Charts New
Performance
Analysts
Dividends
Financials
Valuation
Add View
Edit View
Symbol	Company Name	Market Cap
	Stock Price 	% Change 	Industry 	Volume 	PE Ratio
0390	China Railway Group Limited	115.37B	2.930	-0.34%	Engineering & Construction	17,834,000	3.86
3996	China Energy Engineering Corporation Limited	101.81B	0.905	0.56%	Engineering & Construction	8,521,958	6.39
1800	China Communications Construction Company Limited	97.15B	3.180	-0.31%	Engineering & Construction	7,365,043	4.49
1186	China Railway Construction Corporation Limited	88.02B	3.940	-0.76%	Engineering & Construction	5,287,500	4.63
1618	Metallurgical Corporation of China Ltd.	56.57B	1.295	-0.38%	Engineering & Construction	5,644,834	-
3311	China State Construction International Holdings Limited	46.17B	8.74	0.98%	Engineering & Construction	2,114,000	5.22
0659	CTF Services Limited	43.93B	8.75	-1.46%	Engineering & Construction	4,564,732	16.82
2386	SINOPEC Engineering (Group) Co., Ltd.	25.27B	5.75	1.23%	Engineering & Construction	3,921,000	14.17
9900	Hong Kong Zcloud Technology Construction Limited	16.44B	5.53	1.84%	Engineering & Construction	2,964,000	2,359.09
3928	China Next-Gen Commerce and Supply Chain Limited	14.12B	28.46	-0.14%	Engineering & Construction	355,000	-
2068	China Aluminum International Engineering Corporation Limited	12.52B	1.465	-0.34%	Engineering & Construction	4,900,000	38.18
1783	Envision Greenwise Holdings Limited	10.47B	3.480	0.29%	Engineering & Construction	9,654,000	160.37
1757	Global Chinese Business Club	6.78B	5.65	7.62%	Engineering & Construction	15,000	614.40
1489	Wisewin Innotech Group Limited	3.17B	3.165	-10.47%	Engineering & Construction	1,090,000	-
0368	Superland Group Holdings Limited	3.15B	3.940	-3.31%	Engineering & Construction	100,000	112.94
2520	Shanxi Installation Group Co., Ltd.	3.01B	2.190	-0.23%	Engineering & Construction	64,000	18.64
9929	Yaopop Holdings Limited	2.82B	1.410	-3.09%	Engineering & Construction	710,000	-
0331	FSE Lifestyle Services Limited	2.42B	5.37	-0.37%	Engineering & Construction	11,000	5.90
9913	Chi Kan Holdings Limited	2.12B	2.115	-1.63%	Engineering & Construction	36,000	-
2295	Maxicity Holdings Limited	2.04B	5.10	0.79%	Engineering & Construction	15,000	147.43
0240	Build King Holdings Limited	1.80B	1.450	-1.69%	Engineering & Construction	180,000	3.90
1826	FDB Holdings Limited	1.56B	0.650	-9.09%	Engineering & Construction	5,105,000	-
6063	Lotus Horizon Holdings Limited	1.53B	0.765	2.00%	Engineering & Construction	2,992,000	-
1953	SFQ Global Limited	1.53B	1.035	-1.43%	Engineering & Construction	1,785,000	59.32
2355	Baoye Group Company Limited	1.50B	2.880	1.23%	Engineering & Construction	20,000	16.78
1656	ISDN Holdings Limited	1.47B	3.945	0.00%	Engineering & Construction	-	18.53
2236	Wison Engineering Services Co. Ltd.	1.47B	0.360	0.00%	Engineering & Construction	22,000	13.98
1283	Accel Group Holdings Limited	1.45B	1.770	1.43%	Engineering & Construction	300,000	32.48
1793	Wecon Holdings Limited	1.38B	1.720	-12.24%	Engineering & Construction	2,556,000	144.30
2515	Tianjin Construction Development Group Co., Ltd.	1.35B	4.350	-1.14%	Engineering & Construction	1,042,000	-
1568	Sundart Holdings Limited	1.31B	0.600	-0.83%	Engineering & Construction	156,000	4.58
0830	China State Construction Development Holdings Limited	1.27B	0.565	-4.24%	Engineering & Construction	104,000	-
1977	Analogue Holdings Limited	1.25B	0.895	1.13%	Engineering & Construction	10,000	5.26
1599	Beijing Urban Construction Design & Development Group Co., Limited	1.21B	0.900	0.56%	Engineering & Construction	114,000	2.22
0687	Tysan Holdings Limited	1.06B	0.315	0.00%	Engineering & Construction	100,000	22.85
9639	Wing Lee Development Construction Holdings Limited	1.05B	1.050	-7.08%	Engineering & Construction	355,000	56.99
1372	China Carbon Neutral Development Group Limited	1.00B	1.025	-1.91%	Engineering & Construction	943,000	-
6829	Dragon Rise Group Holdings Limited	920.16M	3.195	-0.16%	Engineering & Construction	452,000	58.78
2789	Yuanda China Holdings Limited	906.48M	0.146	-2.01%	Engineering & Construction	62,000	2.55
1903	JBB Builders International Limited	875.00M	1.750	-1.69%	Engineering & Construction	38,000	-
2503	Zhongshen Jianye Holding Limited	817.02M	0.238	0.00%	Engineering & Construction	296,000	-
0711	Asia Allied Infrastructure Holdings Limited	786.46M	0.430	0.00%	Engineering & Construction	190,000	6.03
0610	Wai Kee Holdings Limited	713.81M	0.900	-0.55%	Engineering & Construction	60,000	0.93
1500	In Construction Holdings Limited	697.20M	0.840	-1.18%	Engineering & Construction	7,045,000	10.75
8321	Tai Kam Holdings Limited	683.91M	1.275	0.00%	Engineering & Construction	-	15.68
1627	Able Engineering Holdings Limited	650.00M	0.325	1.56%	Engineering & Construction	20,000	2.26
0611	China Nuclear Energy Technology Corporation Limited	620.43M	0.335	0.00%	Engineering & Construction	154,000	4.00
1865	Pengo Holdings Group Limited	588.16M	0.410	-1.20%	Engineering & Construction	11,449,200	-
6038	G & M Holdings Limited	576.73M	0.575	0.88%	Engineering & Construction	4,610,000	14.77
1499	OKG Technology Holdings Limited	558.53M	0.104	-2.80%	Engineering & Construction	1,450,000	-
6182	Twintek Investment Holdings Limited	548.00M	0.685	-9.87%	Engineering & Construction	38,288,000	-
8188	GME Group Holdings Limited	481.45M	1.010	-0.49%	Engineering & Construction	684,000	6.74
1746	Man Shun Group (Holdings) Limited	470.00M	0.470	-2.08%	Engineering & Construction	708,000	-
2863	Golden Faith Group Holdings Limited	448.18M	0.650	-0.76%	Engineering & Construction	60,000	-
9998	Kwan Yong Holdings Limited	428.00M	0.535	-6.14%	Engineering & Construction	1,880,000	3.57
2663	KPa-BM Holdings Limited	423.27M	0.760	18.75%	Engineering & Construction	6,450,000	33.16
0994	CT Vision (International) Holdings Limited	400.21M	0.310	-4.62%	Engineering & Construction	2,744,000	-
1751	AI Energy Engineering Holdings Limited	389.33M	0.955	-0.52%	Engineering & Construction	218,000	-
8431	Hao Bai International (Cayman) Limited	382.05M	1.615	-0.62%	Engineering & Construction	1,640,000	-
2262	Steve Leung Design Group Limited	370.96M	0.325	0.00%	Engineering & Construction	-	31.25
1556	Chinney Kin Wing Holdings Limited	355.50M	0.237	0.00%	Engineering & Construction	-	3.04
1727	Hebei Construction Group Corporation Limited	350.52M	0.199	-0.50%	Engineering & Construction	75,500	-
2017	Chanhigh Holdings Limited	346.36M	0.560	-3.45%	Engineering & Construction	36,000	54.80
1416	CTR Holdings Limited	341.00M	0.220	-0.90%	Engineering & Construction	320,000	2.72
1693	BGMC International Limited	321.11M	4.000	0.00%	Engineering & Construction	2,800	-
1420	Chuan Holdings Limited	320.89M	0.239	0.00%	Engineering & Construction	12,000	1.47
1637	SH Group (Holdings) Limited	318.00M	0.795	-0.63%	Engineering & Construction	76,000	53.08
1667	Dimmi Life Holdings Limited	316.80M	0.330	-8.33%	Engineering & Construction	100,000	-
0896	Hanison Construction Holdings Limited	300.46M	0.280	-1.75%	Engineering & Construction	270,000	-
2163	Changsha Broad Homes Industrial Group Co., Ltd.	292.58M	0.600	-4.76%	Engineering & Construction	623,700	-
3789	Royal Deluxe Holdings Limited	288.00M	0.240	0.00%	Engineering & Construction	100,000	19.71
1630	Kin Shing Holdings Limited	285.00M	0.190	2.70%	Engineering & Construction	234,000	165.36
1780	Rongzun International Holdings Group Limited	279.00M	0.450	2.27%	Engineering & Construction	777,500	-
1742	HPC Holdings Limited	272.00M	0.170	-1.16%	Engineering & Construction	5,000	3.07
2227	Solis Holdings Limited	270.10M	0.295	9.26%	Engineering & Construction	8,000	2.18
1726	HKE Holdings Limited	268.31M	0.235	7.80%	Engineering & Construction	15,000	-
8610	BBSB International Limited	265.00M	0.530	-0.93%	Engineering & Construction	8,000	14.99
0784	AiLife International Group Limited	264.00M	0.330	0.00%	Engineering & Construction	480,000	-
1615	AB Builders Group Limited	264.00M	0.440	-6.38%	Engineering & Construction	275,000	133.78
8629	Guangdong Syntrust GK Testing and Certification Tech Service Center Co., Ltd.	261.25M	7.70	0.00%	Engineering & Construction	-	10.24
1301	D&G Technology Holding Company Limited	260.20M	0.415	-2.35%	Engineering & Construction	38,000	-
1662	Yee Hop Holdings Limited	257.50M	0.500	3.09%	Engineering & Construction	6,000	8.46
2132	Landrich Holding Limited	251.20M	0.157	-5.42%	Engineering & Construction	80,000	19.88
1240	CNQC International Holdings Limited	244.84M	0.149	-10.78%	Engineering & Construction	57,500	3.43
8535	Vistar Holdings Limited	242.40M	0.202	-0.98%	Engineering & Construction	40,000	161.34
1429	Skymission Group Holdings Limited	241.92M	0.126	-0.79%	Engineering & Construction	2,840,000	-
1987	Beng Soon Machinery Holdings Limited	240.00M	0.240	0.00%	Engineering & Construction	40,000	42.18
1552	BHCC Holding Limited	224.00M	0.280	-5.08%	Engineering & Construction	180,000	3.75
1920	Junwea Group (China) Company Limited	223.29M	0.380	2.70%	Engineering & Construction	20,000	-
1690	Lap Kei Engineering (Holdings) Limited	222.57M	0.154	4.05%	Engineering & Construction	90,000	10.86
0983	SOCAM Development Limited	222.14M	0.595	6.25%	Engineering & Construction	134,000	10.57
1582	CR Construction Group Holdings Limited	220.00M	0.440	0.00%	Engineering & Construction	17,500	16.74
1447	SFK Construction Holdings Limited	212.00M	0.530	-1.85%	Engineering & Construction	214,000	9.01
8601	Boltek Holdings Limited	208.00M	0.260	0.00%	Engineering & Construction	220,000	10.56
1408	Macau E&M Holding Limited	197.50M	0.395	1.28%	Engineering & Construction	2,000	163.63
0406	Yau Lee Holdings Limited	197.12M	0.450	0.00%	Engineering & Construction	-	-
1683	Hope Life International Holdings Limited	195.96M	0.105	0.00%	Engineering & Construction	624,000	-
1633	Sheung Yue Group Holdings Limited	195.15M	0.285	0.00%	Engineering & Construction	591,000	-
1486	C Cheng Holdings Limited	194.58M	0.450	13.92%	Engineering & Construction	294,000	-
8023	Kwong Man Kee Group Limited	194.17M	0.325	-1.52%	Engineering & Construction	150,000	14.05
1547	IBI Group Holdings Limited	191.20M	0.239	0.00%	Engineering & Construction	-	14.10
8316	SwiftLife Holdings Limited	189.72M	0.199	2.05%	Engineering & Construction	28,000	8.03
1557	K. H. Group Holdings Limited	189.60M	0.395	0.00%	Engineering & Construction	68,000	1.37
2193	Man King Holdings Limited	176.23M	0.420	1.20%	Engineering & Construction	100,000	22.12
2266	Lai Si Enterprise Holding Limited	176.00M	0.440	-1.12%	Engineering & Construction	122,000	-
6816	Prosper Construction Holdings Limited	176.00M	0.220	0.00%	Engineering & Construction	-	-
8305	Sheng Tang Holdings Limited	168.69M	0.104	-7.96%	Engineering & Construction	2,220,000	-
1870	Green Power Group Limited	152.58M	0.150	1.35%	Engineering & Construction	1,515,000	-
1559	Kwan On Holdings Limited	151.50M	0.0550	0.00%	Engineering & Construction	10,000	-
8040	Coolpoint Innonism Holding Limited	147.90M	0.435	6.10%	Engineering & Construction	10,000	-
0385	Chinney Alliance Group Limited	143.37M	0.241	0.00%	Engineering & Construction	81,000	-
1718	Wan Kei Group Holdings Limited	142.95M	0.475	13.10%	Engineering & Construction	311,000	-
8411	K W Nelson Interior Design and Contracting Group Limited	142.56M	0.150	0.00%	Engineering & Construction	270,000	18.24
2221	New Concepts Holdings Limited	134.14M	0.585	-0.85%	Engineering & Construction	16,000	-
6080	Wing Chi Holdings Limited	133.32M	0.119	-0.83%	Engineering & Construction	240,000	-
2340	ISP Holdings Limited	127.71M	0.167	1.21%	Engineering & Construction	104,000	-
1343	Wei Yuan Holdings Limited	112.78M	0.106	3.92%	Engineering & Construction	205,000	2.32
8125	RJVAN Holdings Limited	112.70M	0.520	0.00%	Engineering & Construction	32,000	-
1722	Kin Pang Holdings Limited	108.90M	0.0990	-2.94%	Engineering & Construction	560,000	-
1741	Shing Chi Holdings Limited	108.80M	0.136	0.00%	Engineering & Construction	-	-
1253	China Green Broad Ecological Technology Company Limited	100.89M	0.167	-4.57%	Engineering & Construction	204,000	-
8460	Basetrophy Group Holdings Limited	99.60M	0.375	1.35%	Engineering & Construction	800,000	-
1855	ZONQING Environmental Limited	99.00M	0.120	-6.98%	Engineering & Construction	330,000	-
1459	Jujiang Construction Group Co., Ltd.	98.67M	0.185	0.00%	Engineering & Construction	212,000	-
1376	Raffles Interior Limited	96.00M	0.0960	3.23%	Engineering & Construction	544,000	-
3822	Sam Woo Construction Group Limited	92.40M	1.100	0.00%	Engineering & Construction	4,000	1.62
1546	Fortune Peace Development Group Limited	88.80M	0.111	-4.31%	Engineering & Construction	896,000	-
8616	Sunray Engineering Group Limited	88.00M	0.0880	1.15%	Engineering & Construction	1,000,000	20.81
8208	Radiance Global Group Holdings Limited	87.12M	0.110	0.00%	Engineering & Construction	276,000	-
1472	Sang Hing Holdings (International) Limited	87.00M	0.0870	-2.25%	Engineering & Construction	20,000	-
3878	Vicon Holdings Limited	82.01M	0.171	-1.72%	Engineering & Construction	148,000	18.21
8275	China New Consumption Group Limited	81.60M	0.0850	-4.49%	Engineering & Construction	40,000	-
0498	Blue River Holdings Limited	73.91M	0.0710	0.00%	Engineering & Construction	690,000	1.44
0871	China Dredging Environment Protection Holdings Limited	72.19M	0.0480	-7.69%	Engineering & Construction	55,000	-
8360	Basic House New Life Group Limited	72.05M	0.200	-3.85%	Engineering & Construction	24,000	-
1707	Geotech Holdings Ltd.	70.56M	0.0420	5.00%	Engineering & Construction	112,000	-
1413	FEG Holdings Corporation Limited	69.86M	0.213	-5.33%	Engineering & Construction	519,000	-
1647	Grandshores Technology Group Limited	69.31M	0.0580	3.57%	Engineering & Construction	475,000	-
8549	Golden Leaf International Group Limited	68.80M	0.172	-0.58%	Engineering & Construction	60,000	-
1591	Shun Wo Group Holdings Limited	64.53M	0.121	0.00%	Engineering & Construction	210,000	-
8516	Zhong Ying International Group Limited	63.88M	1.110	2.30%	Engineering & Construction	215,000	-
8445	Noble Engineering Group Holdings Limited	63.01M	0.190	-7.32%	Engineering & Construction	20,000	-
3728	Ching Lee Holdings Limited	58.75M	0.0580	-3.33%	Engineering & Construction	120,000	8.41
3321	ZhongKe Group Holdings Limited	55.53M	0.715	1.42%	Engineering & Construction	800,000	-
8373	Indigo Star Holdings Limited	46.20M	0.850	7.59%	Engineering & Construction	50,000	1.49
8422	WT Group Holdings Limited	40.32M	0.112	-0.88%	Engineering & Construction	270,000	-
1802	Wenye Group Holdings Limited	37.42M	0.0450	0.00%	Engineering & Construction	-	-
8423	Chi Ho Development Holdings Limited	36.80M	0.0460	0.00%	Engineering & Construction	-	-
8268	Smart City Development Holdings Limited	35.14M	0.122	-3.17%	Engineering & Construction	2,448,000	-
8262	Super Strong Holdings Limited	34.16M	0.0370	0.00%	Engineering & Construction	-	-
8366	Zhejiang United Investment Holdings Group Limited	33.12M	0.420	0.00%	Engineering & Construction	-	-
2433	Zhongtian Construction (Hunan) Group Limited	32.26M	0.0560	5.66%	Engineering & Construction	882,000	-
2110	Tian Cheng Holdings Limited	30.46M	0.705	3.68%	Engineering & Construction	53,000	-
2113	Century Group International Holdings Limited	29.21M	0.605	1.68%	Engineering & Construction	202,500	-
2195	Unity Enterprise Holdings Limited	28.42M	0.168	-5.08%	Engineering & Construction	154,500	-
8217	Ju Fu Tang Biotech Holdings Co., Ltd	27.17M	0.0900	0.00%	Engineering & Construction	990,000	1.18
8572	Glory Flame Holdings Limited	26.78M	0.590	0.00%	Engineering & Construction	-	-
8619	NIU Holdings Limited	26.45M	0.0610	-3.17%	Engineering & Construction	1,039,200	-
8128	Sino Energy Conservation International Limited	24.22M	0.0540	-10.00%	Engineering & Construction	479,800	12.37
8059	Glory Flame Holdings Limited	22.74M	0.450	-10.89%	Engineering & Construction	10,000	-
8356	Tsun Yip Holdings Limited	20.97M	0.280	1.82%	Engineering & Construction	2,000	2.31
6189	Guangdong Adway Construction (Group) Holdings Company Limited	17.35M	0.0720	-10.00%	Engineering & Construction	4,499,500	-
8532	Polyfair Holdings Limited	3.73M	0.0440	-6.38%	Engineering & Construction	528,000	-`.trim();

        function extractTickers(raw) {
          var lines = String(raw).replace(/\r/g, "").split("\n");
          var out = [];
          var seen = Object.create(null);

          for (var i = 0; i < lines.length; i++) {
            var line = lines[i];
            var cur = line.trim();
            if (!cur) continue;

            // Mode 1: tab-separated row — ticker in first column
            if (line.indexOf("\t") !== -1) {
              var fields = line.split("\t");
              var firstField = (fields[0] || "").trim();
              if (!TICKER_RE.test(firstField)) continue;
              if (NOISE[firstField]) continue;
              var hasData = false;
              for (var f = 1; f < fields.length; f++) {
                if (/\d/.test(fields[f])) { hasData = true; break; }
              }
              var secondField = fields.length > 1 ? fields[1].trim() : "";
              var isCompany = /[a-z]/.test(secondField) || secondField === "D";
              if (!hasData || !isCompany) continue;
              if (dedupeBox.checked) {
                if (seen[firstField]) continue;
                seen[firstField] = 1;
              }
              out.push(firstField);
              continue;
            }

            // Mode 2: line-by-line — ticker on its own line
            if (!TICKER_RE.test(cur)) continue;
            if (NOISE[cur]) continue;
            var j = i + 1;
            while (j < lines.length && !lines[j].trim()) j++;
            var next = j < lines.length ? lines[j].trim() : "";
            var k = j + 1;
            while (k < lines.length && !lines[k].trim()) k++;
            var after = k < lines.length ? lines[k].trim() : "";
            var looksLikeTicker = !isDataRow(next) && (/[a-z]/.test(next) || next === "D" || after === "D");
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
          list.sort();
          if (descBox.checked) list.reverse();
          outputEl.value = tabbedBox.checked ? list.join("\t") : list.join("\n");
          if (!raw.trim()) { statsEl.textContent = ""; }
          else if (list.length === 0) { statsEl.textContent = "no tickers detected"; }
          else { statsEl.textContent = list.length + (list.length === 1 ? " ticker" : " tickers") + " · " + (descBox.checked ? "Z → A" : "A → Z"); }
        }

        function copyToClipboard(text) {
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
        dedupeBox.addEventListener("change", render);
        descBox.addEventListener("change", render);
        tabbedBox.addEventListener("change", render);

        copyBtn.addEventListener("click", function () {
          var text = outputEl.value.trim();
          if (!text) { Swal.fire(getToastConfig("warning", "Nothing to copy yet — paste some data first.")); return; }
          copyToClipboard(text).then(function (ok) {
            Swal.fire(getToastConfig(ok ? "success" : "error", ok ? "Tickers copied! Paste them straight into your spreadsheet." : "Copy failed — please select the output and copy manually."));
          });
        });

        sampleBtn.addEventListener("click", function () { inputEl.value = SAMPLE; render(); inputEl.focus(); });
        clearBtn.addEventListener("click", function () { inputEl.value = ""; outputEl.value = ""; statsEl.textContent = ""; inputEl.focus(); });
        render();
      })();
    </script>
  </body>
</html>'''

HISTORY_PAGE = r'''<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{{ symbol }} — Historical Data</title>
    <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>📊</text></svg>" />
    <script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>
    <style>
      :root{
        --bg:#f1f5f9; --card:#ffffff; --text:#1e293b; --muted:#64748b;
        --border:#e2e8f0; --primary:#2563eb; --stripe:#f8fafc; --hover:#eff6ff;
      }
      [data-theme="dark"]{
        --bg:#0f172a; --card:#1e293b; --text:#f1f5f9; --muted:#94a3b8;
        --border:#334155; --primary:#3b82f6; --stripe:#243449; --hover:#2d3f5c;
      }
      *{box-sizing:border-box}
      body{font-family:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;
        margin:0; padding:22px 14px 44px; background:var(--bg); color:var(--text);
        -webkit-text-size-adjust:100%; transition: background-color 0.3s ease, color 0.3s ease;}
      .container{max-width: 98%; margin: 0 auto; background:var(--card); border-radius:14px;
        box-shadow:0 10px 25px -5px rgba(0,0,0,.15);}
      .header{background:var(--primary); color:#fff; padding:22px 18px; text-align:center; position:relative; border-radius:14px 14px 0 0;}
      .header h1{margin:0; font-size:clamp(1.05rem,3.4vw,1.5rem); font-weight:800; word-break:break-word}
      .header p{margin:6px 0 0; font-size:clamp(.74rem,2.4vw,.9rem); opacity:.88}
      .theme-toggle{position:absolute; top:15px; right:15px; background:rgba(255,255,255,0.2);
        color:#fff; border:1px solid rgba(255,255,255,0.3); padding:6px 12px; border-radius:20px;
        font-size:0.75rem; font-weight:600; cursor:pointer; transition:all 0.2s ease;
        display:flex; align-items:center; gap:4px;}
      .theme-toggle:hover { background:rgba(255,255,255,0.3); }
      @media (max-width: 600px) { .theme-toggle { top:10px; right:10px; padding:4px 8px; font-size:0.7rem; } }
      .freq-switch{display:inline-flex; gap:4px; margin-top:14px;
        background:rgba(255,255,255,0.16); padding:4px; border-radius:10px;}
      .freq-btn{padding:8px 16px; border:none; border-radius:8px; background:transparent;
        color:#fff; font-weight:700; font-size:0.82rem; cursor:pointer;
        transition: all .2s ease; letter-spacing:.2px;}
      .freq-btn:hover{ background:rgba(255,255,255,0.18); }
      .freq-btn.active{ background:#fff; color:var(--primary); }
      .table-wrap{width:100%; overflow-x:auto; -webkit-overflow-scrolling:touch; padding-bottom:16px;}
      .table-wrap::-webkit-scrollbar { height:10px; }
      .table-wrap::-webkit-scrollbar-track { background:var(--stripe); border-radius:6px; margin:0 15px; }
      .table-wrap::-webkit-scrollbar-thumb { background:var(--border); border-radius:6px; border:2px solid var(--stripe); }
      .table-wrap::-webkit-scrollbar-thumb:hover { background:var(--muted); }
      table{border-collapse:collapse; width:100%; min-width:max-content}
      th,td{padding:8px 10px; border-bottom:1px solid var(--border); white-space:nowrap; font-variant-numeric:tabular-nums;}
      thead th{background:var(--stripe); color:var(--muted); font-size:0.75rem; font-weight:700;
        letter-spacing:.4px; text-transform:uppercase; text-align:center; position:sticky; top:0; z-index:3;}
      thead th:first-child{left:0; z-index:4; text-align:left; padding-left:12px;}
      thead th.period-value{text-align:center; color:var(--text); font-size:0.8rem; font-weight:600;
        letter-spacing:0; text-transform:none; font-variant-numeric:normal;}
      tbody td.latest-cell{background:transparent; font-weight:600; color:var(--text);}
      tbody th{position:sticky; left:0; z-index:2; background:var(--stripe); text-align:left;
        font-size:0.75rem; font-weight:700; color:var(--muted); text-transform:uppercase;
        letter-spacing:.4px; border-right:1px solid var(--border); padding-left:12px;}
      tbody td{text-align:center; font-size:0.85rem; font-weight:600; color:var(--text);}
      tbody tr:hover td{background:var(--hover)}
      tbody tr:hover td.latest-cell{background:var(--hover);}
      tbody tr:last-child th, tbody tr:last-child td{border-bottom:none}
      tbody td.high-cell{cursor:help;}
      .copy-card{padding:18px; border-top:1px solid var(--border); background:var(--card);}
      .copy-row{display:flex; flex-wrap:wrap; gap:16px; align-items:flex-end; justify-content:center;}
      .copy-field{display:flex; flex-direction:column; gap:4px;}
      .copy-label{font-size:0.7rem; font-weight:700; color:var(--muted); text-transform:uppercase; letter-spacing:.4px;}
      .copy-select, .copy-input{padding:8px 12px; font-size:0.95rem; font-weight:700; color:var(--text);
        background:var(--stripe); border:1px solid var(--border); border-radius:8px; outline:none;
        font-family:inherit; font-variant-numeric:tabular-nums; height:38px;}
      .copy-select{cursor:pointer; min-width:150px;}
      .copy-input{width:80px; text-align:center;}
      .copy-select:focus, .copy-input:focus { border-color:var(--primary); }

      /* Custom Dropdown CSS */
      .custom-select-wrapper {
        position: relative;
        min-width: 150px;
        height: 38px;
      }
      .custom-select-trigger {
        padding: 8px 12px;
        font-size: 0.95rem;
        font-weight: 700;
        color: var(--text);
        background: var(--stripe);
        border: 1px solid var(--border);
        border-radius: 8px;
        font-family: inherit;
        font-variant-numeric: tabular-nums;
        height: 100%;
        display: flex;
        align-items: center;
        justify-content: space-between;
        cursor: pointer;
        user-select: none;
      }
      .custom-select-trigger:focus, .custom-select-trigger.open {
        border-color: var(--primary);
        outline: none;
      }
      .custom-select-options {
        display: none;
        position: absolute;
        top: 100%;
        left: 0;
        width: 100%;
        max-height: 200px;
        overflow-y: auto;
        background: var(--stripe);
        border: 1px solid var(--border);
        border-radius: 8px;
        margin-top: 4px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        z-index: 1000;
      }
      .custom-select-options.open {
        display: block;
      }
      .custom-select-option {
        padding: 8px 12px;
        font-size: 0.95rem;
        font-weight: 700;
        color: var(--text);
        cursor: pointer;
        font-variant-numeric: tabular-nums;
      }
      .custom-select-option:hover {
        background: var(--hover);
        color: var(--primary);
      }

      .copy-btn{padding:0 18px; height:38px; background:var(--primary); color:#fff; border:none;
        border-radius:8px; font-weight:700; font-size:0.9rem; cursor:pointer; transition:background .2s;
        white-space:nowrap; display:inline-flex; align-items:center; justify-content:center;}
      .copy-btn:hover{ background:#1d4ed8; }
      .copy-btn:disabled{ opacity:.9; cursor:default; }
      .copy-hint{margin:10px 0 0; font-size:0.72rem; color:var(--muted); text-align:center; line-height:1.5;}
      @media (max-width: 600px){.copy-row{flex-direction:column; align-items:stretch;}
        .copy-select, .copy-input, .copy-btn, .custom-select-wrapper{width:100%;}}
      .foot{padding:14px 18px; font-size:.75rem; color:var(--muted); text-align:center; line-height:1.6; border-radius:0 0 14px 14px;}
      @media (max-width:600px){body{padding:10px 5px 20px} .header{padding:15px 10px}
        th,td{padding:6px 8px} thead th, thead th:first-child, tbody th{font-size:0.65rem;}
        thead th.period-value, tbody td{font-size:0.75rem;} .foot{font-size:.65rem; padding:10px}
        .freq-btn{padding:6px 12px; font-size:0.72rem;}}
    </style>
  </head>
  <body>
    <div class="container">
      <div class="header">
        <button class="theme-toggle" id="themeToggleBtn" title="Switch Theme">🌙 Dark Mode</button>
        <h1>{{ symbol }} — Historical Data</h1>
        <p id="headerSub">Loading...</p>
        <div class="freq-switch">
          <button type="button" data-freq="quarterly" class="freq-btn">Quarterly</button>
          <button type="button" data-freq="semiannual" class="freq-btn">Semiannual</button>
        </div>
      </div>
      <div id="loadingState" style="text-align:center; padding: 40px; font-weight:bold;">
        Fetching historical data for {{ symbol }}...
      </div>
      <div id="content" style="display:none;">
        <div class="table-wrap">
          <table>
            <thead id="tableHead"></thead>
            <tbody id="tableBody"></tbody>
          </table>
        </div>
        <div class="copy-card">
          <div class="copy-row">
            <div class="copy-field">
              <label class="copy-label">Latest Period</label>
              <div class="custom-select-wrapper" id="customPeriodSelect">
                <div class="custom-select-trigger" id="periodTrigger" tabindex="0">
                  <span id="periodLabel">Loading...</span>
                  <span style="font-size: 10px;">▼</span>
                </div>
                <div class="custom-select-options" id="periodOptions"></div>
              </div>
            </div>
            <div class="copy-field">
              <label class="copy-label" for="copyN">Periods to Copy (n)</label>
              <input type="number" id="copyN" class="copy-input" min="1" enterkeyhint="done" />
            </div>
            <div class="copy-field">
              <label class="copy-label" for="copyMode">Value</label>
              <select id="copyMode" class="copy-select">
                <option value="high" selected>Highest Close</option>
                <option value="close">Close Price</option>
              </select>
            </div>
            <button type="button" class="copy-btn" onclick="handleCopyData()">Copy Price Data</button>
          </div>
          <p class="copy-hint">Copies the <b>Current</b> close plus the selected period values as a tab-separated row (values only, no labels). Use the <b>Value</b> selector to copy either <b>Highest Close</b> or <b>Close Price</b>. Press <b>Enter</b> to copy instantly.</p>
        </div>
        <p class="foot" id="footerNote"></p>
      </div>
    </div>
    <script>
      const symbol = "{{ symbol }}";
      const urlParams = new URLSearchParams(window.location.search);
      let freq = urlParams.get('freq') === 'semiannual' ? 'semiannual' : 'quarterly';
      let processedData = null;
      const themeToggleBtn = document.getElementById("themeToggleBtn");

      function setTheme(theme) {
        document.documentElement.setAttribute("data-theme", theme);
        localStorage.setItem("theme", theme);
        themeToggleBtn.innerText = theme === "dark" ? "☀️ Light Mode" : "🌙 Dark Mode";
      }
      const savedTheme = localStorage.getItem("theme") || (window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
      setTheme(savedTheme);
      themeToggleBtn.addEventListener("click", () => {
        const currentTheme = document.documentElement.getAttribute("data-theme");
        setTheme(currentTheme === "dark" ? "light" : "dark");
      });

      function toISO(d) { return d.toISOString().split("T")[0]; }

      // Maps any trading day to its period bucket.
      // Quarterly : 1Q (Jan–Mar), 1H (Apr–Jun), 9M (Jul–Sep), FY (Oct–Dec)
      // Semiannual: 1H (Jan–Jun), FY (Jul–Dec)
      function buildPeriodMeta(d, frequency) {
        const y = d.getFullYear();
        const m = d.getMonth();
        if (frequency === "semiannual") {
          const half = m < 6 ? 1 : 2;
          return {
            key: `${y}-H${half}`,
            endMonth: half === 1 ? 5 : 11,
            label: half === 1 ? `1H${y}` : `FY${y}`,
          };
        }
        const q = Math.floor(m / 3) + 1;
        const labels = { 1: `1Q${y}`, 2: `1H${y}`, 3: `9M${y}`, 4: `FY${y}` };
        return { key: `${y}-Q${q}`, endMonth: q * 3 - 1, label: labels[q] };
      }

      function processPeriodData(timestamps, closes, frequency) {
        let latest = null;
        for (let i = timestamps.length - 1; i >= 0; i--) {
          if (closes[i] === null || closes[i] === undefined) continue;
          const d = new Date(timestamps[i] * 1000);
          latest = { date: toISO(d), close: closes[i] };
          break;
        }
        const grouped = {};
        const order = [];
        for (let i = 0; i < timestamps.length; i++) {
          const c = closes[i];
          if (c === null || c === undefined) continue;
          const d = new Date(timestamps[i] * 1000);
          const iso = toISO(d);
          const meta = buildPeriodMeta(d, frequency);
          let g = grouped[meta.key];
          if (!g) {
            g = grouped[meta.key] = {
              period: meta.label,
              date: null,
              close: null,
              high: null,
              highDate: null,
            };
            order.push(meta.key);
          }
          // Highest close recorded inside the period
          if (g.high === null || c > g.high) {
            g.high = c;
            g.highDate = iso;
          }
          // Period-end close: last trading day of the closing month
          if (d.getMonth() === meta.endMonth && (g.date === null || iso > g.date)) {
            g.date = iso;
            g.close = c;
          }
        }
        const periodData = order
          .map((k) => grouped[k])
          .filter((p) => p.close !== null && p.date !== null);
        periodData.sort((a, b) => (a.date < b.date ? 1 : a.date > b.date ? -1 : 0));
        return { latest, periodData };
      }

      async function loadData() {
        try {
          let apiSymbol = symbol;
          if (symbol.endsWith('.HK')) {
              let parts = symbol.split('.');
              let numPart = parts[0];
              if (/^\d{1,4}$/.test(numPart)) {
                  apiSymbol = numPart.padStart(4, '0') + '.HK';
              }
          }
          const response = await fetch(`/proxy?symbol=${encodeURIComponent(apiSymbol)}&range=10y&interval=1d`);
          if (!response.ok) throw new Error(`Server returned ${response.status}`);
          const data = await response.json();
          if (!data.chart || !data.chart.result || data.chart.result.length === 0) {
            throw new Error("No data found for this ticker symbol.");
          }
          const result = data.chart.result[0];
          processedData = processPeriodData(result.timestamp, result.indicators.quote[0].close, freq);
          document.getElementById("loadingState").style.display = "none";
          document.getElementById("content").style.display = "block";
          render();
        } catch (error) {
          document.getElementById("loadingState").innerHTML = `<span style="color:#ef4444">Error: ${error.message}</span><br><small>Please check the ticker symbol.</small>`;
        }
      }

      function render() {
        if (!processedData || !processedData.periodData || processedData.periodData.length === 0) return;
        const { latest, periodData } = processedData;
        const fmtClose = (v) => v.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 5 });
        const fmtOrDash = (v) => (v === null || v === undefined) ? "—" : fmtClose(v);
        const latestDateCell = latest ? latest.date : "—";
        const latestCloseCell = latest ? fmtClose(latest.close) : "—";
        const latestHeader = latest ? latest.date : "—";

        document.getElementById("headerSub").innerText =
          `${freq === 'semiannual' ? 'Semiannual' : 'Quarter-End'} Closing Prices · Last 10 Years · Newest First · Includes Current Close & Period Highs`;

        document.querySelectorAll('[data-freq]').forEach(btn => {
          btn.classList.toggle('active', btn.getAttribute('data-freq') === freq);
        });

        document.getElementById("tableHead").innerHTML = `
          <tr>
            <th scope="col">Period</th>
            <th scope="col" class="period-value">Current</th>
            ${periodData.map((d) => `<th scope="col" class="period-value">${d.period}</th>`).join("")}
          </tr>
        `;
        document.getElementById("tableBody").innerHTML = `
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
          <tr>
            <th scope="row">Highest Close</th>
            <td class="latest-cell">${latestCloseCell}</td>
            ${periodData.map((d) => `<td class="high-cell" title="Highest close on ${d.highDate || "—"}">${fmtOrDash(d.high)}</td>`).join("")}
          </tr>
        `;
        document.getElementById("footerNote").innerHTML =
          `Swipe horizontally to view every period. The <b>Close Price</b> row shows period-end closing prices in the listing currency. The <b>Highest Close</b> row shows the highest daily closing price recorded inside each period (hover a cell to see the exact date). The <b>Current</b> column always shows the most recent trading day close (${latestHeader}).`;
        
        const periodOptionsEl = document.getElementById("periodOptions");
        const periodLabelEl = document.getElementById("periodLabel");
        periodOptionsEl.innerHTML = periodData.map((d, i) => `<div class="custom-select-option" data-value="${i}">${d.period}</div>`).join("");
        periodLabelEl.textContent = periodData[0].period;
        window.selectedPeriodIndex = 0;

        periodOptionsEl.querySelectorAll('.custom-select-option').forEach(opt => {
            opt.addEventListener('click', function() {
                window.selectedPeriodIndex = parseInt(this.getAttribute('data-value'), 10);
                periodLabelEl.textContent = this.textContent;
                periodOptionsEl.classList.remove('open');
                document.getElementById('periodTrigger').classList.remove('open');
            });
        });

        const defaultN = Math.min(freq === "semiannual" ? 10 : 20, periodData.length);
        document.getElementById("copyN").value = defaultN;
        document.getElementById("copyN").max = periodData.length;
      }

      // Custom dropdown event listeners
      const periodTrigger = document.getElementById('periodTrigger');
      const periodOptionsEl = document.getElementById('periodOptions');
      
      periodTrigger.addEventListener('click', function(e) {
        e.stopPropagation();
        const isOpen = periodOptionsEl.classList.contains('open');
        periodOptionsEl.classList.toggle('open');
        periodTrigger.classList.toggle('open');
      });

      periodTrigger.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          periodTrigger.click();
        }
      });

      document.addEventListener('click', function(e) {
        if (!document.getElementById('customPeriodSelect').contains(e.target)) {
          periodOptionsEl.classList.remove('open');
          periodTrigger.classList.remove('open');
        }
      });

      const copyBtnEl = document.querySelector(".copy-btn");
      function flashCopyBtn() {
        if (!copyBtnEl) return;
        if (copyBtnEl.dataset.busy === "1") return;
        copyBtnEl.dataset.busy = "1";
        copyBtnEl.disabled = true;
        copyBtnEl.textContent = "Copied ✓";
        setTimeout(function () {
          copyBtnEl.textContent = "Copy Price Data";
          copyBtnEl.disabled = false;
          copyBtnEl.dataset.busy = "0";
        }, 900);
      }

      function handleCopyData() {
        if (!processedData) return;
        const startIndex = window.selectedPeriodIndex || 0;
        const nInput = document.getElementById("copyN");
        let n = parseInt(nInput.value, 10);
        if (isNaN(n) || n < 1) n = 1;
        const mode = document.getElementById("copyMode").value;
        const pick = (p) => (mode === "high" && p.high !== null && p.high !== undefined) ? p.high : p.close;
        const selectedPeriods = processedData.periodData.slice(startIndex, startIndex + n);
        nInput.value = selectedPeriods.length;
        const values = [];
        if (processedData.latest) values.push(processedData.latest.close.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 5 }));
        for (let i = 0; i < selectedPeriods.length; i++) {
          values.push(pick(selectedPeriods[i]).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 5 }));
        }
        const text = values.join("\t");
        const isDark = document.documentElement.getAttribute("data-theme") === "dark";
        function toast(icon, title) {
          if (window.Swal) {
            Swal.fire({ toast: true, position: "top", showConfirmButton: false, timer: 3000,
              timerProgressBar: true, background: isDark ? "#1e293b" : "#ffffff",
              color: isDark ? "#f1f5f9" : "#1e293b", icon: icon, title: title });
          } else { alert(title); }
        }
        function onOk() { toast("success", "Successfully copied!"); flashCopyBtn(); }
        function onFail() { toast("error", "Copy failed — please select and copy manually."); }
        if (navigator.clipboard && window.isSecureContext) {
          navigator.clipboard.writeText(text).then(onOk).catch(function () {
            var ta = document.createElement("textarea");
            ta.value = text; ta.style.position = "fixed"; ta.style.top = "-1000px";
            document.body.appendChild(ta); ta.select();
            try { document.execCommand("copy") ? onOk() : onFail(); } catch (e) { onFail(); }
            document.body.removeChild(ta);
          });
        } else {
          var ta = document.createElement("textarea");
          ta.value = text; ta.style.position = "fixed"; ta.style.top = "-1000px";
          document.body.appendChild(ta); ta.select();
          try { document.execCommand("copy") ? onOk() : onFail(); } catch (e) { onFail(); }
          document.body.removeChild(ta);
        }
      }

      document.addEventListener("keydown", function (e) {
        if (e.key !== "Enter" && e.keyCode !== 13) return;
        if (e.isComposing) return;
        const tag = (e.target.tagName || "").toUpperCase();
        if (tag === "BUTTON" || tag === "TEXTAREA" || tag === "A") return;
        if (!processedData || !processedData.periodData || processedData.periodData.length === 0) return;
        e.preventDefault();
        handleCopyData();
      }, { capture: true });

      document.querySelectorAll('[data-freq]').forEach(btn => {
        btn.addEventListener('click', (e) => {
          const f = btn.getAttribute('data-freq');
          if (f === freq) return;
          freq = f;
          const newUrl = new URL(window.location);
          newUrl.searchParams.set('freq', freq);
          window.history.pushState({}, '', newUrl);
          loadData();
        });
      });

      loadData();
    </script>
  </body>
</html>'''


@app.route("/")
def index():
    return render_template_string(HTML_PAGE)


@app.route("/history/<symbol>")
def history(symbol):
    display_symbol = symbol
    if symbol.upper().endswith('.HK'):
        parts = symbol.split('.')
        num_part = parts[0]
        if num_part.isdigit() and len(num_part) <= 4:
            num_part = num_part.lstrip('0') or '0'
            display_symbol = f"{num_part}.HK"
    return render_template_string(HISTORY_PAGE, symbol=display_symbol)


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
    print(" * Running on http://127.0.0.1:5000")
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False, request_handler=QuietRequestHandler)