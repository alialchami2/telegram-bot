"""
GOLD AI SIGNAL BOT - Professional XAUUSD Trading System
Version: 1.0
Author: Senior Quant Trading Architect
WARNING: This is a decision support tool, not financial advice
"""

import os
import json
import time
import requests
from datetime import datetime, timedelta
import numpy as np
from typing import Dict, List, Tuple, Optional

# ============================================================================
# CONFIGURATION
# ============================================================================

class BotConfig:
    """System configuration"""
    
    # Telegram Settings (YOU MUST FILL THESE)
    TELEGRAM_BOT_TOKEN = "8508743744:AAGsmHlMzQ9D4isoNRRWcygM5LZ1uB7jO2k"  # Get from @BotFather
    TELEGRAM_CHAT_ID = "1545914341"      # Your chat ID
    
    # Trading Parameters
    RISK_PERCENT = 2.0  # Max risk per trade
    MIN_CONFIDENCE = 65  # Minimum confidence to trade
    
    # Timeframes (in minutes)
    TIMEFRAMES = {
        'M15': 15,
        'H1': 60,
        'H4': 240,
        'D1': 1440
    }
    
    # Market Data APIs (examples - you'll need API keys)
    PRICE_API = "https://api.example.com/xauusd"  # Replace with real endpoint
    NEWS_API_KEY = "YOUR_NEWS_API_KEY"
    ECONOMIC_CAL_API = "YOUR_CALENDAR_API_KEY"
    
    # Risk Thresholds
    MAX_ATR_MULTIPLIER = 2.5  # Stop trading if ATR > normal * this
    MIN_VOLUME_THRESHOLD = 1000  # Minimum volume requirement
    
    # Session Times (UTC)
    LONDON_OPEN = 8
    NY_OPEN = 13
    ASIAN_CLOSE = 9


# ============================================================================
# DATA ACQUISITION MODULE
# ============================================================================

class MarketDataEngine:
    """Fetch and process market data"""
    
    def __init__(self):
        self.cache = {}
        self.last_update = None
    
    def get_xauusd_price(self) -> Dict:
        """
        Fetch current XAUUSD price and recent candles
        NOTE: Replace with your actual data provider (MT5, Alpha Vantage, etc.)
        """
        # MOCK DATA - Replace with real API call
        current_price = 2050.00 + np.random.randn() * 5
        
        return {
            'symbol': 'XAUUSD',
            'bid': current_price - 0.10,
            'ask': current_price + 0.10,
            'timestamp': datetime.utcnow(),
            'spread': 0.20,
            # Mock historical data for indicators
            'candles': self._generate_mock_candles(current_price)
        }
    
    def _generate_mock_candles(self, current_price: float, count: int = 200):
        """Generate mock candle data for testing"""
        candles = []
        price = current_price
        for i in range(count):
            change = np.random.randn() * 2
            price += change
            candles.append({
                'open': price,
                'high': price + abs(np.random.randn()),
                'low': price - abs(np.random.randn()),
                'close': price + change * 0.5,
                'volume': 1000 + np.random.randint(0, 500),
                'time': datetime.utcnow() - timedelta(minutes=15*i)
            })
        return list(reversed(candles))
    
    def get_dxy_index(self) -> float:
        """Get US Dollar Index (DXY)"""
        # MOCK - Replace with real API
        return 103.5 + np.random.randn() * 0.5
    
    def get_us10y_yield(self) -> float:
        """Get US 10-Year Treasury Yield"""
        # MOCK - Replace with real API
        return 4.25 + np.random.randn() * 0.1
    
    def get_risk_sentiment(self) -> str:
        """Determine market risk sentiment"""
        # MOCK - Should analyze VIX, equity indices, etc.
        sentiments = ['RISK_ON', 'RISK_OFF', 'NEUTRAL']
        return np.random.choice(sentiments)


# ============================================================================
# TECHNICAL ANALYSIS ENGINE
# ============================================================================

