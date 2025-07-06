import os
import time
import logging
import feedparser
import yfinance as yf
import pandas as pd
import finnhub
from dotenv import load_dotenv

# Carica variabili d'ambiente da .env
load_dotenv()

# --------------------------------------------------
# CONFIGURAZIONE CLIENT FINNHUB
# --------------------------------------------------
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")
if not FINNHUB_API_KEY:
    raise RuntimeError("FINNHUB_API_KEY non impostata!")
fh_client = finnhub.Client(api_key=FINNHUB_API_KEY)

# --------------------------------------------------
# HELPER: retry + log per yfinance.history
# --------------------------------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_history(ticker: str, period: str, interval: str = "1d",
                  max_retries: int = 3, sleep_seconds: float = 1.0) -> pd.DataFrame:
    for attempt in range(1, max_retries + 1):
        try:
            df = yf.Ticker(ticker).history(period=period, interval=interval)
            if df.empty:
                logger.warning(f"[fetch_history] {ticker} {period}/{interval} vuoto (tentativo {attempt})")
                time.sleep(sleep_seconds)
                continue
            return df
        except Exception as e:
            logger.error(f"[fetch_history] Errore {e} su {ticker} {period}/{interval} (tentativo {attempt})")
            time.sleep(sleep_seconds)
    return pd.DataFrame()

# --------------------------------------------------
# 1️⃣ RSI via Finnhub (fallback yfinance)
# --------------------------------------------------
def calcola_rsi(ticker: str, period: int = 14) -> float:
    """
    Prima tenta RSI via Finnhub; se fallisce, fallback su yfinance (6mo->1y->max).
    """
    # Finnhub RSI
    try:
        now = int(time.time())
        a_month_ago = now - 60*60*24*30
        resp = fh_client.indicator(symbol=ticker,
                                   resolution='D',
                                   _from=a_month_ago,
                                   to=now,
                                   indicator='rsi',
                                   timeperiod=period)
        if resp and resp.get('rsi'):
            return float(resp['rsi'][-1])
    except Exception as e:
        logger.warning(f"[RSI Finnhub] errore: {e}")
    # yfinance fallback
    for timeframe in ("6mo", "1y", "max"):
        df = fetch_history(ticker, timeframe, interval="1d")
        if len(df) >= period + 1:
            data = df['Close']
            delta = data.diff().dropna()
            gain = delta.where(delta > 0, 0.0)
            loss = -delta.where(delta < 0, 0.0)
            avg_gain = gain.rolling(window=period).mean()
            avg_loss = loss.rolling(window=period).mean()
            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))
            return float(rsi.iloc[-1])
    raise ValueError(f"RSI non calcolabile per {ticker}")

# --------------------------------------------------
# 2️⃣ VWAP via Finnhub (fallback yfinance)
# --------------------------------------------------
def calcola_vwap(ticker: str, period_days: int = 1) -> float:
    """
    Prima VWAP via Finnhub (VWMA); se fallisce, fallback su yfinance intraday o daily.
    """
    try:
        now = int(time.time())
        a_day_ago = now - period_days * 86400
        resp = fh_client.indicator(symbol=ticker,
                                   resolution='5',
                                   _from=a_day_ago,
                                   to=now,
                                   indicator='vwma')
        if resp and resp.get('vwma'):
            return float(resp['vwma'][-1])
    except Exception as e:
        logger.warning(f"[VWAP Finnhub] errore: {e}")
    # yfinance fallback
    df = fetch_history(ticker, f"{period_days}d", interval="5m")
    if not df.empty and 'Volume' in df.columns:
        return float((df['Close'] * df['Volume']).sum() / df['Volume'].sum())
    df = fetch_history(ticker, f"{period_days}d", interval="1d")
    if not df.empty:
        return float(df['Close'].iloc[-1])
    raise ValueError(f"VWAP non calcolabile per {ticker}")

# --------------------------------------------------
# 3️⃣ Notizie via Finnhub (fallback RSS Yahoo)
# --------------------------------------------------
def get_news(ticker: str, limit: int = 5) -> list[dict]:
    try:
        articles = fh_client.company_news(symbol=ticker,
                                          _from=(time.strftime('%Y-%m-%d', time.gmtime(time.time()-86400*7))),
                                          to=time.strftime('%Y-%m-%d', time.gmtime()))
        return [{'title': a['headline'], 'link': a['url']} for a in articles[:limit]]
    except Exception:
        url = f"https://finance.yahoo.com/rss/headline?s={ticker}"
        feed = feedparser.parse(url)
        return [{'title': e.title, 'link': e.link} for e in feed.entries[:limit]]

# --------------------------------------------------
# 4️⃣ Fondamentali & Earnings via Finnhub
# --------------------------------------------------
def get_macro_data() -> dict:
    data = fh_client.economic_calendar()
    res = {}
    for item in data:
        if item.get('symbol') in {'CPI YOY', 'UNRATE', 'FEDFUNDS'}:
            res[item['symbol']] = item.get('actual')
    return res

def get_earnings(ticker: str) -> dict:
    cal = fh_client.earnings_calendar(symbol=ticker)
    result = {}
    for e in cal:
        result[e.get('date')] = {
            'actual': e.get('actual'),
            'estimate': e.get('estimate')
        }
    return result

# --------------------------------------------------
# 5️⃣ Fondamentali aziendali (/bilancio)
# --------------------------------------------------
def get_stock_financials(ticker: str) -> dict:
    rpt = fh_client.financials_reported(symbol=ticker)
    return rpt.get('data', [{}])[0]

# --------------------------------------------------
# 6️⃣ ETF holdings
# --------------------------------------------------
def check_etf_changes(etf: str, period_days: int = 1) -> dict:
    holdings = fh_client.etf_holdings(symbol=etf)
    return {'holdings': holdings.get('holdings', [])}

# --------------------------------------------------
# 7️⃣ Crypto sentiment via Finnhub
# --------------------------------------------------
def get_crypto_data(symbol: str) -> dict:
    now = int(time.time())
    candles = fh_client.crypto_candles(symbol=symbol,
                                       resolution='D',
                                       _from=now-86400,
                                       to=now)
    if candles and candles.get('c'):
        price = candles['c'][-1]
        prev = candles['c'][-2] if len(candles['c'])>1 else price
        change = (price/prev - 1)*100
        return {'price': price, 'change_24h': f"{change:.2f}%"}
    return {'price': None, 'change_24h': None}

# --------------------------------------------------
# 8️⃣ Idea & Score & RSS placeholders
# --------------------------------------------------
def get_ideas(limit: int = 5) -> list[str]:
    return ['Idea1', 'Idea2']

def get_score(ticker: str) -> float:
    return 75.4

def fetch_rss(url: str, limit: int = 5) -> list[dict]:
    feed = feedparser.parse(url)
    return [{'title': e.title, 'link': e.link} for e in feed.entries[:limit]]
