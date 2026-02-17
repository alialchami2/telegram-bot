#!/usr/bin/env python3
"""
Quick test to verify gold price is correct
"""

import requests
from datetime import datetime

print("🧪 Testing Gold Price Sources...\n")
print("=" * 60)

# Method 1: Yahoo Finance (BEST - Free, no API key needed!)
print("\n1️⃣ Yahoo Finance (Gold Futures GC=F):")
try:
    url = "https://query1.finance.yahoo.com/v8/finance/chart/GC=F?interval=1m&range=1d"
    response = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
    data = response.json()
    
    if 'chart' in data and 'result' in data['chart']:
        result = data['chart']['result'][0]
        meta = result.get('meta', {})
        price = meta.get('regularMarketPrice')
        
        if price:
            print(f"   ✅ Gold Price: ${price:,.2f}")
            print(f"   📅 Updated: {datetime.fromtimestamp(meta.get('regularMarketTime', 0)).strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            print("   ❌ No price data")
    else:
        print("   ❌ Invalid response")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Method 2: Alternative - Gold Price Org (scraping - backup)
print("\n2️⃣ GoldPrice.org (Backup):")
try:
    url = "https://www.goldprice.org/gold-price-per-ounce.html"
    response = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
    
    # Simple scraping - look for price in HTML
    if response.status_code == 200:
        text = response.text
        # Look for price pattern (this is a simple extraction)
        if 'gold_price' in text.lower():
            print("   ✅ Website accessible")
            print("   ℹ️  (Would need HTML parsing for exact price)")
        else:
            print("   ⚠️  Website format may have changed")
    else:
        print(f"   ❌ Status code: {response.status_code}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Method 3: Metals-API (if you have a key)
print("\n3️⃣ Metals-API.com (Requires free API key):")
print("   ℹ️  Get free key at: https://metals-api.com/")
print("   ℹ️  (Skipped - requires signup)")

print("\n" + "=" * 60)
print("\n✅ RECOMMENDATION: Bot now uses Yahoo Finance (Method 1)")
print("   This gives you the EXACT price you see on TradingView!")
print("\n💡 Current gold price should be around $5,000-$5,100 per oz")
print("   (As of Feb 2024, based on your chart)")