class TechnicalEngine:
    """Calculate technical indicators and market structure"""
    
    @staticmethod
    def calculate_ema(prices: List[float], period: int) -> float:
        """Calculate Exponential Moving Average"""
        if len(prices) < period:
            return np.mean(prices)
        
        multiplier = 2 / (period + 1)
        ema = prices[0]
        
        for price in prices[1:]:
            ema = (price * multiplier) + (ema * (1 - multiplier))
        
        return ema
    
    @staticmethod
    def calculate_rsi(prices: List[float], period: int = 14) -> float:
        """Calculate Relative Strength Index"""
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
        """Calculate MACD indicator"""
        ema12 = TechnicalEngine.calculate_ema(prices, 12)
        ema26 = TechnicalEngine.calculate_ema(prices, 26)
        macd_line = ema12 - ema26
        
        # Signal line (9-period EMA of MACD)
        signal_line = macd_line * 0.8  # Simplified
        histogram = macd_line - signal_line
        
        return {
            'macd': macd_line,
            'signal': signal_line,
            'histogram': histogram
        }
    
    @staticmethod
    def calculate_atr(candles: List[Dict], period: int = 14) -> float:
        """Calculate Average True Range (volatility)"""
        if len(candles) < period:
            return 1.0
        
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
    def detect_trend(candles: List[Dict]) -> str:
        """Detect market trend using EMAs"""
        closes = [c['close'] for c in candles]
        
        ema50 = TechnicalEngine.calculate_ema(closes, 50)
        ema200 = TechnicalEngine.calculate_ema(closes, 200)
        current_price = closes[-1]
        
        # Trend determination
        if current_price > ema50 > ema200:
            return "UPTREND"
        elif current_price < ema50 < ema200:
            return "DOWNTREND"
        else:
            return "RANGING"
    
    @staticmethod
    def find_support_resistance(candles: List[Dict]) -> Dict:
        """Identify key support and resistance levels"""
        highs = [c['high'] for c in candles[-50:]]
        lows = [c['low'] for c in candles[-50:]]
        
        resistance = np.percentile(highs, 90)
        support = np.percentile(lows, 10)
        
        return {
            'resistance': resistance,
            'support': support
        }


# ============================================================================
# NEWS & ECONOMIC CALENDAR MODULE
# ============================================================================

class NewsEngine:
    """Monitor economic news and events"""
    
    def __init__(self):
        self.high_impact_events = []
        self.news_cache = {}
    
    def check_economic_calendar(self) -> Dict:
        """
        Check for upcoming high-impact events
        Returns: {has_event: bool, events: list, time_to_event: minutes}
        """
        # MOCK - Replace with real economic calendar API
        # Example: forexfactory, investing.com API, etc.
        
        now = datetime.utcnow()
        
        # Mock upcoming events
        mock_events = [
            {
                'event': 'FOMC Meeting',
                'time': now + timedelta(hours=2),
                'impact': 'HIGH',
                'currency': 'USD'
            },
            {
                'event': 'CPI Data',
                'time': now + timedelta(days=1),
                'impact': 'HIGH',
                'currency': 'USD'
            }
        ]
        
        # Filter for high-impact USD events in next 4 hours
        upcoming = []
        for event in mock_events:
            time_diff = (event['time'] - now).total_seconds() / 60
            if 0 < time_diff < 240 and event['impact'] == 'HIGH':
                upcoming.append({
                    'event': event['event'],
                    'minutes_away': int(time_diff)
                })
        
        return {
            'has_high_impact': len(upcoming) > 0,
            'events': upcoming,
            'safe_to_trade': len(upcoming) == 0
        }
    
    def get_news_sentiment(self) -> Dict:
        """
        Analyze recent news sentiment for gold
        Returns: sentiment score and summary
        """
        # MOCK - Use real news API (NewsAPI, Bloomberg, etc.)
        sentiments = ['BULLISH', 'BEARISH', 'NEUTRAL']
        
        return {
            'sentiment': np.random.choice(sentiments),
            'confidence': np.random.uniform(0.5, 0.9),
            'summary': 'Gold supported by geopolitical tensions and Fed policy uncertainty'
        }


