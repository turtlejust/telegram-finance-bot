import json

async def handle_radar(event):
    try:
        with open("watchlist.json", "r") as f:
            data = json.load(f)
        tickers = data.get("tickers", [])
        if tickers:
            lista = "\n".join(f"• {t.upper()}" for t in tickers)
            await event.respond(f"📡 *Radar Watchlist*\n\n{lista}", parse_mode="markdown")
        else:
            await event.respond("⚠️ La watchlist è vuota.")
    except Exception as e:
        await event.respond(f"❗ Errore nel comando /radar: {e}")
