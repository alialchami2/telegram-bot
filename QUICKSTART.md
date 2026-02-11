# ⚡ QUICK START GUIDE - Gold AI Signal Bot

## 🎯 Get Running in 5 Minutes

### Step 1: Get Telegram Credentials (2 minutes)

**Create Bot:**
1. Open Telegram → Search `@BotFather`
2. Send: `/newbot`
3. Name: `My Gold Signals`
4. Username: `my_gold_signals_bot` (must end with "bot")
5. **Copy the token** (looks like `123456789:ABC...xyz`)

**Get Your Chat ID:**
1. Search `@userinfobot` in Telegram
2. Send: `/start`
3. **Copy your ID** (looks like `987654321`)

**Start Your Bot:**
1. Find your bot in Telegram (search the username)
2. Click **START**

---

### Step 2: Install Bot (1 minute)

```bash
# Install Python dependencies
pip install numpy requests

# Or if you have the requirements file
pip install -r requirements.txt
```

---

### Step 3: Configure Bot (1 minute)

Open `gold_signal_bot.py` in any text editor and edit lines 25-26:

```python
# REPLACE THESE TWO LINES:
TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"  # ← Paste your bot token
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID_HERE"      # ← Paste your chat ID
```

**Example:**
```python
TELEGRAM_BOT_TOKEN = "6123456789:AAE7xMq_abcdefghijklmnop"
TELEGRAM_CHAT_ID = "987654321"
```

Save the file.

---

### Step 4: Run Bot (30 seconds)

```bash
python gold_signal_bot.py
```

**You should see:**
```
🚀 Gold AI Signal Bot Starting...
⏰ Started at: 2024-02-11 14:30 UTC
```

**And in Telegram:**
```
🤖 Gold AI Signal Bot ONLINE
Monitoring XAUUSD markets...
```

---

### Step 5: Wait for Signals

The bot will:
- Check markets every 15 minutes
- Send signals when opportunities appear
- Send NO_TRADE when conditions aren't right

**Example Signal:**
```
🟢 BUY GOLD NOW

📊 ENTRY: $2050.00
🛑 STOP LOSS: $2035.00
🎯 TAKE PROFIT: $2070.00

⚠️ RISK: MEDIUM
✅ CONFIDENCE: 75%
```

---

## 🛑 Stop Bot

Press `Ctrl+C` in the terminal

---

## 🔧 Common Issues

### "ERROR: Please configure TELEGRAM_BOT_TOKEN"
**Fix:** You didn't replace `YOUR_BOT_TOKEN_HERE` with your actual token

### "Telegram send error"
**Fix:** 
- Check token is correct (no spaces)
- Check chat ID is correct
- Make sure you clicked START in your bot

### "Module not found"
**Fix:** `pip install numpy requests`

---

## 🚀 Run 24/7 (Optional)

### On Linux/Mac:
```bash
# Use screen to keep it running
screen -S goldbot
python gold_signal_bot.py
# Press Ctrl+A then D to detach

# Reattach later
screen -r goldbot
```

### On Windows:
Just keep the terminal open, or use a VPS

---

## ⚙️ Customize Settings (Optional)

In `gold_signal_bot.py`, find `BotConfig` class:

```python
RISK_PERCENT = 2.0      # Change to 1.0 for less risk, 3.0 for more
MIN_CONFIDENCE = 65     # Change to 70 for fewer but stronger signals
```

---

## 📊 What To Expect

- **Signals per day:** 1-4 (quality over quantity)
- **NO_TRADE messages:** Very common (60-70% of checks)
- **False signals:** Possible - this is decision support, not magic
- **Win rate:** Not guaranteed - always use your judgment

---

## ⚠️ CRITICAL WARNINGS

1. **This is NOT financial advice** - it's a tool to help you decide
2. **Never risk more than you can afford to lose**
3. **Always use proper stop losses**
4. **Test with paper trading first**
5. **The bot uses MOCK data by default** - connect real data for live signals

---

## 🎓 Next Steps

1. Read `SETUP_GUIDE.md` for detailed configuration
2. Read `SYSTEM_ARCHITECTURE.md` to understand how it works
3. Connect real market data (MT5 or API)
4. Monitor performance for 1-2 weeks before risking capital
5. Keep a trading journal

---

## 📞 Need Help?

Check the full `SETUP_GUIDE.md` for:
- Detailed troubleshooting
- Data source integration
- Advanced deployment options
- Performance optimization

---

**That's it! You're ready to receive Gold signals. 🎯**

**Remember:** Trade responsibly and never risk more than you can afford to lose.

Good luck! 🍀