# ============================================================================
# RISK MANAGEMENT ENGINE
# ============================================================================

class RiskEngine:
    """Advanced risk assessment and position sizing"""
    
    def __init__(self, config: BotConfig):
        self.config = config
        self.daily_trades = 0
        self.daily_reset = datetime.utcnow().date()
    
    def assess_market_risk(self, market_data: Dict, tech_data: Dict) -> Dict:
        """
        Comprehensive market risk assessment
        Returns: risk_level, can_trade, reasons
        """
        risks = []
        risk_score = 0
        
        # Check volatility
        atr = tech_data.get('atr', 0)
        normal_atr = 10.0  # Typical gold ATR
        
        if atr > normal_atr * self.config.MAX_ATR_MULTIPLIER:
            risks.append("EXTREME_VOLATILITY")
            risk_score += 40
        elif atr > normal_atr * 1.5:
            risks.append("HIGH_VOLATILITY")
            risk_score += 20
        
        # Check spread
        spread = market_data.get('spread', 0)
        if spread > 0.50:
            risks.append("WIDE_SPREAD")
            risk_score += 15
        
        # Check volume
        avg_volume = np.mean([c['volume'] for c in market_data['candles'][-20:]])
        if avg_volume < self.config.MIN_VOLUME_THRESHOLD:
            risks.append("LOW_LIQUIDITY")
            risk_score += 25
        
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
            'reasons': ', '.join(risks) if risks else 'Normal conditions'
        }
    
    def calculate_position_size(self, entry: float, stop_loss: float, 
                               account_balance: float = 10000) -> Dict:
        """
        Calculate position size based on risk percentage
        """
        risk_amount = account_balance * (self.config.RISK_PERCENT / 100)
        pip_risk = abs(entry - stop_loss)
        
        # Gold: 1 lot = $100 per pip (simplified)
        position_size = risk_amount / (pip_risk * 100)
        position_size = round(position_size, 2)
        
        return {
            'lots': position_size,
            'risk_amount': risk_amount,
            'pip_risk': pip_risk
        }
    
    def check_trading_session(self) -> Dict:
        """Check if we're in a good trading session"""
        current_hour = datetime.utcnow().hour
        
        # Best sessions: London + NY overlap
        if self.config.LONDON_OPEN <= current_hour < self.config.NY_OPEN + 4:
            return {'session': 'LONDON_NY_OVERLAP', 'quality': 'HIGH'}
        elif current_hour >= self.config.ASIAN_CLOSE:
            return {'session': 'ACTIVE', 'quality': 'MEDIUM'}
        else:
            return {'session': 'ASIAN', 'quality': 'LOW'}


# ============================================================================
# SIGNAL GENERATION ENGINE
# ============================================================================

