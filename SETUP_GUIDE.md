# 🚀 GOLD AI SIGNAL BOT - Complete Setup Guide

## 📋 Table of Contents
1. [System Requirements](#system-requirements)
2. [Telegram Bot Setup](#telegram-bot-setup)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Running the Bot](#running-the-bot)
6. [Deployment (24/7)](#deployment-247)
7. [Troubleshooting](#troubleshooting)

---

## 🖥️ System Requirements

- **Python**: 3.8 or higher
- **Operating System**: Linux, macOS, or Windows
- **Internet**: Stable connection required
- **RAM**: Minimum 512MB
- **Disk Space**: 100MB

---

## 🤖 Telegram Bot Setup

### Step 1: Create Your Bot

1. **Open Telegram** and search for **@BotFather**
2. Send `/newbot` command
3. Choose a name (e.g., "Gold Signal Pro")
4. Choose a username (must end in 'bot', e.g., "gold_signal_pro_bot")
5. **Save the token** - it looks like:
   ```
   123456789:ABCdefGHIjklMNOpqrsTUVwxyz
   ```

### Step 2: Get Your Chat ID

**Option A: Using userinfobot**
1. Search for **@userinfobot** in Telegram
2. Send `/start`
3. Bot will reply with your ID (e.g., `987654321`)

**Option B: Using RawDataBot**
1. Search for **@RawDataBot**
2. Send any message
3. Look for `"id":` in the response

### Step 3: Start Your Bot

1. Find your bot in Telegram (search for the username)
2. Click **START** or send `/start`

---

## 📦 Installation

### Option 1: Quick Setup (Recommended)

```bash
# Clone or download the bot files
cd gold-signal-bot

# Install dependencies
pip install -r requirements.txt

# Or install manually
pip install numpy requests
```

### Option 2: Virtual Environment (Advanced)

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

## ⚙️ Configuration

### 1. Edit the Bot Configuration

Open `gold_signal_bot.py` and find the `BotConfig` class (around line 25):

```python
class BotConfig:
    # REQUIRED: Replace these with your values
    TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"  # From @BotFather
    TELEGRAM_CHAT_ID = "YOUR_CHAT_ID_HERE"      # From @userinfobot
    
    # OPTIONAL: Customize these
    RISK_PERCENT = 2.0  # Risk per trade (1-3% recommended)
    MIN_CONFIDENCE = 65  # Minimum confidence to send signals
```

**Example Configuration:**
```python
TELEGRAM_BOT_TOKEN = "6123456789:AAE7xMq_example_token_abc123"
TELEGRAM_CHAT_ID = "987654321"
RISK_PERCENT = 2.0
MIN_CONFIDENCE = 70
```

### 2. Advanced Configuration (Optional)

**Risk Management:**
```python
MAX_ATR_MULTIPLIER = 2.5  # Stop trading if volatility too high
MIN_VOLUME_THRESHOLD = 1000  # Minimum volume requirement
```

**Trading Sessions (UTC):**
```python
LONDON_OPEN = 8   # London session start
NY_OPEN = 13      # New York session start
ASIAN_CLOSE = 9   # Asian session end
```

---

## 🏃 Running the Bot

### Basic Usage

```bash
# Run the bot
python gold_signal_bot.py
```

**Expected Output:**
```
    ╔═══════════════════════════════════════════════════╗
    ║     GOLD AI SIGNAL BOT - Professional Edition     ║
    ║              XAUUSD Trading System                ║
    ╚═══════════════════════════════════════════════════╝
    
🚀 Gold AI Signal Bot Starting...
⏰ Started at: 2024-02-11 14:30 UTC
============================================================
```

### Test Mode

For testing, reduce the wait time:

```python
# In gold_signal_bot.py, find:
time.sleep(900)  # 15 minutes

# Change to:
time.sleep(60)  # 1 minute for testing
```

### Stop the Bot

Press `Ctrl+C` to stop gracefully.

---

## 🌐 Deployment (24/7)

### Option 1: Linux Screen (Simple)

```bash
# Start a screen session
screen -S gold_bot

# Run the bot
python gold_signal_bot.py

# Detach: Press Ctrl+A, then D

# Reattach later
screen -r gold_bot

# Kill session
screen -X -S gold_bot quit
```

### Option 2: Systemd Service (Professional)

Create `/etc/systemd/system/gold-bot.service`:

```ini
[Unit]
Description=Gold AI Signal Bot
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/gold-signal-bot
ExecStart=/usr/bin/python3 gold_signal_bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable gold-bot
sudo systemctl start gold-bot

# Check status
sudo systemctl status gold-bot

# View logs
sudo journalctl -u gold-bot -f
```

### Option 3: Docker (Advanced)

Create `Dockerfile`:

```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY gold_signal_bot.py .

CMD ["python", "gold_signal_bot.py"]
```

Build and run:
```bash
docker build -t gold-signal-bot .
docker run -d --name gold-bot --restart unless-stopped gold-signal-bot
```

### Option 4: VPS / Cloud Server

**Recommended Providers:**
- DigitalOcean (Droplet: $6/month)
- Vultr (Cloud Compute: $5/month)
- AWS EC2 (t2.micro: Free tier)
- Google Cloud (e2-micro: Free tier)

**Setup Steps:**
1. Create a server (Ubuntu 22.04 recommended)
2. SSH into server: `ssh root@your_server_ip`
3. Install Python: `apt update && apt install python3 python3-pip`
4. Upload bot files or clone from Git
5. Use Screen or Systemd method above

---

## 🔧 Troubleshooting

### Issue 1: "Telegram send error"

**Cause:** Invalid token or chat ID

**Solution:**
1. Verify token from @BotFather
2. Verify chat ID from @userinfobot
3. Ensure you've started your bot in Telegram
4. Check for extra spaces in config

### Issue 2: Bot crashes immediately

**Cause:** Missing dependencies

**Solution:**
```bash
pip install --upgrade numpy requests
```

### Issue 3: No signals received

**Cause:** Mock data not triggering conditions

**Solution:**
This is expected with MOCK data. The bot needs real market data to generate actual signals.

**Next Steps:**
- Connect to a real data provider (see Data Integration below)
- Lower `MIN_CONFIDENCE` temporarily for testing
- Check logs for "NO_TRADE" reasons

### Issue 4: "Module not found" error

**Solution:**
```bash
# Ensure you're in the right directory
cd /path/to/gold-signal-bot

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue 5: Bot stops after some time

**Cause:** Server/computer went to sleep or lost connection

**Solution:**
- Use deployment options (Screen, Systemd, Docker)
- Use a VPS for 24/7 operation

---

## 📊 Data Integration

The bot uses MOCK data by default. To use real market data:

### Option 1: MetaTrader 5 (MT5)

```python
# Install MT5
pip install MetaTrader5

# In gold_signal_bot.py, replace get_xauusd_price():
import MetaTrader5 as mt5

def get_xauusd_price(self):
    if not mt5.initialize():
        return None
    
    symbol = "XAUUSD"
    tick = mt5.symbol_info_tick(symbol)
    
    return {
        'symbol': symbol,
        'bid': tick.bid,
        'ask': tick.ask,
        'timestamp': datetime.fromtimestamp(tick.time),
        'spread': tick.ask - tick.bid,
        'candles': self._get_mt5_candles(symbol)
    }
```

### Option 2: Alpha Vantage (Free API)

```python
# Get free API key from alphavantage.co
API_KEY = "your_api_key"

def get_xauusd_price(self):
    url = f"https://www.alphavantage.co/query?function=FX_INTRADAY&from_symbol=XAU&to_symbol=USD&interval=15min&apikey={API_KEY}"
    response = requests.get(url)
    data = response.json()
    # Parse and return...
```

### Option 3: Yahoo Finance (Free)

```python
pip install yfinance

import yfinance as yf

def get_xauusd_price(self):
    gold = yf.Ticker("GC=F")  # Gold futures
    hist = gold.history(period="1d", interval="15m")
    # Parse and return...
```

---

## 📈 Performance Monitoring

### Add Logging

```python
import logging

logging.basicConfig(
    filename='gold_bot.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# In signal generation:
logging.info(f"Signal generated: {signal['action']}")
```

### Track Signals

Create `signals.json` to log all signals:

```python
def save_signal(self, signal):
    with open('signals.json', 'a') as f:
        json.dump(signal, f)
        f.write('\n')
```

---

## ✅ Testing Checklist

Before going live:

- [ ] Bot token configured correctly
- [ ] Chat ID configured correctly
- [ ] Received startup message in Telegram
- [ ] Dependencies installed
- [ ] Bot runs without errors
- [ ] Received at least one signal (even if NO_TRADE)
- [ ] Stop/start works correctly
- [ ] Deployment method chosen
- [ ] Data source configured (if using real data)

---

## 🎯 Next Steps

1. **Test with paper trading** first
2. **Connect real market data** (MT5, API, etc.)
3. **Monitor for 1-2 weeks** before risking capital
4. **Keep a trading journal** of all signals
5. **Adjust parameters** based on performance
6. **Set up alerts** for critical errors

---

## ⚠️ Important Disclaimers

- This bot is a **decision support tool**, not financial advice
- **No guarantee of profits** - markets are unpredictable
- Always use **proper risk management**
- Never risk more than you can afford to lose
- **Test thoroughly** before live trading
- Past performance doesn't guarantee future results
- You are responsible for all trading decisions

---

## 📞 Support

For issues:
1. Check this guide first
2. Review error messages carefully
3. Test with MOCK data first
4. Verify Telegram configuration

---

**Version:** 1.0  
**Last Updated:** February 2024  
**License:** For personal use only

**Good luck and trade safely! 🍀**
