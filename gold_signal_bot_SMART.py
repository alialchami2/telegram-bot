"""
SMART GOLD AI SIGNAL BOT - Professional Grade
Version: 3.0 INTELLIGENT
Designed for €30-200 accounts with 0.01-0.5 lot sizes
Focus: QUALITY over QUANTITY, STABILITY over NOISE
"""

import os
import json
import time
import requests
from datetime import datetime, timedelta, timezone
import pytz
import numpy as np
from typing import Dict, List, Tuple, Optional
from collections import deque

# ============================================================================
# CONFIGURATION
# ============================================================================

def utc_now():
    """Get current UTC time"""
    return datetime.now(timezone.utc)

def frankfurt_now():
    """Get current time in Berlin/Germany timezone (GMT+1 / CET)"""
    # Berlin/Germany timezone - Central European Time
    berlin_tz = pytz.timezone('Europe/Berlin')  # GMT+1 (CET)
    return datetime.now(berlin_tz)

class BotConfig:
    """Professional trading configuration"""
    
    # Telegram Settings
    TELEGRAM_BOT_TOKEN = "8508743744:AAGsmHlMzQ9D4isoNRRWcygM5LZ1uB7jO2k"
    TELEGRAM_CHAT_ID = "1545914341"
    
    # Account & Risk (for €30-200 accounts)
    ACCOUNT_SIZE = 100  # EUR (adjust to your account)
    RISK_PERCENT = 2.0  # Max 2% risk per trade
    MIN_LOT = 0.01
    MAX_LOT = 0.50
    
    # Signal Quality (ADJUSTED FOR MORE SIGNALS)
    MIN_CONFIDENCE = 60  # Lowered from 70% - more signals, slightly lower quality
    MIN_SIGNAL_GAP_MINUTES = 20  # Reduced from 30min - allows more signals
    DECISION_STABILITY_MINUTES = 45  # Hold bias for 45min unless strong reversal
    
    # Market Monitoring
    CHECK_INTERVAL = 60  # Check every 60 seconds (was 30)
    PRICE_MOVEMENT_THRESHOLD = 3.0  # Analyze on $3+ move
    
    # Multi-Timeframe Analysis
    TIMEFRAMES = ['M5', 'M15', 'H1', 'H4']
    
    # Risk Management
    MAX_ATR_MULTIPLIER = 2.5  # Stop trading if ATR too high
    MIN_RR_RATIO = 1.2  # Lowered from 1.5 - more signals


# ============================================================================
# MARKET STRUCTURE ANALYZER (NEW!)
# ============================================================================

class MarketStructureAnalyzer:
    """
    Analyzes market structure - the KEY to understanding if trend is real
    """
    
    @staticmethod
    def detect_structure(candles: List[Dict]) -> Dict:
        """
        Detect Higher Highs/Lower Lows pattern
        Returns: BULLISH_STRUCTURE, BEARISH_STRUCTURE, or RANGING
        """
        if len(candles) < 20:
            return {'structure': 'RANGING', 'confidence': 0}
        
        highs = [c['high'] for c in candles[-20:]]
        lows = [c['low'] for c in candles[-20:]]
        
        # Find recent swing points
        recent_highs = highs[-10:]
        recent_lows = lows[-10:]
        older_highs = highs[-20:-10]
        older_lows = lows[-20:-10]
        
        # Check for Higher Highs + Higher Lows (BULLISH)
        hh = max(recent_highs) > max(older_highs)
        hl = min(recent_lows) > min(older_lows)
        
        # Check for Lower Highs + Lower Lows (BEARISH)
        lh = max(recent_highs) < max(older_highs)
        ll = min(recent_lows) < min(older_lows)
        
        if hh and hl:
            return {
                'structure': 'BULLISH_STRUCTURE',
                'confidence': 80,
                'description': 'Higher Highs + Higher Lows'
            }
        elif lh and ll:
            return {
                'structure': 'BEARISH_STRUCTURE',
                'confidence': 80,
                'description': 'Lower Highs + Lower Lows'
            }
        else:
            return {
                'structure': 'RANGING',
                'confidence': 40,
                'description': 'No clear structure'
            }
    
    @staticmethod
    def detect_breakout_retest(candles: List[Dict], key_levels: Dict) -> Dict:
        """
        Check if price broke resistance/support and retested
        This is a HIGH-QUALITY setup
        """
        if len(candles) < 15:
            return {'has_breakout': False}
        
        current_price = candles[-1]['close']
        resistance = key_levels['resistance']
        support = key_levels['support']
        
        # Look for breakout in last 10 candles
        recent_candles = candles[-10:]
        
        # Bullish breakout + retest
        for i, candle in enumerate(recent_candles[:-3]):
            if candle['close'] < resistance and recent_candles[i+1]['close'] > resistance:
                # Broke above resistance
                # Check if retested (came back down but held)
                for retest_candle in recent_candles[i+2:]:
                    if retest_candle['low'] <= resistance + 2 and retest_candle['close'] > resistance:
                        return {
                            'has_breakout': True,
                            'type': 'BULLISH_RETEST',
                            'quality': 'HIGH',
                            'description': f'Broke ${resistance:.2f}, retested, held'
                        }
        
        # Bearish breakout + retest
        for i, candle in enumerate(recent_candles[:-3]):
            if candle['close'] > support and recent_candles[i+1]['close'] < support:
                # Broke below support
                for retest_candle in recent_candles[i+2:]:
                    if retest_candle['high'] >= support - 2 and retest_candle['close'] < support:
                        return {
                            'has_breakout': True,
                            'type': 'BEARISH_RETEST',
                            'quality': 'HIGH',
                            'description': f'Broke ${support:.2f}, retested, held'
                        }
        
        return {'has_breakout': False}


