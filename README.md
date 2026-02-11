# 🥇 Gold AI Signal Bot - Professional XAUUSD Trading System

<div align="center">

![Version](https://img.shields.io/badge/version-1.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![License](https://img.shields.io/badge/license-Personal%20Use-orange)

**A professional-grade AI trading signal system for Gold (XAUUSD) with Telegram integration**

[Quick Start](#-quick-start) • [Features](#-features) • [Documentation](#-documentation) • [Setup](#-setup)

</div>

---

## 📋 Overview

The Gold AI Signal Bot is a sophisticated trading signal system that monitors XAUUSD (Gold vs USD) markets 24/7 and sends high-probability BUY/SELL signals directly to your Telegram. Unlike simple indicator bots, this system uses multi-factor analysis combining technical indicators, macro factors, news events, and strict risk management.

**⚠️ IMPORTANT:** This is a decision support tool, NOT financial advice. All trading involves risk.

---

## ✨ Features

### 🎯 Core Capabilities
- **Multi-Timeframe Analysis** - M15, H1, H4, D1 confluence
- **Advanced Technical Indicators** - EMA, RSI, MACD, ATR, Support/Resistance
- **Macro Factor Integration** - DXY, US10Y yields, risk sentiment
- **Economic Calendar** - Avoids high-impact news events
- **Risk Management Engine** - Strict position sizing and stop losses
- **Confidence Scoring** - 0-100% signal confidence rating
- **Multiple Signal Types** - BUY, SELL, NO_TRADE, STOP_TRADING

### 🛡️ Safety Features
- **News Event Filter** - No trading during major announcements
- **Volatility Detection** - Stops trading in extreme conditions
- **Session Quality Check** - Prioritizes London-NY overlap
- **Spread Monitoring** - Avoids high spread conditions
- **Conservative Approach** - Prefers NO_TRADE over weak signals

### 📱 Telegram Integration
- **Real-time Alerts** - Instant notifications to your phone
- **Professional Formatting** - Clear, structured signal messages
- **Entry/Exit Levels** - Precise stop loss and take profit
- **Risk Analysis** - Detailed reasoning for each signal
- **Status Updates** - Startup, shutdown, error notifications

---

## 🚀 Quick Start

### 1. Get Telegram Credentials

**Create Bot (@BotFather):**
```
1. Open Telegram → Search @BotFather
2. Send: /newbot
3. Follow prompts
4. Save the token
```

**Get Chat ID (@userinfobot):**
```
1. Search @userinfobot
2. Send: /start
3. Copy your ID
```

### 2. Install & Configure

```bash
# Install dependencies
pip install numpy requests

# Edit gold_signal_bot.py (lines 25-26)
TELEGRAM_BOT_TOKEN = "your_bot_token_here"
TELEGRAM_CHAT_ID = "your_chat_id_here"
```

### 3. Run

```bash
python gold_signal_bot.py
```

**That's it!** Check Telegram for the startup message.

📖 See [QUICKSTART.md](QUICKSTART.md) for detailed 5-minute setup guide.

---

## 📊 Signal Examples

### BUY Signal
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

### NO TRADE
```
⏸️ NO TRADE

Reason: Signal confidence 60% < 65% threshold
Next Check: 14:45 UTC
```

### STOP TRADING
```
🚨 STOP TRADING

⚠️ Market risk too high: EXTREME_VOLATILITY, WIDE_SPREAD

Resume Time: 15:30 UTC
```

---

## 🏗️ System Architecture

```
Gold Signal Bot (Controller)
    │
    ├── Signal Engine (AI Brain)
    │   ├── Market Data Engine
    │   ├── Technical Engine
    │   ├── News Engine
    │   └── Risk Engine
    │
    └── Telegram Bot (Messenger)
```

**Key Components:**
- **MarketDataEngine** - Fetches XAUUSD, DXY, yields, sentiment
- **TechnicalEngine** - Calculates EMA, RSI, MACD, ATR
- **NewsEngine** - Monitors economic calendar
- **RiskEngine** - Assesses market risk and position sizing
- **SignalEngine** - Multi-factor decision logic
- **TelegramBot** - Formats and sends signals

📖 See [SYSTEM_ARCHITECTURE.md](SYSTEM_ARCHITECTURE.md) for complete technical docs.

---

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| **QUICKSTART.md** | 5-minute setup guide |
| **SETUP_GUIDE.md** | Complete installation & configuration |
| **SYSTEM_ARCHITECTURE.md** | Technical architecture & algorithms |
| **requirements.txt** | Python dependencies |

---

## ⚙️ Configuration

### Basic Settings
```python
class BotConfig:
    # Required
    TELEGRAM_BOT_TOKEN = "your_token"
    TELEGRAM_CHAT_ID = "your_chat_id"
    
    # Optional (defaults shown)
    RISK_PERCENT = 2.0          # Risk per trade (1-3%)
    MIN_CONFIDENCE = 65         # Minimum signal confidence
    MAX_ATR_MULTIPLIER = 2.5    # Volatility threshold
```

### Advanced Settings
- **Trading Sessions** - London/NY priority
- **Timeframes** - M15, H1, H4, D1
- **Risk Thresholds** - ATR, spread, volume limits
- **Signal Frequency** - 15-minute checks (configurable)

---

## 🔧 Deployment Options

### Option 1: Simple (Screen)
```bash
screen -S goldbot
python gold_signal_bot.py
# Ctrl+A, D to detach
```

### Option 2: Professional (Systemd)
```bash
sudo systemctl enable gold-bot
sudo systemctl start gold-bot
```

### Option 3: Cloud (Docker)
```bash
docker build -t gold-bot .
docker run -d --restart unless-stopped gold-bot
```

### Option 4: VPS
- DigitalOcean ($6/mo)
- Vultr ($5/mo)
- AWS Free Tier
- Google Cloud Free Tier

---

## 📈 Performance Expectations

**Realistic Expectations:**
- Signal frequency: 1-4 per day
- NO_TRADE frequency: 60-70% of checks
- Risk:Reward: 1:1.33 to 1:2.33
- Win rate: NOT GUARANTEED (focus on process, not results)

**Quality over Quantity:**
- Conservative approach
- Strict filters
- High-confidence signals only
- Frequent NO_TRADE is normal and healthy

---

## 🔌 Data Integration

### Mock Data (Default)
The bot uses mock data for testing. This is NOT suitable for live trading.

### Real Data Options

**Option 1: MetaTrader 5**
```bash
pip install MetaTrader5
# Connect to MT5 terminal
# See SETUP_GUIDE.md for code
```

**Option 2: API (Alpha Vantage, etc.)**
```python
# Free API keys available
# See SETUP_GUIDE.md for integration
```

**Option 3: Yahoo Finance**
```bash
pip install yfinance
# See SETUP_GUIDE.md for code
```

---

## ⚠️ Risk Disclaimers

### CRITICAL WARNINGS

1. **NOT FINANCIAL ADVICE**
   - This is a decision support tool
   - You are responsible for all trading decisions
   - Past performance ≠ future results

2. **SIGNIFICANT RISK OF LOSS**
   - Gold trading is highly volatile
   - You can lose your entire investment
   - Only trade with money you can afford to lose

3. **NO GUARANTEES**
   - No guarantee of profits
   - No guarantee of accuracy
   - Signals may be wrong

4. **TEST THOROUGHLY**
   - Paper trade first
   - Monitor for weeks before risking capital
   - Understand the system before trading

5. **USE PROPER RISK MANAGEMENT**
   - Never risk more than 1-3% per trade
   - Always use stop losses
   - Don't overtrade

### Legal Notice
This software is provided "as is" without warranty of any kind. The author is not responsible for any losses incurred from using this system. Trading financial instruments involves substantial risk.

---

## 🛠️ Troubleshooting

### Common Issues

**"Telegram send error"**
- Verify bot token and chat ID
- Ensure you started the bot in Telegram
- Check for typos/spaces

**"Module not found"**
```bash
pip install --upgrade numpy requests
```

**No signals received**
- Expected with MOCK data
- Connect real data source
- Lower MIN_CONFIDENCE for testing

**Bot stops running**
- Use deployment options (screen, systemd, docker)
- Consider VPS for 24/7 operation

📖 See SETUP_GUIDE.md for complete troubleshooting.

---

## 🎯 Roadmap

### Phase 1 (Current - v1.0)
- [x] Core signal engine
- [x] Telegram integration
- [x] Multi-factor analysis
- [x] Risk management
- [x] Documentation

### Phase 2 (Future)
- [ ] Real broker integration (MT5)
- [ ] Backtesting engine
- [ ] Performance analytics
- [ ] Machine learning scoring
- [ ] Multi-symbol support

### Phase 3 (Advanced)
- [ ] Auto-execution capability
- [ ] Portfolio management
- [ ] Web dashboard
- [ ] Mobile app

---

## 📄 License

**Personal Use Only**

This software is provided for personal, non-commercial use only. You may:
- Use for your own trading decisions
- Modify for personal use
- Learn from the code

You may NOT:
- Sell or commercialize
- Redistribute
- Claim as your own work

---

## 🤝 Support

**For Issues:**
1. Check SETUP_GUIDE.md
2. Review SYSTEM_ARCHITECTURE.md
3. Test with MOCK data first
4. Verify configuration

**No Official Support Provided**
- This is an open-source educational project
- No guarantee of assistance
- Community contributions welcome

---

## 🙏 Acknowledgments

Built with:
- Python 3.8+
- NumPy for calculations
- Requests for Telegram API
- Professional trading knowledge

Inspired by:
- Quantitative trading principles
- Risk management best practices
- Professional signal services

---

## 📞 Contact

**Repository:** Gold AI Signal Bot  
**Version:** 1.0  
**Last Updated:** February 2024  
**Language:** Python

---

<div align="center">

**⚠️ REMEMBER: Trade Responsibly. Never Risk More Than You Can Afford to Lose. ⚠️**

**Good luck and trade safely! 🍀**

---

*This is a decision support tool, not financial advice.*  
*Always do your own research and consult a financial advisor.*

</div>
