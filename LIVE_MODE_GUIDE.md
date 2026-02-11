# 🔴 LIVE MODE GUIDE - Real-Time Signal Generation

## 🎯 What is Live Mode?

Your Gold AI Signal Bot now runs in **LIVE MODE**, which means:

- ✅ **Monitors markets every 30 seconds** (not every 15 minutes)
- ✅ **Triggers analysis on price movements** of $3 or more
- ✅ **Sends signals immediately** when entry conditions align
- ✅ **More responsive** to market changes
- ✅ **Detects opportunities faster**

---

## 🚀 How Live Mode Works

### Price Monitoring Loop

```
Every 30 seconds:
  1. Check current gold price
  2. Compare to last price
  
  IF price moved $3+ OR 10 minutes passed:
    → Run full technical analysis
    → Check macro factors
    → Assess risk
    → Generate signal if conditions align
    → Send to Telegram immediately
  
  ELSE:
    → Continue monitoring
    → Show live price on screen
```

---

## 📊 What You'll See

### Terminal Output (Live Monitoring)

When just monitoring (no signal):
```
💹 Live: $2050.45 | Change: $1.20 | Check #15
```

When price moves significantly:
```
🔍 ANALYZING: Price moved $3.40
📡 NEW SIGNAL: BUY at $2053.85
✅ Signal sent to Telegram
```

When no change in signal:
```
🔍 ANALYZING: Periodic full analysis
⏸️  No signal change (current: NO_TRADE)
```

---

## ⚡ Signal Triggers

### Immediate Full Analysis Happens When:

1. **Price Movement** - Gold moves $3+ from last analysis
2. **Periodic Check** - Every 10 minutes (forced)
3. **Confidence Change** - Signal confidence increases 10%+
4. **Entry Change** - Entry price shifts $2+

### Signals Are Sent When:

1. **Action Changes**
   - Was NO_TRADE → Now BUY
   - Was BUY → Now SELL
   - Was SELL → Now NO_TRADE

2. **Entry Price Shifts $2+**
   - BUY entry changed from $2050 → $2052

3. **Confidence Increases 10%+**
   - Was 65% confidence → Now 75%

---

## 🎛️ Customization

### Change Monitoring Frequency

In `gold_signal_bot.py`, find line ~850:

```python
time.sleep(30)  # 30 seconds between checks
```

**Options:**
- `15` = Every 15 seconds (very active)
- `30` = Every 30 seconds (balanced) ✅ **Current**
- `60` = Every 60 seconds (moderate)

### Change Price Movement Threshold

In `gold_signal_bot.py`, find line ~815:

```python
self.price_movement_threshold = 3.0  # Trigger analysis on $3+ move
```

**Options:**
- `1.0` = Very sensitive (analyzes often)
- `3.0` = Balanced ✅ **Current**
- `5.0` = Less sensitive (fewer analyses)
- `10.0` = Only major moves

### Change Signal Sensitivity

In `gold_signal_bot.py`, find line ~873:

```python
if abs(signal['entry'] - self.last_signal['entry']) > 2:
```

**Options:**
- `1` = Very sensitive (many signals)
- `2` = Balanced ✅ **Current**
- `5` = Less sensitive (fewer signals)

---

## 📈 Expected Behavior

### During Quiet Markets

```
💹 Live: $2050.23 | Change: $0.45 | Check #1
💹 Live: $2050.28 | Change: $0.50 | Check #2
💹 Live: $2050.19 | Change: $0.54 | Check #3
...
🔍 ANALYZING: Periodic full analysis
⏸️  No signal change (current: NO_TRADE)
```

### During Volatile Markets

```
💹 Live: $2050.23 | Change: $0.45 | Check #1
🔍 ANALYZING: Price moved $3.40
📡 NEW SIGNAL: BUY at $2053.63
✅ Signal sent to Telegram

💹 Live: $2054.15 | Change: $0.52 | Check #1
💹 Live: $2054.89 | Change: $1.26 | Check #2
🔍 ANALYZING: Price moved $3.12
⏸️  No signal change (current: BUY)
```

### When Opportunity Appears

```
🔍 ANALYZING: Price moved $4.20
📡 NEW SIGNAL: BUY at $2047.80
✅ Signal sent to Telegram

[Telegram Message]
🟢 BUY GOLD NOW

📊 ENTRY: $2047.80
🛑 STOP LOSS: $2032.80
🎯 TAKE PROFIT 1: $2067.80
🎯 TAKE PROFIT 2: $2085.30

⚠️ RISK LEVEL: LOW
✅ CONFIDENCE: 78%
📈 MARKET STATE: UPTREND

📋 ANALYSIS:
  • Strong uptrend (EMA alignment)
  • RSI oversold recovery (38.2)
  • MACD bullish crossover
  • Weak USD (DXY: 102.45)
  • Price above support (2044.00)

⏰ 2024-02-11 15:23 UTC
```

---

## ⚡ Performance Impact