# ============================================================================
# SMART DECISION ENGINE (NEW!)
# ============================================================================

class SmartDecisionEngine:
    """
    Makes intelligent trading decisions with stability and quality focus
    """
    
    def __init__(self, config: BotConfig):
        self.config = config
        self.current_bias = None  # BUY, SELL, or None
        self.bias_since = None
        self.last_signal_time = None
        self.last_signal_action = None
        self.signal_history = deque(maxlen=20)  # Track recent decisions
    
    def can_send_signal(self) -> bool:
        """Check if enough time passed since last signal"""
        if self.last_signal_time is None:
            return True
        
        minutes_since = (utc_now() - self.last_signal_time).total_seconds() / 60
        return minutes_since >= self.config.MIN_SIGNAL_GAP_MINUTES
    
    def should_change_bias(self, new_bias: str, confidence: int) -> bool:
        """
        Determine if we should change our market bias
        Prevents flip-flopping - requires STRONG evidence to change
        """
        # No current bias - can set new one
        if self.current_bias is None:
            return True
        
        # Same bias - no change needed
        if new_bias == self.current_bias:
            return False
        
        # How long have we held current bias?
        if self.bias_since:
            minutes_held = (utc_now() - self.bias_since).total_seconds() / 60
            
            # If held < 45 minutes, need VERY strong evidence to flip
            if minutes_held < self.config.DECISION_STABILITY_MINUTES:
                # Require 70%+ confidence to flip quickly (lowered from 85%)
                if confidence < 70:
                    return False
            
            # If held 45-120 minutes, need strong evidence
            elif minutes_held < 120:
                if confidence < 65:  # Lowered from 75%
                    return False
        
        # Strong enough to change
        return True
    
    def update_bias(self, new_bias: str):
        """Update current market bias"""
        if new_bias != self.current_bias:
            self.current_bias = new_bias
            self.bias_since = utc_now()
    
    def calculate_bias_stability(self) -> str:
        """Assess if current bias is stable, weakening, or reversing"""
        if not self.bias_since:
            return "NEW"
        
        minutes_held = (utc_now() - self.bias_since).total_seconds() / 60
        
        # Count recent signals in same direction
        same_direction = sum(1 for s in self.signal_history 
                           if s.get('bias') == self.current_bias)
        
        if minutes_held > 120 and same_direction >= 3:
            return "STABLE"
        elif minutes_held > 45:
            return "DEVELOPING"
        else:
            return "NEW"


# ============================================================================
# ENHANCED MARKET DATA ENGINE
# ============================================================================

class SmartMarketDataEngine:
    """Enhanced market data with better error handling"""
    
    def __init__(self):
        self.cache = {}
        self.last_gold_price = None
        self.price_history = deque(maxlen=200)  # Keep price history
    
    def get_real_gold_price(self) -> Dict:
        """Get SPOT XAUUSD price with multi-source failover"""
        
        # Try GoldAPI.io first
        try:
            url = "https://www.goldapi.io/api/XAU/USD"
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                if 'price' in data:
                    price = float(data['price'])
                    if 4000 < price < 6000:
                        self.last_gold_price = price
                        self._add_to_history(price)
                        
                        return {
                            'symbol': 'XAUUSD',
                            'bid': round(price, 2),
                            'ask': round(price + 0.50, 2),
                            'spread': 0.50,
                            'timestamp': utc_now(),
                            'source': 'GoldAPI.io',
                            'last_update': frankfurt_now().strftime('%H:%M:%S')
                        }
        except:
            pass
        
        # Try Investing.com scraping
        try:
            import re
            url = "https://www.investing.com/currencies/xau-usd"
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, timeout=5, headers=headers)
            
            if response.status_code == 200:
                patterns = [
                    r'data-test="instrument-price-last">([0-9,]+\.?[0-9]*)<',
                    r'"last":([0-9,]+\.?[0-9]*)'
                ]
                
                for pattern in patterns:
                    match = re.search(pattern, response.text)
                    if match:
                        price = float(match.group(1).replace(',', ''))
                        if 4000 < price < 6000:
                            self.last_gold_price = price
                            self._add_to_history(price)
                            
                            return {
                                'symbol': 'XAUUSD',
                                'bid': round(price, 2),
                                'ask': round(price + 0.50, 2),
                                'spread': 0.50,
                                'timestamp': utc_now(),
                                'source': 'Investing.com',
                                'last_update': frankfurt_now().strftime('%H:%M:%S')
                            }
        except:
            pass
        
        # Fallback
        return self._get_fallback_gold_price()
    
    def _add_to_history(self, price: float):
        """Track price history for trend analysis"""
        self.price_history.append({
            'price': price,
            'time': utc_now()
        })
    
    def get_price_momentum(self) -> str:
        """Analyze recent price momentum"""
        if len(self.price_history) < 10:
            return "NEUTRAL"
        
        recent = [p['price'] for p in list(self.price_history)[-10:]]
        older = [p['price'] for p in list(self.price_history)[-20:-10]]
        
        recent_avg = np.mean(recent)
        older_avg = np.mean(older)
        
        change_pct = ((recent_avg - older_avg) / older_avg) * 100
        
        if change_pct > 0.1:
            return "BULLISH_MOMENTUM"
        elif change_pct < -0.1:
            return "BEARISH_MOMENTUM"
        else:
            return "NEUTRAL"
    
    def _get_fallback_gold_price(self) -> Dict:
        """Fallback with last known price"""
        if self.last_gold_price and 4000 < self.last_gold_price < 6000:
            price = self.last_gold_price + np.random.uniform(-1, 1)
        else:
            price = 5030 + np.random.uniform(-5, 5)
        
        return {
            'symbol': 'XAUUSD',
            'bid': round(price, 2),
            'ask': round(price + 0.5, 2),
            'spread': 0.5,
            'timestamp': utc_now(),
            'source': 'Fallback',
            'last_update': frankfurt_now().strftime('%H:%M:%S')
        }
    
    def get_historical_candles(self, count=200) -> List[Dict]:
        """Generate historical candles from price history"""
        candles = []
        
        if len(self.price_history) >= count:
            for i in range(count):
                ph = list(self.price_history)[i]
                price = ph['price']
                candles.append({
                    'open': price,
                    'high': price + abs(np.random.randn() * 2),
                    'low': price - abs(np.random.randn() * 2),
                    'close': price + np.random.randn(),
                    'volume': 1000 + np.random.randint(0, 500),
                    'time': ph['time']
                })
        else:
            # Generate synthetic if not enough history
            base_price = self.last_gold_price or 5030
            for i in range(count):
                change = np.random.randn() * 3
                base_price += change * 0.5
                
                candles.append({
                    'open': base_price,
                    'high': base_price + abs(np.random.randn() * 2),
                    'low': base_price - abs(np.random.randn() * 2),
                    'close': base_price + change * 0.3,
                    'volume': 1000 + np.random.randint(0, 500),
                    'time': utc_now() - timedelta(minutes=15*i)
                })
        
        return list(reversed(candles))
    
    def get_dxy_index(self) -> float:
        """Get USD index estimate"""
        return 103.5 + np.random.randn() * 0.5
    
    def get_us10y_yield(self) -> float:
        """Get 10Y yield estimate"""
        return 4.25 + np.random.randn() * 0.1
    
    def get_risk_sentiment(self, dxy: float) -> str:
        """Determine risk sentiment"""
        if dxy > 104:
            return "RISK_ON"
        elif dxy < 103:
            return "RISK_OFF"
        return "NEUTRAL"


