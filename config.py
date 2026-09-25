"""
Configuration Management Module
Central settings for Nobitex Trading Bot
"""

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import List

from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env")

# ============================================================================
# API & AUTHENTICATION SETTINGS
# ============================================================================
NOBITEX_API_BASE_URL = os.getenv("NOBITEX_API_BASE_URL", os.getenv("BASE_URL", "https://apiv2.nobitex.ir")).rstrip("/")
NOBITEX_API_KEY = os.getenv("NOBITEX_API_KEY", "YOUR_API_KEY_HERE")
NOBITEX_API_SECRET = os.getenv("NOBITEX_API_SECRET", os.getenv("NOBITEX_SECRET_KEY", "YOUR_API_SECRET_HERE"))
NOBITEX_USERNAME = os.getenv("NOBITEX_USERNAME", "YOUR_USERNAME_HERE")
NOBITEX_PASSWORD = os.getenv("NOBITEX_PASSWORD", "YOUR_PASSWORD_HERE")

# Execution mode (paper trading / live / dry run)
EXECUTION_MODE = os.getenv("EXECUTION_MODE", "PAPER_TRADING").upper()
PAPER_TRADING = os.getenv("PAPER_TRADING", "true").strip().lower() == "true"
DRY_RUN = os.getenv("DRY_RUN", "true").strip().lower() == "true"
LIVE_TRADING = os.getenv("LIVE_TRADING", "false").strip().lower() == "true"
MARGIN_ENABLED = os.getenv("MARGIN_ENABLED", "false").strip().lower() == "true"

# Multi-symbol runtime config
TRADING_SYMBOLS = [
    s.strip().upper().replace("/", "")
    for s in os.getenv("TRADING_SYMBOLS", "BTCUSDT,ETHUSDT").split(",")
    if s and s.strip()
]
SCAN_INTERVAL_SECONDS = int(os.getenv("SCAN_INTERVAL_SECONDS", "60"))
DASHBOARD_PORT = int(os.getenv("DASHBOARD_PORT", "8000"))

# ============================================================================
# TRADING & RISK MANAGEMENT PARAMETERS
# ============================================================================

@dataclass
class RiskConfig:
    """Risk management configuration"""
    MAX_CONCURRENT_POSITIONS: int = 6
    MAX_POSITION_SIZE_PERCENT: float = 5.0
    MIN_POSITION_SIZE_USDT: float = 50.0
    MAX_POSITION_SIZE_USDT: float = 5000.0
    LEVERAGE: int = 2
    ATR_MULTIPLIER_SL: float = 2.0
    ATR_MULTIPLIER_TP: float = 3.0
    ATR_PERIOD: int = 14
    TRAILING_STOP_PERCENT: float = 1.5
    TP_LEVELS: List[float] = field(default_factory=lambda: [0.5, 0.3, 0.2])
    MAKER_FEE_PERCENT: float = 0.1
    TAKER_FEE_PERCENT: float = 0.15
    MARGIN_EXTENSION_FEE_PERCENT: float = 0.025
    MIN_VOLUME_24H_USDT: float = 100000.0
    MAX_SPREAD_BPS: float = 50.0
    MIN_LIQUIDITY_DEPTH: float = 10000.0

RISK_CONFIG = RiskConfig()

# ============================================================================
# MARKET SCREENER CONFIGURATION
# ============================================================================

@dataclass
class ScreenerConfig:
    """Dynamic market screener settings"""
    SCAN_INTERVAL_SECONDS: int = SCAN_INTERVAL_SECONDS
    MIN_COINS_TO_TRACK: int = 5
    MAX_COINS_TO_TRACK: int = 20
    VOLATILITY_THRESHOLD_LOW: float = 0.5
    VOLATILITY_THRESHOLD_HIGH: float = 5.0
    VOLUME_RANKING_WEIGHT: float = 0.4
    VOLATILITY_RANKING_WEIGHT: float = 0.3
    LIQUIDITY_RANKING_WEIGHT: float = 0.3
    BLACKLIST_DAYS: int = 1
    QUOTE_CURRENCY: str = "USDT"

SCREENER_CONFIG = ScreenerConfig()

# ============================================================================
# TECHNICAL ANALYSIS & STRATEGY
# ============================================================================