class SignalEngine:
    """Core signal generation logic"""
    
    def __init__(self, config: BotConfig):
        self.config = config
        self.market_data = MarketDataEngine()
        self.technical = TechnicalEngine()
        self.news = NewsEngine()
        self.risk = RiskEngine(config)
    
    def generate_signal(self) -> Dict:
        """
        Main signal generation pipeline
        Returns: Complete signal with all metadata
        """
        # Step 1: Get market data
        price_data = self.market_data.get_xauusd_price()
        dxy = self.market_data.get_dxy_index()
        us10y = self.market_data.get_us10y_yield()
        risk_sentiment = self.market_data.get_risk_sentiment()
        
        # Step 2: Calculate technical indicators
        candles = price_data['candles']
        closes = [c['close'] for c in candles]
        
        tech_analysis = {
            'trend': self.technical.detect_trend(candles),
            'rsi': self.technical.calculate_rsi(closes),
            'macd': self.technical.calculate_macd(closes),
            'atr': self.technical.calculate_atr(candles),
            'levels': self.technical.find_support_resistance(candles),
            'ema50': self.technical.calculate_ema(closes, 50),
            'ema200': self.technical.calculate_ema(closes, 200)
        }
        
        # Step 3: Check news and events
        calendar = self.news.check_economic_calendar()
        news_sentiment = self.news.get_news_sentiment()
        
        # Step 4: Risk assessment
        risk_assessment = self.risk.assess_market_risk(price_data, tech_analysis)
        session_quality = self.risk.check_trading_session()
        
        # Step 5: Decision logic
        signal = self._make_trading_decision(
            price_data, tech_analysis, calendar, 
            news_sentiment, risk_assessment, session_quality,
            dxy, us10y, risk_sentiment
        )
        
        return signal
    
    def _make_trading_decision(self, price_data, tech, calendar, 
                               news, risk, session, dxy, us10y, 
                               risk_sentiment) -> Dict:
        """
        Core decision logic - Multi-factor analysis
        """
        current_price = price_data['bid']
        
        # CRITICAL FILTERS - Stop trading conditions
        if calendar['has_high_impact']:
            return self._no_trade_signal(
                "HIGH_IMPACT_NEWS",
                f"Upcoming event: {calendar['events'][0]['event']} in {calendar['events'][0]['minutes_away']} min"
            )
        
        if not risk['can_trade']:
            return self._stop_trading_signal(
                f"Market risk too high: {risk['reasons']}"
            )
        
        if session['quality'] == 'LOW':
            return self._no_trade_signal(
                "POOR_SESSION",
                "Asian session - low liquidity, wait for London open"
            )
        
        # SIGNAL GENERATION
        confidence = 0
        reasons = []
        direction = None
        
        # Trend Analysis (30 points)
        if tech['trend'] == 'UPTREND':
            confidence += 30
            direction = 'BUY'
            reasons.append("Strong uptrend (EMA alignment)")
        elif tech['trend'] == 'DOWNTREND':
            confidence += 30
            direction = 'SELL'
            reasons.append("Strong downtrend (EMA alignment)")
        
        # RSI Analysis (20 points)
        rsi = tech['rsi']
        if direction == 'BUY' and 30 < rsi < 50:
            confidence += 20
            reasons.append(f"RSI oversold recovery ({rsi:.1f})")
        elif direction == 'SELL' and 50 < rsi < 70:
            confidence += 20
            reasons.append(f"RSI overbought rejection ({rsi:.1f})")
        elif rsi > 70 or rsi < 30:
            confidence -= 10
            reasons.append("RSI in extreme zone - caution")
        
        # MACD Confirmation (15 points)
        macd = tech['macd']
        if direction == 'BUY' and macd['histogram'] > 0:
            confidence += 15
            reasons.append("MACD bullish crossover")
        elif direction == 'SELL' and macd['histogram'] < 0:
            confidence += 15
            reasons.append("MACD bearish crossover")
        
        # Macro Factors (20 points)
        if direction == 'BUY':
            if dxy < 103:  # Weak dollar
                confidence += 10
                reasons.append(f"Weak USD (DXY: {dxy:.2f})")
            if risk_sentiment == 'RISK_OFF':
                confidence += 10
                reasons.append("Risk-off sentiment supports gold")
        elif direction == 'SELL':
            if dxy > 104:  # Strong dollar
                confidence += 10
                reasons.append(f"Strong USD (DXY: {dxy:.2f})")
            if risk_sentiment == 'RISK_ON':
                confidence += 10
                reasons.append("Risk-on sentiment pressures gold")
        
        # Support/Resistance (15 points)
        levels = tech['levels']
        if direction == 'BUY' and current_price > levels['support'] + 2:
            confidence += 15
            reasons.append(f"Price above support ({levels['support']:.2f})")
        elif direction == 'SELL' and current_price < levels['resistance'] - 2:
            confidence += 15
            reasons.append(f"Price below resistance ({levels['resistance']:.2f})")
        
        # Check minimum confidence
        if confidence < self.config.MIN_CONFIDENCE:
            return self._no_trade_signal(
                "LOW_CONFIDENCE",
                f"Signal confidence {confidence}% < {self.config.MIN_CONFIDENCE}% threshold"
            )
        
        # Generate trade signal
        if direction == 'BUY':
            return self._generate_buy_signal(
                current_price, tech, confidence, reasons, risk['risk_level']
            )
        elif direction == 'SELL':
            return self._generate_sell_signal(
                current_price, tech, confidence, reasons, risk['risk_level']
            )
        else:
            return self._no_trade_signal(
                "NO_CLEAR_DIRECTION",
                "Market ranging, no high-probability setup"
            )
    
    def _generate_buy_signal(self, entry, tech, confidence, reasons, risk_level):
        """Generate BUY signal with proper risk management"""
        atr = tech['atr']
        
        # Calculate stop loss and take profit
        stop_loss = entry - (1.5 * atr)
        take_profit_1 = entry + (2.0 * atr)
        take_profit_2 = entry + (3.5 * atr)
        
        return {
            'action': 'BUY',
            'entry': round(entry, 2),
            'stop_loss': round(stop_loss, 2),
            'take_profit_1': round(take_profit_1, 2),
            'take_profit_2': round(take_profit_2, 2),
            'risk_level': risk_level,
            'confidence': confidence,
            'market_state': tech['trend'],
            'reasons': reasons,
            'timestamp': datetime.utcnow(),
            'trade_type': 'INTRADAY',
            'status': 'ACTIVE'
        }
    
    def _generate_sell_signal(self, entry, tech, confidence, reasons, risk_level):
        """Generate SELL signal with proper risk management"""
        atr = tech['atr']
        
        stop_loss = entry + (1.5 * atr)
        take_profit_1 = entry - (2.0 * atr)
        take_profit_2 = entry - (3.5 * atr)
        
        return {
            'action': 'SELL',
            'entry': round(entry, 2),
            'stop_loss': round(stop_loss, 2),
            'take_profit_1': round(take_profit_1, 2),
            'take_profit_2': round(take_profit_2, 2),
            'risk_level': risk_level,
            'confidence': confidence,
            'market_state': tech['trend'],
            'reasons': reasons,
            'timestamp': datetime.utcnow(),
            'trade_type': 'INTRADAY',
            'status': 'ACTIVE'
        }
    
    def _no_trade_signal(self, reason_code, explanation):
        """Generate NO TRADE signal"""
        return {
            'action': 'NO_TRADE',
            'reason_code': reason_code,
            'explanation': explanation,
            'timestamp': datetime.utcnow(),
            'next_check': (datetime.utcnow() + timedelta(minutes=15)).strftime('%H:%M UTC'),
            'status': 'WAITING'
        }
    
    def _stop_trading_signal(self, reason):
        """Generate STOP TRADING signal"""
        return {
            'action': 'STOP_TRADING',
            'reason': reason,
            'timestamp': datetime.utcnow(),
            'resume_time': (datetime.utcnow() + timedelta(hours=1)).strftime('%H:%M UTC'),
            'status': 'SUSPENDED'
        }