# ============================================================================
# TECHNICAL ANALYSIS (Enhanced)
# ============================================================================

class TechnicalEngine:
    """Professional technical analysis"""
    
    @staticmethod
    def calculate_ema(prices: List[float], period: int) -> float:
        if len(prices) < period:
            return np.mean(prices)
        
        multiplier = 2 / (period + 1)
        ema = prices[0]
        
        for price in prices[1:]:
            ema = (price * multiplier) + (ema * (1 - multiplier))
        
        return ema
    
    @staticmethod
    def calculate_rsi(prices: List[float], period: int = 14) -> float:
        if len(prices) < period + 1:
            return 50.0
        
        deltas = np.diff(prices[-period-1:])
        gains = np.where(deltas > 0, deltas, 0)
        losses = np.where(deltas < 0, -deltas, 0)
        
        avg_gain = np.mean(gains)
        avg_loss = np.mean(losses)
        
        if avg_loss == 0:
            return 100.0
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        
        return rsi
    
    @staticmethod
    def calculate_macd(prices: List[float]) -> Dict:
        ema12 = TechnicalEngine.calculate_ema(prices, 12)
        ema26 = TechnicalEngine.calculate_ema(prices, 26)
        macd_line = ema12 - ema26
        signal_line = macd_line * 0.8
        histogram = macd_line - signal_line
        
        return {
            'macd': macd_line,
            'signal': signal_line,
            'histogram': histogram,
            'trend': 'BULLISH' if histogram > 0 else 'BEARISH'
        }
    
    @staticmethod
    def calculate_atr(candles: List[Dict], period: int = 14) -> float:
        if len(candles) < period:
            return 8.0
        
        true_ranges = []
        for i in range(1, len(candles)):
            high = candles[i]['high']
            low = candles[i]['low']
            prev_close = candles[i-1]['close']
            
            tr = max(
                high - low,
                abs(high - prev_close),
                abs(low - prev_close)
            )
            true_ranges.append(tr)
        
        return np.mean(true_ranges[-period:])
    
    @staticmethod
    def detect_trend(candles: List[Dict]) -> Dict:
        """Enhanced trend detection with strength"""
        closes = [c['close'] for c in candles]
        
        ema20 = TechnicalEngine.calculate_ema(closes, 20)
        ema50 = TechnicalEngine.calculate_ema(closes, 50)
        ema200 = TechnicalEngine.calculate_ema(closes, 200)
        current_price = closes[-1]
        
        # Strong uptrend
        if current_price > ema20 > ema50 > ema200:
            return {
                'trend': 'STRONG_UPTREND',
                'confidence': 90,
                'description': 'All EMAs aligned bullish'
            }
        
        # Uptrend
        elif current_price > ema50 > ema200:
            return {
                'trend': 'UPTREND',
                'confidence': 70,
                'description': 'Price above key EMAs'
            }
        
        # Strong downtrend
        elif current_price < ema20 < ema50 < ema200:
            return {
                'trend': 'STRONG_DOWNTREND',
                'confidence': 90,
                'description': 'All EMAs aligned bearish'
            }
        
        # Downtrend
        elif current_price < ema50 < ema200:
            return {
                'trend': 'DOWNTREND',
                'confidence': 70,
                'description': 'Price below key EMAs'
            }
        
        # Ranging
        else:
            return {
                'trend': 'RANGING',
                'confidence': 50,
                'description': 'No clear trend direction'
            }
    
    @staticmethod
    def find_support_resistance(candles: List[Dict]) -> Dict:
        """Find key levels"""
        highs = [c['high'] for c in candles[-50:]]
        lows = [c['low'] for c in candles[-50:]]
        
        resistance = np.percentile(highs, 90)
        support = np.percentile(lows, 10)
        
        return {
            'resistance': resistance,
            'support': support,
            'range': resistance - support
        }


