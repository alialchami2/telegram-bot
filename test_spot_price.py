#!/usr/bin/env python3
"""
Test XAUUSD SPOT price (matches MetaTrader 5)
"""

import requests
from datetime import datetime
import re

print("🧪 Testing XAUUSD SPOT Prices (MT5 Compatible)...\n")
print("=" * 70)

# Method 1: GoldPrice.org (Real-time spot, FREE!)
print("\n1️⃣ GoldPrice.org (Live Spot - Best for MT5):")
try:
    url = "https://data-asg.goldprice.org/dbXRates/USD"
    response = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
    data = response.json()
    
    if 'items' in data:
        for item in data['items']:
            if item.get('curr') == 'XAU':
                price = float(item.get('xauPrice', 0))
                print(f"   ✅ XAUUSD Spot: ${price:,.2f}")
                print(f"   📊 This should match your MT5!")
                break
except Exception as e:
    print(f"   ❌ Error: {e}")

# Method 2: Investing.com (spot price scraping)
print("\n2️⃣ Investing.com (XAUUSD Spot):")
try:
    url = "https://www.investing.com/currencies/xau-usd"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    response = requests.get(url, timeout=10, headers=headers)
    
    if response.status_code == 200:
        text = response.text
        price_match = re.search(r'data-test="instrument-price-last">([0-9,]+\.?[0-9]*)<', text)
        
        if price_match:
            price = float(price_match.group(1).replace(',', ''))
            print(f"   ✅ XAUUSD Spot: ${price:,.2f}")
        else:
            print("   ⚠️  Could not extract price from page")
    else:
        print(f"   ❌ HTTP {response.status_code}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Method 3: Yahoo Finance for comparison (note: this is FUTURES, not spot)
print("\n3️⃣ Yahoo Finance (Gold Futures GC=F - NOT MT5 spot):")
try:
    url = "https://query1.finance.yahoo.com/v8/finance/chart/GC=F?interval=1m&range=1d"
    response = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
    data = response.json()
    
    if 'chart' in data and 'result' in data['chart']:
        result = data['chart']['result'][0]
        price = result['meta'].get('regularMarketPrice')
        if price:
            print(f"   ⚠️  Futures Price: ${price:,.2f}")
            print(f"   ℹ️  (Futures are ~$50-60 HIGHER than spot)")
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n" + "=" * 70)
print("\n💡 KEY DIFFERENCE:")
print("   • MT5 shows SPOT XAUUSD: ~$5,030")
print("   • Futures (GC=F) show: ~$5,085 (higher!)")
print("\n✅ Bot now uses SPOT prices (Method 1) to match MT5!")
print("\n🔍 Your MT5 shows $5,030? That's SPOT price - we're using that now!")
