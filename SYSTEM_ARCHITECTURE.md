# 📐 GOLD AI SIGNAL BOT - System Architecture

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                   GOLD SIGNAL BOT                       │
│                    (Main Controller)                    │
└──────────────────┬──────────────────────────────────────┘
                   │
        ┌──────────┴──────────┐
        │                     │
        ▼                     ▼
┌───────────────┐     ┌───────────────┐
│  Signal Engine│     │ Telegram Bot  │
│   (AI Brain)  │────▶│  (Messenger)  │
└───────┬───────┘     └───────────────┘
        │
        │ Analyzes Data From:
        │
        ├─────────────────────┐
        │                     │
        ▼                     ▼
┌───────────────┐     ┌───────────────┐
│ Market Data   │     │  News Engine  │
│   Engine      │     │               │
└───────┬───────┘     └───────┬───────┘
        │                     │
        ▼                     ▼
┌───────────────┐     ┌───────────────┐
│  Technical    │     │ Economic      │
│  Analysis     │     │ Calendar      │
└───────┬───────┘     └───────────────┘
        │
        ▼
┌───────────────┐
│  Risk Engine  │
│ (Safety Net)  │
└───────────────┘
```

---

## 🧩 Core Components

### 1. **BotConfig** (Configuration Layer)
**Purpose:** Centralized settings management  
**Responsibilities:**
- Store API keys (Telegram, market data)
- Define risk parameters
- Set trading thresholds
- Configure timeframes

**Key Parameters:**
```python
TELEGRAM_BOT_TOKEN     # Bot authentication
TELEGRAM_CHAT_ID       # Target chat
RISK_PERCENT = 2.0     # Max risk per trade
MIN_CONFIDENCE = 65    # Signal threshold
MAX_ATR_MULTIPLIER     # Volatility limit
```

---

### 2. **MarketDataEngine** (Data Acquisition)
**Purpose:** Fetch and process market data  
**Data Sources:**
- XAUUSD real-time prices
- Historical candles (M15, H1, H4, D1)
- DXY (US Dollar Index)
- US10Y (Treasury yields)
- Risk sentiment indicators

**Methods:**
```python
get_xauusd_price()      # Current gold price + candles
get_dxy_index()         # Dollar strength
get_us10y_yield()       # Bond yields
get_risk_sentiment()    # RISK_ON/RISK_OFF/NEUTRAL
```

**Data Flow:**
```
External APIs → MarketDataEngine → Cache → Signal Engine
```

---

### 3. **TechnicalEngine** (Indicator Calculation)
**Purpose:** Calculate technical indicators  
**Indicators Computed:**
- **EMA** (50, 200): Trend identification
- **RSI** (14): Momentum + overbought/oversold
- **MACD**: Trend confirmation
- **ATR**: Volatility measurement
- **Support/Resistance**: Key price levels

**Analysis Framework:**
```python
Trend Detection:
  - UPTREND: Price > EMA50 > EMA200
  - DOWNTREND: Price < EMA50 < EMA200
  - RANGING: Overlapping EMAs

Momentum Analysis:
  - RSI < 30: Oversold (potential buy)
  - RSI > 70: Overbought (potential sell)
  - 30-70: Neutral zone

Volatility Check:
  - ATR > Normal*2.5: STOP TRADING
  - ATR > Normal*1.5: HIGH RISK
```

---

### 4. **NewsEngine** (Event Monitoring)
**Purpose:** Monitor economic events and news  
**Functions:**
- Check economic calendar
- Identify high-impact events
- Assess news sentiment
- Calculate time to event

**High-Impact Events:**
- FOMC meetings
- CPI/NFP releases
- Central bank speeches
- Geopolitical crises

**Safety Logic:**
```python
if event_in_next_4_hours and impact == HIGH:
    return NO_TRADE