### Resource Usage

**CPU:** Low to Moderate
- Price checks are lightweight
- Full analysis only on triggers
- ~2-5% CPU usage typical

**Memory:** ~100-200 MB RAM

**Network:** Minimal
- API calls only when triggered
- Telegram sends only on new signals

### Recommended Setup

**For Testing:**
- Run on your computer
- Monitor terminal output
- Adjust thresholds as needed

**For Production (24/7):**
- Use VPS (DigitalOcean, Vultr, AWS)
- Cost: $5-6/month
- Reliable internet connection
- See SETUP_GUIDE.md for deployment

---

## 🎯 Optimization Tips

### 1. Reduce False Signals

```python
# Increase minimum confidence
MIN_CONFIDENCE = 70  # Was 65

# Increase price threshold
self.price_movement_threshold = 5.0  # Was 3.0
```

### 2. Increase Responsiveness

```python
# Check more frequently
time.sleep(15)  # Was 30

# Lower price threshold
self.price_movement_threshold = 2.0  # Was 3.0
```

### 3. Balance Performance

```python
# Moderate settings (recommended)
time.sleep(30)
self.price_movement_threshold = 3.0
MIN_CONFIDENCE = 65
```

---

## 📊 Live Mode vs Periodic Mode

| Feature | Live Mode (Current) | Periodic Mode (Old) |
|---------|-------------------|-------------------|
| Check Frequency | Every 30 seconds | Every 15 minutes |
| Price Monitoring | Continuous | Periodic only |
| Analysis Trigger | Price movement | Time-based |
| Signal Speed | Immediate | Up to 15 min delay |
| Resource Usage | Moderate | Low |
| Best For | Active trading | Swing trading |

---

## 🛑 When to Use Each Mode

### Use Live Mode When:
- ✅ Trading intraday (scalping/day trading)
- ✅ Want immediate entry signals
- ✅ Monitoring volatile markets
- ✅ Have stable internet connection
- ✅ Running on VPS or always-on computer

### Use Periodic Mode When:
- ✅ Swing trading (multi-day positions)
- ✅ Want less frequent signals
- ✅ Limited resources (old computer)
- ✅ Unstable internet connection
- ✅ Prefer end-of-day analysis

**To Switch to Periodic Mode:**

Change line ~850 to:
```python
time.sleep(900)  # 15 minutes
```

And comment out the price movement logic.

---

## ⚠️ Important Notes

1. **Mock Data Warning**
   - Bot still uses MOCK data by default
   - Connect real data source for live signals
   - See SETUP_GUIDE.md for integration

2. **No Guarantees**
   - Faster signals ≠ better results
   - Always use stop losses
   - Manage risk properly

3. **Testing Required**
   - Paper trade first
   - Monitor for several days
   - Adjust settings to your style

4. **Internet Stability**
   - Live mode needs reliable connection
   - Consider VPS for 24/7 operation

---

## 🔧 Troubleshooting Live Mode

### Issue: Too Many Signals

**Solution:**
```python
# Increase thresholds
MIN_CONFIDENCE = 70
self.price_movement_threshold = 5.0
```

### Issue: Missing Signals

**Solution:**
```python
# Decrease thresholds
MIN_CONFIDENCE = 60
self.price_movement_threshold = 2.0
time.sleep(15)  # Check more often
```

### Issue: High CPU Usage

**Solution:**
```python
# Reduce frequency
time.sleep(60)  # Check every minute instead
```

### Issue: Bot Keeps Reanalyzing

**Cause:** Price moving frequently

**Solution:**
- Increase `price_movement_threshold`
- Or increase `time.sleep()` value

---

## 📝 Live Mode Checklist

Before running in live mode:

- [ ] Telegram bot configured and tested
- [ ] Internet connection stable
- [ ] Thresholds adjusted to your preference
- [ ] Connected to real data source (not mock)
- [ ] Risk management settings configured
- [ ] Paper trading account ready
- [ ] Trading journal prepared
- [ ] Stop loss strategy defined

---

## 🎓 Best Practices

1. **Start Conservative**
   - Higher confidence threshold (70%)
   - Larger price movement trigger ($5)
   - Paper trade for 2 weeks

2. **Monitor Performance**
   - Track all signals in journal
   - Note false signals
   - Adjust thresholds based on results

3. **Gradual Optimization**
   - Change one setting at a time
   - Test for 3-5 days
   - Compare results

4. **Risk Management**
   - Never risk more than 2% per trade
   - Always use stop losses
   - Don't overtrade

---

## 📞 Summary

**Live Mode gives you:**
- ⚡ Faster signal generation
- 📊 Real-time price monitoring
- 🎯 Immediate entry opportunities
- 🔍 Continuous market analysis

**Remember:**
- Speed ≠ Profit
- Quality > Quantity
- Risk management is key
- Test thoroughly first

---

**Happy live trading! 🚀**

*Trade responsibly and never risk more than you can afford to lose.*
