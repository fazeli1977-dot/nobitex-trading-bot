"""
Configuration Management Module
Central settings for Nobitex Trading Bot
"""

import os
from dataclasses import dataclass
from typing import List
from pathlib import Path

# ============================================================================
# API & AUTHENTICATION SETTINGS
# ============================================================================
NOBITEX_API_BASE_URL = "https://api.nobitex.ir"
NOBITEX_MARGIN_API_BASE_URL = "https://margin.nobitex.ir"

# Secure credential management - Load from environment variables
NOBITEX_API_KEY = os.getenv("NOBITEX_API_KEY", "YOUR_API_KEY_HERE")
NOBITEX_API_SECRET = os.getenv("NOBITEX_API_SECRET", "YOUR_API_SECRET_HERE")
NOBITEX_USERNAME = os.getenv("NOBITEX_USERNAME", "YOUR_USERNAME_HERE")
NOBITEX_PASSWORD = os.getenv("NOBITEX_PASSWORD", "YOUR_PASSWORD_HERE")

# ============================================================================
# TRADING & RISK MANAGEMENT PARAMETERS
# ============================================================================

@dataclass
class RiskConfig:
    """Risk management configuration"""
    MAX_CONCURRENT_POSITIONS: int = 6  # Maximum simultaneous open positions
    MAX_POSITION_SIZE_PERCENT: float = 5.0  # Max % of account per trade
    MIN_POSITION_SIZE_USDT: float = 50.0  # Minimum position size
    MAX_POSITION_SIZE_USDT: float = 5000.0  # Maximum position size
    
    # Leverage settings
    LEVERAGE: int = 2  # Conservative 2x leverage (max 5x on Nobitex)
    
    # Stop Loss & Take Profit
    ATR_MULTIPLIER_SL: float = 2.0  # SL = ATR * 2.0
    ATR_MULTIPLIER_TP: float = 3.0  # TP = ATR * 3.0
    ATR_PERIOD: int = 14  # Standard ATR period
    
    # Trailing Stop
    TRAILING_STOP_PERCENT: float = 1.5  # Dynamic trailing stop (% of ATR)
    
    # Multi-target exit
    TP_LEVELS: List[float] = None  # [0.5, 0.3, 0.2] = Exit 50%, 30%, 20% at targets
    
    # Fees
    MAKER_FEE_PERCENT: float = 0.1  # Nobitex maker fee %
    TAKER_FEE_PERCENT: float = 0.15  # Nobitex taker fee %
    MARGIN_EXTENSION_FEE_PERCENT: float = 0.025  # Daily margin extension fee
    
    # Safety
    MIN_VOLUME_24H_USDT: float = 100000.0  # Minimum 24h volume to trade
    MAX_SPREAD_BPS: float = 50.0  # Maximum bid-ask spread (basis points)
    MIN_LIQUIDITY_DEPTH: float = 10000.0  # Min liquidity in order book

    def __post_init__(self):
        if self.TP_LEVELS is None:
            self.TP_LEVELS = [0.5, 0.3, 0.2]  # Default multi-level exit

RISK_CONFIG = RiskConfig()

# ============================================================================
# MARKET SCREENER CONFIGURATION
# ============================================================================

@dataclass
class ScreenerConfig:
    """Dynamic market screener settings"""
    SCAN_INTERVAL_SECONDS: int = 60  # Rescan market every 60s
    MIN_COINS_TO_TRACK: int = 5  # Minimum coins in watchlist
    MAX_COINS_TO_TRACK: int = 20  # Maximum coins to monitor
    VOLATILITY_THRESHOLD_LOW: float = 0.5  # Min volatility (ATR %)
    VOLATILITY_THRESHOLD_HIGH: float = 5.0  # Max volatility (ATR %)
    VOLUME_RANKING_WEIGHT: float = 0.4  # Weight for volume in scoring
    VOLATILITY_RANKING_WEIGHT: float = 0.3  # Weight for volatility
    LIQUIDITY_RANKING_WEIGHT: float = 0.3  # Weight for order book depth
    BLACKLIST_DAYS: int = 1  # Days to blacklist poor performers
    QUOTE_CURRENCY: str = "USDT"  # Only USDT pairs for now

SCREENER_CONFIG = ScreenerConfig()

# ============================================================================
# TECHNICAL ANALYSIS & STRATEGY
# ============================================================================

@dataclass
class StrategyConfig:
    """Technical analysis and strategy parameters"""
    # Timeframe
    CANDLE_INTERVAL_MINUTES: int = 5  # 5-minute candles
    LOOKBACK_CANDLES: int = 100  # Fetch last 100 candles
    
    # EMA Ribbon
    EMA_FAST_PERIOD: int = 9
    EMA_MID_PERIOD: int = 21
    EMA_SLOW_PERIOD: int = 55
    
    # RSI Filter
    RSI_PERIOD: int = 14
    RSI_OVERBOUGHT: float = 70.0
    RSI_OVERSOLD: float = 30.0
    
    # Volume & Order Flow
    VOLUME_MA_PERIOD: int = 20
    VOLUME_BREAKOUT_THRESHOLD: float = 1.5  # 1.5x average volume
    
    # Entry conditions
    MIN_RSI_LONG: float = 30.0  # Don't buy when RSI < 30 (too weak signal)
    MAX_RSI_SHORT: float = 70.0  # Don't short when RSI > 70
    
    # Adaptive signals
    SIGNAL_CONFIDENCE_THRESHOLD: float = 0.65  # Minimum signal confidence (0.0-1.0)