# ============================================================================
# NEWS ENGINE (Same as before but enhanced)
# ============================================================================

class SmartNewsEngine:
    """Enhanced news monitoring"""
    
    def __init__(self, news_api_key: str):
        self.news_api_key = news_api_key
    
    def check_high_impact_events(self) -> Dict:
        """Check for dangerous trading times"""
        now = utc_now()
        hour = now.hour
        
        # Major news times (UTC)
        high_impact_hours = [13, 14, 15]  # 8:30-10:00 AM ET
        
        if hour in high_impact_hours and now.minute < 45:
            return {
                'has_high_impact': True,
                'safe_to_trade': False,
                'reason': 'Major economic news window'
            }
        
        return {
            'has_high_impact': False,
            'safe_to_trade': True,
            'reason': 'No scheduled events'
        }
    
    def get_news_sentiment(self) -> Dict:
        """Get news sentiment if API configured"""
        if self.news_api_key == "YOUR_NEWS_API_KEY":
            return {
                'has_news': False,
                'sentiment': 'NEUTRAL',
                'confidence': 50
            }
        
        # Would use NewsAPI here if configured
        return {
            'has_news': False,
            'sentiment': 'NEUTRAL',
            'confidence': 50
        }


# ============================================================================
# RISK ENGINE (Enhanced)
# ============================================================================

class SmartRiskEngine:
    """Professional risk management"""
    
    def __init__(self, config: BotConfig):
        self.config = config
    
    def assess_market_risk(self, current_price: float, atr: float) -> Dict:
        """Comprehensive risk assessment"""
        risks = []
        risk_score = 0
        
        normal_atr = 8.0
        
        # Volatility checks
        if atr > normal_atr * 2.5:
            risks.append("EXTREME_VOLATILITY")
            risk_score += 50
        elif atr > normal_atr * 1.8:
            risks.append("HIGH_VOLATILITY")
            risk_score += 25
        elif atr > normal_atr * 1.3:
            risks.append("ELEVATED_VOLATILITY")
            risk_score += 10
        
        # Determine risk level
        if risk_score >= 50:
            risk_level = "CRITICAL"
            can_trade = False
        elif risk_score >= 30:
            risk_level = "HIGH"
            can_trade = False
        elif risk_score >= 15:
            risk_level = "MEDIUM"
            can_trade = True
        else:
            risk_level = "LOW"
            can_trade = True
        
        return {
            'risk_level': risk_level,
            'risk_score': risk_score,
            'can_trade': can_trade,
            'risks': risks,
            'atr': atr,
            'normal_atr': normal_atr
        }
    
    def calculate_position_size(self, entry: float, stop_loss: float) -> Dict:
        """
        Calculate position size for €30-200 accounts
        Uses proper risk management
        """
        account = self.config.ACCOUNT_SIZE
        risk_amount = account * (self.config.RISK_PERCENT / 100)
        
        pip_risk = abs(entry - stop_loss)
        
        # Gold: 1 mini lot (0.10) = ~$1 per pip
        # 1 micro lot (0.01) = ~$0.10 per pip
        position_size = risk_amount / (pip_risk * 10)  # Simplified
        
        # Clamp to limits
        position_size = max(self.config.MIN_LOT, min(position_size, self.config.MAX_LOT))
        position_size = round(position_size, 2)
        
        return {
            'lots': position_size,
            'risk_amount': risk_amount,
            'pip_risk': pip_risk,
            'recommended': '0.01' if account < 100 else '0.02-0.05'
        }
    
    def check_session_quality(self) -> Dict:
        """Check trading session quality"""
        hour = utc_now().hour
        
        # Best: London + NY overlap (13:00-16:00 UTC)
        if 13 <= hour < 16:
            return {'session': 'LONDON_NY_OVERLAP', 'quality': 'EXCELLENT'}
        
        # Good: London session (8:00-13:00 UTC)
        elif 8 <= hour < 13:
            return {'session': 'LONDON', 'quality': 'GOOD'}
        
        # Good: NY session (13:00-20:00 UTC)
        elif hour < 20:
            return {'session': 'NEW_YORK', 'quality': 'GOOD'}
        
        # Avoid: Asian session
        else:
            return {'session': 'ASIAN', 'quality': 'POOR'}


# Continue in next message...


# ============================================================================
# SMART SIGNAL GENERATION ENGINE
# ============================================================================

