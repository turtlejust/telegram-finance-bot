# File: jusaboy_bot_finale.py

from telethon import events
import traceback
from jusaboy_bot_data import (
    calcola_rsi, calcola_vwap,
    get_news, get_macro_data, check_etf_changes,
    get_crypto_data, get_ideas, get_score,
    fetch_rss, get_earnings
)

async def handle_finale_commands(event):
    try:
        text = event.raw_text.lower().strip()

        # ——————————————————————————————
        # NUOVI COMANDI
        # ——————————————————————————————

        # /signal: RSI e VWAP
        if text.startswith("/signal"):
            parts = text.split()
            if len(parts) == 2:
                ticker = parts[1].upper()
                rsi = calcola_rsi(ticker)
                vwap = calcola_vwap(ticker)
                await event.respond(
                    f"📊 *Signal {ticker}*\n"
                    f"• RSI: {rsi:.2f}\n"
                    f"• VWAP: {vwap:.2f}",
                    parse_mode="markdown"
                )
            else:
                await event.respond("❗ Usa: /signal TICKER")

        # /news TICKER  (RSS da Yahoo)
        elif text.startswith("/news"):
            parts = text.split()
            if len(parts) == 2:
                ticker = parts[1].upper()
                articles = get_news(ticker)
                msg = "\n".join(f"• [{a['title']}]({a['link']})" for a in articles)
                await event.respond(f"📰 *Notizie {ticker}*\n{msg}", parse_mode="markdown")
            else:
                await event.respond("❗ Usa: /news TICKER")

        # /macro
        elif text == "/macro":
            data = get_macro_data()
            msg = "\n".join(f"• {k}: {v}" for k, v in data.items())
            await event.respond(f"📈 *Dati Macro*\n{msg}", parse_mode="markdown")

        # /etf-changes ETF
        elif text.startswith("/etf-changes"):
            parts = text.split()
            if len(parts) == 2:
                etf = parts[1].upper()
                changes = check_etf_changes(etf)
                await event.respond(
                    f"💼 *ETF {etf} changes*\n"
                    f"Added: {changes['added']}\n"
                    f"Removed: {changes['removed']}",
                    parse_mode="markdown"
                )
            else:
                await event.respond("❗ Usa: /etf-changes ETF")

        # /crypto SYMBOL
        elif text.startswith("/crypto"):
            parts = text.split()
            if len(parts) == 2:
                sym = parts[1].upper()
                info = get_crypto_data(sym)
                await event.respond(
                    f"🚀 *Crypto {sym}*\n"
                    f"Price: {info['price']}\n"
                    f"24h: {info['change_24h']}"
                )
            else:
                await event.respond("❗ Usa: /crypto SYMBOL")

        # /ideas
        elif text == "/ideas":
            ideas = get_ideas()
            msg = "\n".join(f"• {i}" for i in ideas)
            await event.respond(f"💡 *Idee*\n{msg}", parse_mode="markdown")

        # /score TICKER
        elif text.startswith("/score"):
            parts = text.split()
            if len(parts) == 2:
                tck = parts[1].upper()
                sc = get_score(tck)
                await event.respond(f"🏆 *Score {tck}*: {sc:.1f}")
            else:
                await event.respond("❗ Usa: /score TICKER")

        # /rss URL
        elif text.startswith("/rss"):
            parts = text.split(maxsplit=1)
            if len(parts) == 2:
                url = parts[1]
                entries = fetch_rss(url)
                msg = "\n".join(f"• [{e['title']}]({e['link']})" for e in entries)
                await event.respond(f"🔗 *Feed RSS*\n{msg}", parse_mode="markdown")
            else:
                await event.respond("❗ Usa: /rss RSS_FEED_URL")

        # /earnings TICKER
        elif text.startswith("/earnings"):
            parts = text.split()
            if len(parts) == 2:
                tk = parts[1].upper()
                ev = get_earnings(tk)
                msg = "\n".join(f"• {k}: {v}" for k, v in ev.items())
                await event.respond(f"🗓️ *Earnings {tk}*\n{msg}", parse_mode="markdown")
            else:
                await event.respond("❗ Usa: /earnings TICKER")

        # ——————————————————————————————
        # COMMANDI STORICI (placeholder)
        # ——————————————————————————————

        elif text.startswith("/notizie"):
            ticker = text.split(" ",1)[1].upper() if " " in text else None
            if ticker:
                await event.respond(f"📰 Ultime notizie per {ticker} (placeholder).")
            else:
                await event.respond("❗ Usa: /notizie TICKER")

        elif text.startswith("/rsi"):
            ticker = text.split(" ",1)[1].upper() if " " in text else None
            if ticker:
                await event.respond(f"📈 RSI attuale per {ticker} (placeholder).")
            else:
                await event.respond("❗ Usa: /rsi TICKER")

        elif text.startswith("/vwap"):
            ticker = text.split(" ",1)[1].upper() if " " in text else None
            if ticker:
                await event.respond(f"📊 VWAP vs prezzo per {ticker} (placeholder).")
            else:
                await event.respond("❗ Usa: /vwap TICKER")

        elif text.startswith("/bilancio"):
            ticker = text.split(" ",1)[1].upper() if " " in text else None
            if ticker:
                await event.respond(f"🏦 Bilancio aziendale per {ticker} (placeholder).")
            else:
                await event.respond("❗ Usa: /bilancio TICKER")

        elif text.startswith("/etf "):
            ticker = text.split(" ",1)[1].upper() if " " in text else None
            if ticker:
                await event.respond(f"💼 ETF legati a {ticker} (placeholder).")
            else:
                await event.respond("❗ Usa: /etf TICKER")

        elif text.startswith("/previsione"):
            ticker = text.split(" ",1)[1].upper() if " " in text else None
            if ticker:
                await event.respond(f"🔮 Previsioni esterne per {ticker} (placeholder).")
            else:
                await event.respond("❗ Usa: /previsione TICKER")

        elif text == "/idee":
            await event.respond("💡 Contenuti da value source (placeholder).")

        else:
            await event.respond("❓ Comando non riconosciuto.")

    except Exception as e:
        await event.respond(f"❗ Errore: {e}\n{traceback.format_exc()}")