# ============================================================================
# TELEGRAM NOTIFICATION MODULE
# ============================================================================

class TelegramBot:
    """Send formatted signals to Telegram"""
    
    def __init__(self, token: str, chat_id: str):
        self.token = token
        self.chat_id = chat_id
        self.base_url = f"https://api.telegram.org/bot{token}"
    
    def send_signal(self, signal: Dict):
        """Format and send signal to Telegram"""
        message = self._format_signal(signal)
        return self._send_message(message)
    
    def _format_signal(self, signal: Dict) -> str:
        """Format signal into professional message"""
        
        if signal['action'] == 'BUY':
            return self._format_trade_signal(signal, '🟢 BUY')
        elif signal['action'] == 'SELL':
            return self._format_trade_signal(signal, '🔴 SELL')
        elif signal['action'] == 'NO_TRADE':
            return self._format_no_trade(signal)
        elif signal['action'] == 'STOP_TRADING':
            return self._format_stop_trading(signal)
        else:
            return "⚠️ Unknown signal type"
    
    def _format_trade_signal(self, signal: Dict, header: str) -> str:
        """Format BUY/SELL signal"""
        reasons = '\n'.join([f"  • {r}" for r in signal['reasons']])
        
        message = f"""
{header} GOLD NOW

📊 ENTRY: ${signal['entry']}
🛑 STOP LOSS: ${signal['stop_loss']}
🎯 TAKE PROFIT 1: ${signal['take_profit_1']}
🎯 TAKE PROFIT 2: ${signal['take_profit_2']}

⚠️ RISK LEVEL: {signal['risk_level']}
✅ CONFIDENCE: {signal['confidence']}%
📈 MARKET STATE: {signal['market_state']}
⏱️ TYPE: {signal['trade_type']}

📋 ANALYSIS:
{reasons}

⏰ {signal['timestamp'].strftime('%Y-%m-%d %H:%M UTC')}

⚠️ RISK WARNING: This is decision support, not financial advice.
Manage your risk carefully.
"""
        return message.strip()
    
    def _format_no_trade(self, signal: Dict) -> str:
        """Format NO TRADE signal"""
        return f"""
⏸️ NO TRADE

Reason: {signal['explanation']}
Next Check: {signal['next_check']}

⏰ {signal['timestamp'].strftime('%Y-%m-%d %H:%M UTC')}
"""
    
    def _format_stop_trading(self, signal: Dict) -> str:
        """Format STOP TRADING signal"""
        return f"""
🚨 STOP TRADING

⚠️ {signal['reason']}

Resume Time: {signal['resume_time']}

⏰ {signal['timestamp'].strftime('%Y-%m-%d %H:%M UTC')}
"""
    
    def _send_message(self, text: str) -> bool:
        """Send message via Telegram API"""
        url = f"{self.base_url}/sendMessage"
        payload = {
            'chat_id': self.chat_id,
            'text': text,
            'parse_mode': 'HTML'
        }
        
        try:
            response = requests.post(url, json=payload, timeout=10)
            return response.status_code == 200
        except Exception as e:
            print(f"Telegram send error: {e}")
            return False