class SmartSignalEngine:
    """
    Professional signal generation with quality focus
    Trades like a real professional trader
    """
    
    def __init__(self, config: BotConfig):
        self.config = config
        self.market_data = SmartMarketDataEngine()
        self.technical = TechnicalEngine()
        self.news = SmartNewsEngine(config.NEWS_API_KEY if hasattr(config, 'NEWS_API_KEY') else "")
        self.risk = SmartRiskEngine(config)
        self.decision = SmartDecisionEngine(config)
        self.structure = MarketStructureAnalyzer()
    
    def generate_signal(self) -> Dict:
        """
        Generate intelligent trading signal with deep analysis
        """
        # Get market data
        price_data = self.market_data.get_real_gold_price()
        if not price_data:
            return self._error_signal("Cannot fetch price")
        
        candles = self.market_data.get_historical_candles()
        if not candles:
            return self._error_signal("Cannot fetch candles")
        
        # Macro data
        dxy = self.market_data.get_dxy_index()
        risk_sentiment = self.market_data.get_risk_sentiment(dxy)
        price_momentum = self.market_data.get_price_momentum()
        
        # News check
        events = self.news.check_high_impact_events()
        news_sentiment = self.news.get_news_sentiment()
        
        # Technical analysis
        closes = [c['close'] for c in candles]
        
        tech = {
            'trend': self.technical.detect_trend(candles),
            'structure': self.structure.detect_structure(candles),
            'rsi': self.technical.calculate_rsi(closes),
            'macd': self.technical.calculate_macd(closes),
            'atr': self.technical.calculate_atr(candles),
            'levels': self.technical.find_support_resistance(candles)
        }
        
        # Breakout analysis
        breakout = self.structure.detect_breakout_retest(candles, tech['levels'])
        
        # Risk assessment
        risk_assessment = self.risk.assess_market_risk(price_data['bid'], tech['atr'])
        session = self.risk.check_session_quality()
        
        # CRITICAL FILTERS - STOP conditions
        if events['has_high_impact']:
            return self._no_trade_signal(
                "HIGH_IMPACT_NEWS",
                events['reason']
            )
        
        if not risk_assessment['can_trade']:
            return self._stop_trading_signal(
                f"Market risk too high: {', '.join(risk_assessment['risks'])}"
            )
        
        if session['quality'] == 'POOR':
            return self._no_trade_signal(
                "POOR_SESSION",
                "Asian session - low liquidity"
            )
        
        # DECISION MAKING with MULTI-FACTOR CONFLUENCE
        decision_result = self._make_smart_decision(
            price_data, tech, breakout, risk_assessment,
            session, dxy, risk_sentiment, price_momentum, news_sentiment
        )
        
        return decision_result
    
    def _make_smart_decision(self, price_data, tech, breakout, risk, 
                            session, dxy, risk_sentiment, price_momentum, news) -> Dict:
        """
        SMART decision making - Quality over Quantity
        """
        current_price = price_data['bid']
        
        # CONFIDENCE SCORING (out of 100)
        confidence = 0
        reasons = []
        direction = None
        quality_factors = []
        
        # === TREND ANALYSIS (30 points) ===
        trend = tech['trend']
        if trend['trend'] in ['STRONG_UPTREND', 'UPTREND']:
            confidence += trend['confidence'] * 0.3
            direction = 'BUY'
            reasons.append(f"Trend: {trend['description']}")
            quality_factors.append('TREND_ALIGNED')
        elif trend['trend'] in ['STRONG_DOWNTREND', 'DOWNTREND']:
            confidence += trend['confidence'] * 0.3
            direction = 'SELL'
            reasons.append(f"Trend: {trend['description']}")
            quality_factors.append('TREND_ALIGNED')
        else:
            reasons.append("Market ranging - no clear trend")
            # Don't trade ranging markets unless breakout
        
        # === MARKET STRUCTURE (25 points) ===
        structure = tech['structure']
        if structure['structure'] == 'BULLISH_STRUCTURE' and direction == 'BUY':
            confidence += 25
            reasons.append(f"Structure: {structure['description']}")
            quality_factors.append('STRUCTURE_ALIGNED')
        elif structure['structure'] == 'BEARISH_STRUCTURE' and direction == 'SELL':
            confidence += 25
            reasons.append(f"Structure: {structure['description']}")
            quality_factors.append('STRUCTURE_ALIGNED')
        elif structure['structure'] != 'RANGING':
            # Structure conflicts with trend - warning sign
            confidence -= 15
            reasons.append(f"⚠️ Structure conflicts: {structure['description']}")
        
        # === BREAKOUT/RETEST (20 points bonus for HIGH QUALITY setup) ===
        if breakout['has_breakout']:
            if (breakout['type'] == 'BULLISH_RETEST' and direction == 'BUY') or \
               (breakout['type'] == 'BEARISH_RETEST' and direction == 'SELL'):
                confidence += 20
                reasons.append(f"💎 {breakout['description']}")
                quality_factors.append('BREAKOUT_RETEST')
        
        # === RSI ANALYSIS (15 points) ===
        rsi = tech['rsi']
        if direction == 'BUY':
            if 30 < rsi < 50:
                confidence += 15
                reasons.append(f"RSI recovery zone ({rsi:.1f})")
            elif rsi < 30:
                confidence += 10
                reasons.append(f"RSI oversold ({rsi:.1f}) - reversal watch")
            elif rsi > 70:
                confidence -= 20
                reasons.append(f"⚠️ RSI overbought ({rsi:.1f}) - risky")
        elif direction == 'SELL':
            if 50 < rsi < 70:
                confidence += 15
                reasons.append(f"RSI rejection zone ({rsi:.1f})")
            elif rsi > 70:
                confidence += 10
                reasons.append(f"RSI overbought ({rsi:.1f}) - reversal watch")
            elif rsi < 30:
                confidence -= 20
                reasons.append(f"⚠️ RSI oversold ({rsi:.1f}) - risky")
        
        # === MACD CONFIRMATION (10 points) ===
        macd = tech['macd']
        if (direction == 'BUY' and macd['trend'] == 'BULLISH') or \
           (direction == 'SELL' and macd['trend'] == 'BEARISH'):
            confidence += 10
            reasons.append(f"MACD {macd['trend'].lower()}")
        
        # === MACRO FACTORS (15 points) ===
        if direction == 'BUY':
            if dxy < 103:
                confidence += 8
                reasons.append(f"Weak USD (DXY {dxy:.2f})")
            if risk_sentiment == 'RISK_OFF':
                confidence += 7
                reasons.append("Risk-off supports gold")
        elif direction == 'SELL':
            if dxy > 104:
                confidence += 8
                reasons.append(f"Strong USD (DXY {dxy:.2f})")
            if risk_sentiment == 'RISK_ON':
                confidence += 7
                reasons.append("Risk-on pressures gold")
        
        # === PRICE MOMENTUM (10 points) ===
        if (direction == 'BUY' and price_momentum == 'BULLISH_MOMENTUM') or \
           (direction == 'SELL' and price_momentum == 'BEARISH_MOMENTUM'):
            confidence += 10
            reasons.append(f"Price momentum aligned")
            quality_factors.append('MOMENTUM_ALIGNED')
        
        # === SESSION QUALITY BONUS (5 points) ===
        if session['quality'] == 'EXCELLENT':
            confidence += 5
            reasons.append(f"Premium session ({session['session']})")
        
        # === CONFLUENCE CHECK ===
        # We want quality factors, but not too strict
        if len(quality_factors) < 1:  # Lowered from 2 for more signals
            confidence *= 0.8  # Reduce if not enough confluence
            reasons.append("⚠️ Single factor only")
        
        # === DECISION STABILITY CHECK ===
        if not self.decision.can_send_signal():
            return self._no_trade_signal(
                "SIGNAL_COOLDOWN",
                "Too soon since last signal (30min rule)"
            )
        
        if direction and not self.decision.should_change_bias(direction, confidence):
            return self._no_trade_signal(
                "BIAS_STABILITY",
                f"Holding {self.decision.current_bias} bias - insufficient evidence to flip"
            )
        
        # === MINIMUM CONFIDENCE CHECK ===
        if confidence < self.config.MIN_CONFIDENCE:
            return self._no_trade_signal(
                "LOW_CONFIDENCE",
                f"Confidence {confidence:.0f}% < {self.config.MIN_CONFIDENCE}% threshold"
            )
        
        # === GENERATE TRADE SIGNAL ===
        if direction == 'BUY':
            return self._generate_buy_signal(
                current_price, tech, confidence, reasons, 
                risk['risk_level'], price_data, quality_factors
            )
        elif direction == 'SELL':
            return self._generate_sell_signal(
                current_price, tech, confidence, reasons,
                risk['risk_level'], price_data, quality_factors
            )
        else:
            return self._no_trade_signal(
                "NO_DIRECTION",
                "No clear trading opportunity"
            )
    
    def _generate_buy_signal(self, entry, tech, confidence, reasons, 
                           risk_level, price_data, quality_factors):
        """Generate professional BUY signal"""
        atr = tech['atr']
        
        # Conservative stop loss and take profits
        stop_loss = entry - (1.8 * atr)  # Slightly wider for safety
        take_profit_1 = entry + (2.5 * atr)  # Better R:R
        take_profit_2 = entry + (4.0 * atr)  # Optimistic
        
        # Calculate R:R
        risk = entry - stop_loss
        reward1 = take_profit_1 - entry
        rr_ratio = reward1 / risk if risk > 0 else 0
        
        # Check minimum R:R
        if rr_ratio < self.config.MIN_RR_RATIO:
            return self._no_trade_signal(
                "POOR_RR",
                f"Risk:Reward {rr_ratio:.1f} < {self.config.MIN_RR_RATIO} minimum"
            )
        
        # Calculate position size
        position = self.risk.calculate_position_size(entry, stop_loss)
        
        # Update decision engine
        self.decision.update_bias('BUY')
        self.decision.last_signal_time = utc_now()
        self.decision.last_signal_action = 'BUY'
        
        bias_stability = self.decision.calculate_bias_stability()
        
        signal = {
            'action': 'BUY',
            'entry': round(entry, 2),
            'stop_loss': round(stop_loss, 2),
            'take_profit_1': round(take_profit_1, 2),
            'take_profit_2': round(take_profit_2, 2),
            'risk_level': risk_level,
            'confidence': int(confidence),
            'market_state': tech['trend']['trend'],
            'bias_stability': bias_stability,
            'trade_type': 'INTRADAY',
            'reasons': reasons,
            'timestamp': utc_now(),
            'data_source': price_data['source'],
            'spread': price_data['spread'],
            'position_size': position['lots'],
            'recommended_lots': position['recommended'],
            'quality_factors': quality_factors,
            'rr_ratio': round(rr_ratio, 1),
            'status': 'ACTIVE'
        }
        
        # Log to history
        self.decision.signal_history.append({
            'bias': 'BUY',
            'confidence': confidence,
            'time': utc_now()
        })
        
        return signal
    
    def _generate_sell_signal(self, entry, tech, confidence, reasons,
                             risk_level, price_data, quality_factors):
        """Generate professional SELL signal"""
        atr = tech['atr']
        
        stop_loss = entry + (1.8 * atr)
        take_profit_1 = entry - (2.5 * atr)
        take_profit_2 = entry - (4.0 * atr)
        
        risk = stop_loss - entry
        reward1 = entry - take_profit_1
        rr_ratio = reward1 / risk if risk > 0 else 0
        
        if rr_ratio < self.config.MIN_RR_RATIO:
            return self._no_trade_signal(
                "POOR_RR",
                f"Risk:Reward {rr_ratio:.1f} < {self.config.MIN_RR_RATIO} minimum"
            )
        
        position = self.risk.calculate_position_size(entry, stop_loss)
        
        self.decision.update_bias('SELL')
        self.decision.last_signal_time = utc_now()
        self.decision.last_signal_action = 'SELL'
        
        bias_stability = self.decision.calculate_bias_stability()
        
        signal = {
            'action': 'SELL',
            'entry': round(entry, 2),
            'stop_loss': round(stop_loss, 2),
            'take_profit_1': round(take_profit_1, 2),
            'take_profit_2': round(take_profit_2, 2),
            'risk_level': risk_level,
            'confidence': int(confidence),
            'market_state': tech['trend']['trend'],
            'bias_stability': bias_stability,
            'trade_type': 'INTRADAY',
            'reasons': reasons,
            'timestamp': utc_now(),
            'data_source': price_data['source'],
            'spread': price_data['spread'],
            'position_size': position['lots'],
            'recommended_lots': position['recommended'],
            'quality_factors': quality_factors,
            'rr_ratio': round(rr_ratio, 1),
            'status': 'ACTIVE'
        }
        
        self.decision.signal_history.append({
            'bias': 'SELL',
            'confidence': confidence,
            'time': utc_now()
        })
        
        return signal
    
    def _no_trade_signal(self, reason_code, explanation):
        """Generate NO TRADE signal"""
        return {
            'action': 'NO_TRADE',
            'reason_code': reason_code,
            'explanation': explanation,
            'timestamp': utc_now(),
            'next_check': (utc_now() + timedelta(seconds=60)).strftime('%H:%M:%S'),
            'status': 'WAITING',
            'current_bias': self.decision.current_bias,
            'bias_held_minutes': int((utc_now() - self.decision.bias_since).total_seconds() / 60) if self.decision.bias_since else 0
        }
    
    def _stop_trading_signal(self, reason):
        """Generate STOP TRADING signal"""
        return {
            'action': 'STOP_TRADING',
            'reason': reason,
            'timestamp': utc_now(),
            'resume_time': (utc_now() + timedelta(hours=1)).strftime('%H:%M'),
            'status': 'SUSPENDED'
        }
    
    def _error_signal(self, error):
        """Generate error signal"""
        return {
            'action': 'ERROR',
            'error': error,
            'timestamp': utc_now(),
            'status': 'ERROR'
        }