STRATEGY_CONFIG = StrategyConfig()

# ============================================================================
# ADAPTIVE LEARNING MODULE
# ============================================================================

@dataclass
class LearnerConfig:
    """Online learning and optimization settings"""
    DB_PATH: str = str(Path(__file__).parent / "trading_history.db")
    UPDATE_INTERVAL_HOURS: int = 24  # Daily weight update
    MIN_TRADES_TO_LEARN: int = 10  # Minimum trades before optimization
    LEARNING_RATE: float = 0.1  # Bayesian optimization learning rate
    SIGNAL_WEIGHT_DECAY: float = 0.95  # Exponential decay of old signals
    ENABLE_ADAPTIVE_MODE: bool = True  # Enable real-time weight adjustment

LEARNER_CONFIG = LearnerConfig()

# ============================================================================
# EMAIL & NOTIFICATION SETTINGS
# ============================================================================

@dataclass
class NotifierConfig:
    """Email and daily reporting configuration"""
    SMTP_SERVER: str = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USERNAME: str = os.getenv("SMTP_USERNAME", "your-email@gmail.com")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "your-app-password")
    
    REPORT_RECIPIENT: str = "alirezafazeli@live.com"
    REPORT_TIME_HOUR: int = 23  # 23:00 (11 PM)
    REPORT_TIME_MINUTE: int = 0
    
    ENABLE_EMAIL_REPORTS: bool = True
    ENABLE_TRADE_ALERTS: bool = True  # Alert on each trade entry/exit

NOTIFIER_CONFIG = NotifierConfig()

# ============================================================================
# SYSTEM & LOGGING
# ============================================================================

@dataclass
class SystemConfig:
    """System and logging settings"""
    LOG_DIR: str = str(Path(__file__).parent / "logs")
    LOG_LEVEL: str = "INFO"  # DEBUG, INFO, WARNING, ERROR
    
    # Network & API
    API_TIMEOUT_SECONDS: int = 10
    API_MAX_RETRIES: int = 3
    BACKOFF_MULTIPLIER: float = 2.0
    BACKOFF_MAX_WAIT: int = 60  # Max 60 seconds between retries
    
    # Heartbeat & Watchdog
    HEARTBEAT_INTERVAL_SECONDS: int = 30  # Check connection health
    SAFE_MODE_IDLE_TIMEOUT: int = 300  # 5 minutes before auto-exit in safe mode
    
    # Performance
    ENABLE_PROFILING: bool = False
    MAX_LOG_FILE_SIZE_MB: int = 50
    LOG_RETENTION_DAYS: int = 30

SYSTEM_CONFIG = SystemConfig()

# ============================================================================
# TRADING PAIRS WHITELIST
# ============================================================================
# Only trade these pairs (add or remove as needed)
WHITELISTED_PAIRS = [
    "BTC/USDT",
    "ETH/USDT",
    "BNB/USDT",
    "XRP/USDT",
    "ADA/USDT",
    "DOGE/USDT",
    "SOL/USDT",
    "MATIC/USDT",
]

# ============================================================================
# BLACKLISTED PAIRS
# ============================================================================
# Never trade these pairs
BLACKLISTED_PAIRS = [
    "SHIB/USDT",  # Low liquidity, high spread
]

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def ensure_config_dirs():
    """Create necessary directories if they don't exist"""
    Path(SYSTEM_CONFIG.LOG_DIR).mkdir(parents=True, exist_ok=True)
    Path(LEARNER_CONFIG.DB_PATH).parent.mkdir(parents=True, exist_ok=True)

def validate_config() -> bool:
    """Validate critical configuration settings"""
    errors = []
    
    if NOBITEX_API_KEY == "YOUR_API_KEY_HERE":
        errors.append("NOBITEX_API_KEY not configured")
    if NOBITEX_API_SECRET == "YOUR_API_SECRET_HERE":
        errors.append("NOBITEX_API_SECRET not configured")
    if RISK_CONFIG.MAX_CONCURRENT_POSITIONS < 1:
        errors.append("MAX_CONCURRENT_POSITIONS must be >= 1")
    if RISK_CONFIG.LEVERAGE < 1 or RISK_CONFIG.LEVERAGE > 5:
        errors.append("LEVERAGE must be between 1 and 5")
    
    if errors:
        print("⚠️  Configuration Errors:")
        for error in errors:
            print(f"  - {error}")
        return False
    
    return True

# Initialize on import
ensure_config_dirs()