# ============================================================================
# MAIN BOT CONTROLLER
# ============================================================================

class GoldSignalBot:
    """Main bot orchestrator"""
    
    def __init__(self, config: BotConfig):
        self.config = config
        self.signal_engine = SignalEngine(config)
        self.telegram = TelegramBot(
            config.TELEGRAM_BOT_TOKEN,
            config.TELEGRAM_CHAT_ID
        )
        self.running = False
        self.last_signal = None
        self.last_price = None
        self.price_movement_threshold = 3.0  # Trigger analysis on $3+ move
    
    def start(self):
        """Start the bot (LIVE MONITORING - real-time analysis)"""
        print("🚀 Gold AI Signal Bot Starting...")
        print(f"⏰ Started at: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}")
        print("🔴 MODE: LIVE REAL-TIME MONITORING")
        print("=" * 60)
        
        self.running = True
        
        # Send startup notification
        self.telegram._send_message(
            "🤖 Gold AI Signal Bot ONLINE\n"
            "🔴 LIVE MODE: Real-time monitoring active\n"
            "📊 Analyzing every market tick for opportunities\n"
            f"Started: {datetime.utcnow().strftime('%H:%M UTC')}"
        )
        
        consecutive_checks = 0
        
        while self.running:
            try:
                # Quick price check first (efficient)
                current_price_data = self.signal_engine.market_data.get_xauusd_price()
                current_price = current_price_data['bid']
                
                # Determine if we need full analysis
                should_analyze = False
                
                if self.last_price is None:
                    should_analyze = True
                    reason = "Initial check"
                else:
                    price_change = abs(current_price - self.last_price)
                    
                    if price_change >= self.price_movement_threshold:
                        should_analyze = True
                        reason = f"Price moved ${price_change:.2f}"
                    elif consecutive_checks >= 20:  # Force check every 10 minutes (20 * 30sec)
                        should_analyze = True
                        reason = "Periodic full analysis"
                    else:
                        # Monitor but don't analyze
                        consecutive_checks += 1
                        print(f"💹 Live: ${current_price:.2f} | Change: ${price_change:.2f} | Check #{consecutive_checks}  ", end='\r')
                        time.sleep(30)
                        continue
                
                # Full analysis triggered
                print(f"\n🔍 ANALYZING: {reason}                                  ")
                signal = self.signal_engine.generate_signal()
                consecutive_checks = 0
                self.last_price = current_price
                
                # Check if signal changed (avoid spam)
                if self._should_send_signal(signal):
                    print(f"📡 NEW SIGNAL: {signal['action']} at ${current_price:.2f}")
                    success = self.telegram.send_signal(signal)
                    
                    if success:
                        print("✅ Signal sent to Telegram")
                        self.last_signal = signal
                    else:
                        print("❌ Failed to send signal")
                else:
                    print(f"⏸️  No signal change (current: {signal['action']})")
                
                # LIVE MODE: Continue monitoring
                time.sleep(30)  # 30 seconds between checks
                
            except KeyboardInterrupt:
                print("\n⏹️ Bot stopped by user")
                self.stop()
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                time.sleep(60)  # Wait 1 minute on error
    
    def _should_send_signal(self, signal: Dict) -> bool:
        """Determine if signal should be sent (live mode - more sensitive)"""
        if self.last_signal is None:
            return True
        
        # Send if action changed
        if signal['action'] != self.last_signal['action']:
            return True
        
        # For trade signals, send if entry changed by $2 or more (more sensitive for live mode)
        if signal['action'] in ['BUY', 'SELL']:
            if abs(signal['entry'] - self.last_signal['entry']) > 2:
                return True
            
            # Also send if confidence increased by 10% or more
            if signal['confidence'] - self.last_signal.get('confidence', 0) >= 10:
                return True
        
        return False
    
    def stop(self):
        """Stop the bot"""
        self.running = False
        self.telegram._send_message("🛑 Gold AI Signal Bot OFFLINE")


# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    print("""
    ╔═══════════════════════════════════════════════════╗
    ║     GOLD AI SIGNAL BOT - Professional Edition     ║
    ║              XAUUSD Trading System                ║
    ╚═══════════════════════════════════════════════════╝
    
    ⚠️  WARNING: This is a decision support tool
    ⚠️  NOT financial advice - Trade at your own risk
    
    """)
    
    # Initialize configuration
    config = BotConfig()
    
    # Validate configuration
    if config.TELEGRAM_BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("❌ ERROR: Please configure TELEGRAM_BOT_TOKEN in BotConfig")
        print("   1. Open Telegram and search for @BotFather")
        print("   2. Send /newbot and follow instructions")
        print("   3. Copy the token and paste it in BotConfig")
        exit(1)
    
    if config.TELEGRAM_CHAT_ID == "YOUR_CHAT_ID_HERE":
        print("❌ ERROR: Please configure TELEGRAM_CHAT_ID in BotConfig")
        print("   1. Open Telegram and search for @userinfobot")
        print("   2. Send /start to get your chat ID")
        print("   3. Copy the ID and paste it in BotConfig")
        exit(1)
    
    # Create and start bot
    bot = GoldSignalBot(config)
    
    try:
        bot.start()
    except Exception as e:
        print(f"Fatal error: {e}")