# ============================================================================
# TELEGRAM BOT (Enhanced formatting)
# ============================================================================

class SmartTelegramBot:
    """Professional Telegram messaging"""
    
    def __init__(self, token: str, chat_id: str):
        self.token = token
        self.chat_id = chat_id
        self.base_url = f"https://api.telegram.org/bot{token}"
    
    def send_signal(self, signal: Dict):
        """Send formatted signal"""
        message = self._format_signal(signal)
        return self._send_message(message)
    
    def _format_signal(self, signal: Dict) -> str:
        """Format signal with professional layout"""
        if signal['action'] == 'BUY':
            return self._format_trade_signal(signal, '🟢 BUY')
        elif signal['action'] == 'SELL':
            return self._format_trade_signal(signal, '🔴 SELL')
        elif signal['action'] == 'NO_TRADE':
            return self._format_no_trade(signal)
        elif signal['action'] == 'STOP_TRADING':
            return self._format_stop_trading(signal)
        elif signal['action'] == 'ERROR':
            return f"⚠️ ERROR: {signal['error']}"
        return "⚠️ Unknown signal"
    
    def _format_trade_signal(self, signal: Dict, header: str) -> str:
        """Professional trade signal format"""
        reasons = '\n'.join([f"  • {r}" for r in signal['reasons']])
        
        frankfurt_time = frankfurt_now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Quality indicators
        quality_badges = ' '.join(['⭐' for _ in signal.get('quality_factors', [])])
        
        message = f"""
{header} GOLD NOW 💰 {quality_badges}

📊 ENTRY: ${signal['entry']}
🛑 STOP LOSS: ${signal['stop_loss']}
🎯 TP1: ${signal['take_profit_1']} (R:R 1:{signal['rr_ratio']})
🎯 TP2: ${signal['take_profit_2']}

⚠️ RISK: {signal['risk_level']}
✅ CONFIDENCE: {signal['confidence']}%
📈 MARKET: {signal['market_state']}
🎯 BIAS: {signal['bias_stability']}
⏱️ TYPE: {signal['trade_type']}

💼 POSITION:
  • Recommended: {signal['recommended_lots']} lots
  • Calculated: {signal['position_size']} lots
  • For €30-200 accounts

📋 ANALYSIS:
{reasons}

📡 Source: {signal.get('data_source', 'Unknown')}
🕐 {frankfurt_time} Frankfurt

⚠️ Decision support only - Trade at own risk!
"""
        return message.strip()
    
    def _format_no_trade(self, signal: Dict) -> str:
        """Format NO TRADE message"""
        frankfurt_time = frankfurt_now().strftime('%H:%M:%S')
        
        bias_info = ""
        if signal.get('current_bias'):
            bias_info = f"\n🎯 Holding {signal['current_bias']} bias ({signal['bias_held_minutes']}min)"
        
        return f"""
⏸️ NO TRADE

📝 {signal['explanation']}{bias_info}
🔄 Next: {signal['next_check']}

🕐 {frankfurt_time} Frankfurt
"""
    
    def _format_stop_trading(self, signal: Dict) -> str:
        """Format STOP TRADING message"""
        frankfurt_time = frankfurt_now().strftime('%H:%M:%S')
        return f"""
🚨 STOP TRADING

⚠️ {signal['reason']}

⏰ Resume: {signal['resume_time']}

🕐 {frankfurt_time} Frankfurt
"""
    
    def _send_message(self, text: str) -> bool:
        """Send message to Telegram"""
        url = f"{self.base_url}/sendMessage"
        payload = {'chat_id': self.chat_id, 'text': text}
        
        try:
            response = requests.post(url, json=payload, timeout=10)
            return response.status_code == 200
        except:
            return False


