import json

async def handle_radar(event):
    try:
        with open("watchlist.json", "r") as f:
            data = json.load(f)
        tickers = data.get("jmila", [])
        if tickers:
            tickers_list = "\n".join(f"• {t.upper()}" for t in tickers)
            await event.respond(f"📡 *La tua Watchlist attuale:*\n\n{tickers_list}")
        else:
            await event.respond("⚠️ Nessun ticker trovato nella tua watchlist.")
    except Exception as e:
        await event.respond(f"Errore nel leggere la watchlist: {e}")
