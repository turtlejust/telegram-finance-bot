from telethon import TelegramClient, events, Button
import json

# === CONFIGURAZIONE ===
import os

api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('TELEGRAM_BOT_TOKEN')


bot = TelegramClient('jusaboy_session', api_id, api_hash).start(bot_token=bot_token)

# === /START ===
@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    if event.is_private:
        await event.respond(
            "👋 *Benvenuto nel tuo Assistente Finanziario!*\n\n"
            "Scegli cosa vuoi fare:",
            buttons=[
                [Button.text("📊 Radar Watchlist"), Button.text("➕ Aggiungi Ticker")],
                [Button.text("⚙️ Menu completo"), Button.text("❌ Esci")]
            ]
        )

# === /MENU ===
@bot.on(events.NewMessage(pattern='/menu'))
async def menu(event):
    await event.respond(
        "📋 *Comandi disponibili:*\n"
        "/radar — panoramica titoli\n"
        "/notizie TICKER — ultime news\n"
        "/rsi TICKER — RSI attuale\n"
        "/vwap TICKER — VWAP vs prezzo\n"
        "/bilancio TICKER — check-up azienda\n"
        "/etf TICKER — ETF legati al titolo\n"
        "/previsione TICKER — forecast esterni\n"
        "/idee — contenuti da value source"
    )

# === /RADAR ===
@bot.on(events.NewMessage(pattern='/radar'))
async def radar(event):
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

print("🤖 Bot avviato!")
bot.run_until_disconnected()