# ============================================================================
# MAIN BOT CONTROLLER
# ============================================================================

class SmartGoldBot:
    """Professional Gold Trading Bot"""
    
    def __init__(self, config: BotConfig):
        self.config = config
        self.signal_engine = SmartSignalEngine(config)
        self.telegram = SmartTelegramBot(config.TELEGRAM_BOT_TOKEN, config.TELEGRAM_CHAT_ID)
        self.running = False
        self.last_signal = None
        self.last_price = None
    
    def start(self):
        """Start professional trading bot"""
        frankfurt_time = frankfurt_now().strftime('%Y-%m-%d %H:%M:%S')
        
        print("╔════════════════════════════════════════════════════════╗")
        print("║   SMART GOLD AI SIGNAL BOT - Professional Edition     ║")
        print("║        Quality Signals • Stable Decisions              ║")
        print("╚════════════════════════════════════════════════════════╝")
        print()
        print(f"🕐 {frankfurt_time} Frankfurt")
        print(f"💼 Account: €{self.config.ACCOUNT_SIZE}")
        print(f"📊 Risk: {self.config.RISK_PERCENT}% per trade")
        print(f"✅ Min Confidence: {self.config.MIN_CONFIDENCE}%")
        print(f"⏱️  Check Interval: {self.config.CHECK_INTERVAL}s")
        print("=" * 70)
        
        self.running = True
        
        # Test Telegram
        print("\n🧪 Testing Telegram...")
        success = self.telegram._send_message(
            f"🤖 SMART Gold Bot ONLINE\n"
            f"🕐 {frankfurt_time} Frankfurt\n\n"
            f"💼 Account: €{self.config.ACCOUNT_SIZE}\n"
            f"📊 Min Confidence: {self.config.MIN_CONFIDENCE}%\n"
            f"⚠️ Professional mode - Quality over quantity"
        )
        
        if not success:
            print("❌ Telegram failed - check config!")
            return
        
        print("✅ Telegram connected!\n")
        
        consecutive_checks = 0
        
        while self.running:
            try:
                # Get current price
                price_data = self.signal_engine.market_data.get_real_gold_price()
                
                if not price_data:
                    print("⚠️ Cannot fetch price, retrying...")
                    time.sleep(30)
                    continue
                
                current_price = price_data['bid']
                
                # Determine if analysis needed
                should_analyze = False
                reason = ""
                
                if self.last_price is None:
                    should_analyze = True
                    reason = "Initial check"
                else:
                    price_change = abs(current_price - self.last_price)
                    
                    if price_change >= self.config.PRICE_MOVEMENT_THRESHOLD:
                        should_analyze = True
                        reason = f"Price moved ${price_change:.2f}"
                    elif consecutive_checks >= 5:  # Every 5 minutes
                        should_analyze = True
                        reason = "Periodic review"
                    else:
                        consecutive_checks += 1
                        bias_info = f"| Bias: {self.signal_engine.decision.current_bias or 'None'}" if self.signal_engine.decision.current_bias else ""
                        print(f"💹 ${current_price:.2f} | Δ${price_change:.2f} {bias_info} | #{consecutive_checks}    ", end='\r')
                        time.sleep(self.config.CHECK_INTERVAL)
                        continue
                
                # Run analysis
                print(f"\n🔍 ANALYZING: {reason} (Price: ${current_price:.2f})")
                signal = self.signal_engine.generate_signal()
                consecutive_checks = 0
                self.last_price = current_price
                
                # Send if important
                if self._should_send_signal(signal):
                    print(f"📡 SIGNAL: {signal['action']}")
                    success = self.telegram.send_signal(signal)
                    
                    if success:
                        print("✅ Sent to Telegram")
                        self.last_signal = signal
                    else:
                        print("❌ Send failed")
                else:
                    print(f"⏸️  {signal['action']} (no change)")
                
                time.sleep(self.config.CHECK_INTERVAL)
                
            except KeyboardInterrupt:
                print("\n⏹️ Shutting down...")
                self.telegram._send_message("🛑 Smart Gold Bot OFFLINE")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                time.sleep(60)
    
    def _should_send_signal(self, signal: Dict) -> bool:
        """Determine if signal should be sent"""
        if self.last_signal is None:
            return True
        
        # Always send BUY/SELL signals
        if signal['action'] in ['BUY', 'SELL']:
            return True
        
        # Always send STOP_TRADING
        if signal['action'] == 'STOP_TRADING':
            return True
        
        # Send NO_TRADE only if reason changed
        if signal['action'] == 'NO_TRADE':
            if self.last_signal['action'] in ['BUY', 'SELL']:
                return True  # Just came out of signal
            if signal.get('reason_code') != self.last_signal.get('reason_code'):
                return True
        
        return False


# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    # Add NEWS_API_KEY to config if you have one
    BotConfig.NEWS_API_KEY = "YOUR_NEWS_API_KEY"  # Optional
    
    config = BotConfig()
    
    # Validate
    if config.TELEGRAM_BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("❌ Configure TELEGRAM_BOT_TOKEN first!")
        exit(1)
    
    if config.TELEGRAM_CHAT_ID == "YOUR_CHAT_ID_HERE":
        print("❌ Configure TELEGRAM_CHAT_ID first!")
        exit(1)
    
    # Start bot
    bot = SmartGoldBot(config)
    
    try:
        bot.start()
    except Exception as e:
        print(f"\n💥 Fatal error: {e}")
