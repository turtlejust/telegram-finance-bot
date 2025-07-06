import os
import requests
import feedparser
import yfinance as yf
import pandas as pd

# 1️⃣ RSI e VWAP
def calcola_rsi(ticker: str, period: int = 14) -> float:
    data = yf.Ticker(ticker).history(period="6mo")["Close"]
    if len(data) < period + 1:
        raise ValueError(f"Dati insufficienti per RSI su {ticker}")
    delta = data.diff().dropna()
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return float(rsi.iloc[-1])

def calcola_vwap(ticker: str, period_days: int = 1) -> float:
    intraday = yf.Ticker(ticker).history(period=f"{period_days}d", interval="5m")
    if not intraday.empty and "Volume" in intraday.columns:
        return float((intraday["Close"] * intraday["Volume"]).sum() / intraday["Volume"].sum())
    daily = yf.Ticker(ticker).history(period=f"{period_days}d", interval="1d")
    return float(daily["Close"].iloc[-1])

# 2️⃣ News via RSS (Yahoo)
def get_news(ticker: str, limit: int = 5) -> list[dict]:
    url = f"https://finance.yahoo.com/rss/headline?s={ticker}"
    feed = feedparser.parse(url)
    return [{"title": e.title, "link": e.link} for e in feed.entries[:limit]]

# 3️⃣ Macro data (stub)
def get_macro_data() -> dict:
    return {
        "CPI (MoM)": "0.4%",
        "Unemployment Rate": "5.1%",
        "Fed Funds Rate": "5.25%"
    }

# 4️⃣ ETF changes (stub)
def check_etf_changes(etf: str, period_days: int = 1) -> dict:
    return {"added": ["ABC", "DEF"], "removed": ["XYZ"]}

# 5️⃣ Crypto sentiment (stub)
def get_crypto_data(symbol: str) -> dict:
    return {"price": 12345.67, "change_24h": "+2.3%"}

# 6️⃣ Ideas (stub)
def get_ideas(limit: int = 5) -> list[str]:
    return ["Idea1", "Idea2", "Idea3"]

# 7️⃣ Score (stub)
def get_score(ticker: str) -> float:
    return 75.4

# 8️⃣ Generic RSS
def fetch_rss(url: str, limit: int = 5) -> list[dict]:
    feed = feedparser.parse(url)
    return [{"title": e.title, "link": e.link} for e in feed.entries[:limit]]

# 9️⃣ Earnings via yfinance
def get_earnings(ticker: str) -> dict:
    cal = yf.Ticker(ticker).calendar
    return {k: v for k, v in cal.items()}