```

---

### 5. **RiskEngine** (Risk Management)
**Purpose:** Protect capital through strict risk controls  
**Risk Assessment Factors:**

| Factor | Weight | Trigger |
|--------|--------|---------|
| Extreme Volatility | 40 pts | ATR > 2.5x normal |
| Wide Spread | 15 pts | Spread > 0.50 |
| Low Liquidity | 25 pts | Volume < threshold |
| High Volatility | 20 pts | ATR > 1.5x normal |

**Risk Levels:**
- **CRITICAL** (50+ pts): STOP TRADING
- **HIGH** (30-49 pts): NO TRADE
- **MEDIUM** (15-29 pts): Trade with caution
- **LOW** (0-14 pts): Normal conditions

**Position Sizing:**
```python
Risk Amount = Account * (RISK_PERCENT / 100)
Position Size = Risk Amount / (Pip Risk * Pip Value)
```

**Session Quality:**
```
HIGH: London-NY overlap (8:00-17:00 UTC)
MEDIUM: London/NY separate (7:00-22:00 UTC)
LOW: Asian session (22:00-7:00 UTC)
```

---

### 6. **SignalEngine** (AI Decision Core)
**Purpose:** Multi-factor analysis and signal generation  

**Decision Pipeline:**
```
1. Fetch Data (Market + Macro + News)
2. Calculate Indicators (Technical)
3. Check Calendar (Events)
4. Assess Risk (Safety)
5. Generate Signal (Logic)
6. Format Output (Telegram)
```

**Confidence Scoring System:**
```python
Base Points: 100

Trend Alignment:          +30 pts (EMA confirmation)
RSI Confirmation:         +20 pts (momentum match)
MACD Confirmation:        +15 pts (crossover)
Macro Alignment:          +20 pts (DXY + sentiment)
Support/Resistance:       +15 pts (near key level)
Session Quality:          +10 pts (London-NY)

Penalties:
Extreme RSI:              -10 pts
Volatility spike:         -15 pts
News uncertainty:         -20 pts
```

**Signal Types:**
1. **BUY/SELL** (Confidence ≥ 65%)
2. **NO_TRADE** (Low confidence / poor setup)
3. **STOP_TRADING** (Dangerous conditions)

**Entry/Exit Logic:**
```python
BUY Signal:
  Entry: Current Ask
  Stop Loss: Entry - (1.5 * ATR)
  TP1: Entry + (2.0 * ATR)  [Risk:Reward 1:1.33]
  TP2: Entry + (3.5 * ATR)  [Risk:Reward 1:2.33]

SELL Signal:
  Entry: Current Bid
  Stop Loss: Entry + (1.5 * ATR)
  TP1: Entry - (2.0 * ATR)
  TP2: Entry - (3.5 * ATR)
```

---

### 7. **TelegramBot** (Communication Layer)
**Purpose:** Send formatted signals to user  

**Message Templates:**

**BUY/SELL Signal:**
```
🟢 BUY GOLD NOW

📊 ENTRY: $2050.00
🛑 STOP LOSS: $2035.00
🎯 TAKE PROFIT 1: $2070.00
🎯 TAKE PROFIT 2: $2087.50

⚠️ RISK LEVEL: MEDIUM
✅ CONFIDENCE: 75%
📈 MARKET STATE: UPTREND
⏱️ TYPE: INTRADAY

📋 ANALYSIS:
  • Strong uptrend (EMA alignment)
  • RSI oversold recovery (42.3)
  • MACD bullish crossover
  • Weak USD (DXY: 102.85)
  • Price above support (2045.00)

⏰ 2024-02-11 14:30 UTC
```

**NO TRADE:**
```
⏸️ NO TRADE

Reason: Signal confidence 60% < 65% threshold
Next Check: 14:45 UTC
```

**STOP TRADING:**
```
🚨 STOP TRADING

⚠️ Market risk too high: EXTREME_VOLATILITY, WIDE_SPREAD

Resume Time: 15:30 UTC
```

---

### 8. **GoldSignalBot** (Main Controller)
**Purpose:** Orchestrate all components  

**Lifecycle:**
```
START
  ↓
Initialize Components
  ↓
Send Startup Message
  ↓
┌─────────────────┐
│  Main Loop:     │
│  1. Generate    │
│  2. Filter      │
│  3. Send        │
│  4. Sleep 15min │
└─────────────────┘
  ↓
STOP (Ctrl+C)
  ↓