@dataclass
class StrategyConfig:
    """Technical analysis and strategy parameters"""
    CANDLE_INTERVAL_MINUTES: int = 5
    LOOKBACK_CANDLES: int = 100
    EMA_FAST_PERIOD: int = 9
    EMA_MID_PERIOD: int = 21
    EMA_SLOW_PERIOD: int = 55
    RSI_PERIOD: int = 14
    RSI_OVERBOUGHT: float = 70.0
    RSI_OVERSOLD: float = 30.0
    VOLUME_MA_PERIOD: int = 20
    VOLUME_BREAKOUT_THRESHOLD: float = 1.5
    MIN_RSI_LONG: float = 30.0
    MAX_RSI_SHORT: float = 70.0
    SIGNAL_CONFIDENCE_THRESHOLD: float = 0.65

STRATEGY_CONFIG = StrategyConfig()

# ============================================================================
# ADAPTIVE LEARNING MODULE
# ============================================================================

@dataclass
class LearnerConfig:
    """Online learning and optimization settings"""
    DB_PATH: str = str(Path(__file__).parent / "trading_history.db")
    UPDATE_INTERVAL_HOURS: int = 24
    MIN_TRADES_TO_LEARN: int = 10
    LEARNING_RATE: float = 0.1
    SIGNAL_WEIGHT_DECAY: float = 0.95
    ENABLE_ADAPTIVE_MODE: bool = True

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
    REPORT_RECIPIENT: str = os.getenv("REPORT_RECIPIENT", "alirezafazeli@live.com")
    REPORT_TIME_HOUR: int = int(os.getenv("REPORT_TIME_HOUR", "23"))
    REPORT_TIME_MINUTE: int = int(os.getenv("REPORT_TIME_MINUTE", "0"))
    ENABLE_EMAIL_REPORTS: bool = os.getenv("ENABLE_EMAIL_REPORTS", "true").strip().lower() == "true"
    ENABLE_TRADE_ALERTS: bool = os.getenv("ENABLE_TRADE_ALERTS", "true").strip().lower() == "true"

NOTIFIER_CONFIG = NotifierConfig()

# ============================================================================
# SYSTEM & LOGGING
# ============================================================================

@dataclass
class SystemConfig:
    """System and logging settings"""
    LOG_DIR: str = str(Path(__file__).parent / "logs")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    API_TIMEOUT_SECONDS: int = int(os.getenv("API_TIMEOUT_SECONDS", "10"))
    API_MAX_RETRIES: int = int(os.getenv("API_MAX_RETRIES", "3"))
    BACKOFF_MULTIPLIER: float = float(os.getenv("BACKOFF_MULTIPLIER", "2.0"))
    BACKOFF_MAX_WAIT: int = int(os.getenv("BACKOFF_MAX_WAIT", "60"))
    HEARTBEAT_INTERVAL_SECONDS: int = int(os.getenv("HEARTBEAT_INTERVAL_SECONDS", "30"))
    SAFE_MODE_IDLE_TIMEOUT: int = int(os.getenv("SAFE_MODE_IDLE_TIMEOUT", "300"))
    ENABLE_PROFILING: bool = os.getenv("ENABLE_PROFILING", "false").strip().lower() == "true"
    MAX_LOG_FILE_SIZE_MB: int = int(os.getenv("MAX_LOG_FILE_SIZE_MB", "50"))
    LOG_RETENTION_DAYS: int = int(os.getenv("LOG_RETENTION_DAYS", "30"))

SYSTEM_CONFIG = SystemConfig()

# ============================================================================
# TRADING PAIRS WHITELIST
# ============================================================================
WHITELISTED_PAIRS = [
    f"{symbol[:3]}/{symbol[3:]}" if symbol.endswith("USDT") and len(symbol) > 4 else symbol
    for symbol in TRADING_SYMBOLS
]

# Never trade these pairs
BLACKLISTED_PAIRS = [
    "SHIB/USDT",
]

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def ensure_config_dirs():
    Path(SYSTEM_CONFIG.LOG_DIR).mkdir(parents=True, exist_ok=True)
    Path(LEARNER_CONFIG.DB_PATH).parent.mkdir(parents=True, exist_ok=True)


def validate_config() -> bool:
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

ensure_config_dirs()