Send Shutdown Message
```

**Anti-Spam Logic:**
- Track last signal sent
- Only send if action changes
- Or if entry price moves >$5
- Prevents duplicate alerts

---

## 🔄 Data Flow Architecture

```
┌─────────────┐
│   START     │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────┐
│  1. FETCH MARKET DATA           │
│     - XAUUSD price + candles    │
│     - DXY, US10Y                │
│     - Risk sentiment            │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│  2. CALCULATE INDICATORS        │
│     - EMA 50/200                │
│     - RSI, MACD                 │
│     - ATR, Support/Resistance   │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│  3. CHECK NEWS CALENDAR         │
│     - High-impact events?       │
│     - Time to event < 4 hours?  │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│  4. ASSESS RISK                 │
│     - Volatility normal?        │
│     - Liquidity adequate?       │
│     - Spread acceptable?        │
└────────────┬────────────────────┘
             │
        ┌────┴────┐
        │         │
        ▼         ▼
    [UNSAFE]  [SAFE]
        │         │
        ▼         ▼
    STOP/NO   ANALYZE
    TRADE       ↓
                ▼
        ┌───────────────┐
        │ 5. SCORE      │
        │    SIGNAL     │
        │  Confidence:  │
        │  0-100%       │
        └───────┬───────┘
                │
           ┌────┴────┐
           │         │
           ▼         ▼
      [< 65%]   [≥ 65%]
           │         │
           ▼         ▼
      NO TRADE   BUY/SELL
           │         │
           └────┬────┘
                │
                ▼
        ┌───────────────┐
        │ 6. FORMAT &   │
        │    SEND       │
        │   TELEGRAM    │
        └───────┬───────┘
                │
                ▼
        ┌───────────────┐
        │ 7. SLEEP      │
        │   15 minutes  │
        └───────┬───────┘
                │
                ▼
           [LOOP BACK]
```

---

## 🎯 Decision Matrix

| Condition | Trend | RSI | MACD | DXY | Risk | Session | → Action |
|-----------|-------|-----|------|-----|------|---------|----------|
| Perfect BUY | UP | 30-50 | BUY | <103 | LOW | OVERLAP | **BUY 85%** |
| Good BUY | UP | 30-50 | BUY | Any | MED | ACTIVE | **BUY 70%** |
| Weak BUY | UP | Any | SELL | >104 | MED | ASIAN | **NO TRADE** |
| Perfect SELL | DOWN | 50-70 | SELL | >104 | LOW | OVERLAP | **SELL 85%** |
| Good SELL | DOWN | 50-70 | SELL | Any | MED | ACTIVE | **SELL 70%** |
| Weak SELL | DOWN | Any | BUY | <103 | MED | ASIAN | **NO TRADE** |
| High Vol | Any | Any | Any | Any | HIGH | Any | **STOP** |
| News Soon | Any | Any | Any | Any | Any | Any | **NO TRADE** |

---

## 🔐 Safety Mechanisms

### Critical Filters (MUST PASS)
1. **No High-Impact News** in next 4 hours
2. **Risk Score** < 50 (not CRITICAL)
3. **Confidence** ≥ 65%
4. **Session Quality** ≥ MEDIUM (optional but weighted)

### Position Limits
- Max risk: 2% per trade (configurable)
- Max ATR: 2.5x normal
- Min confidence: 65%

### Error Handling
```python
try:
    signal = generate_signal()
except Exception as e:
    log_error(e)
    send_telegram("⚠️ Bot encountered error, restarting...")
    sleep(60)
    retry()
```

---

## 📊 Performance Metrics

**Expected Behavior:**
- Signal frequency: 1-4 per day (quality over quantity)
- Win rate: Not guaranteed, focus on R:R
- Risk:Reward: 1:1.33 to 1:2.33
- NO_TRADE frequency: 60-70% of checks (conservative)

**Optimization Targets:**
- Reduce false signals (<30%)
- Avoid trading during news
- Maintain strict risk management
- Filter low-quality setups

---

## 🚀 Scalability & Extensions

### Phase 1 (Current)
- Single symbol (XAUUSD)
- Mock data support
- Basic technical analysis
- Telegram alerts

### Phase 2 (Future)
- Multi-symbol support
- Real broker integration (MT5/API)
- Machine learning signal scoring
- Backtesting engine

### Phase 3 (Advanced)
- Auto-execution via broker API
- Portfolio management
- Advanced risk models
- Web dashboard

---

## 📝 Code Quality Standards

- **Type hints** throughout
- **Docstrings** for all classes/methods
- **Error handling** at every external call
- **Logging** for debugging
- **Modular design** (easy to extend)
- **Configuration-driven** (no hardcoded values)

---

**Version:** 1.0  
**Architecture:** Modular Microservices  
**Language:** Python 3.8+  
**Design Pattern:** MVC + Strategy Pattern
