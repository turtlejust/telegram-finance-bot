import os
from telethon import TelegramClient, events, Button

from jusaboy_bot_radar import handle_radar
from jusaboy_bot_google_sheets import handle_google_sheets_command
from jusaboy_bot_finale import handle_finale_commands

api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('TELEGRAM_BOT_TOKEN')

bot = TelegramClient('jusaboy_session', api_id, api_hash).start(bot_token=bot_token)

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
        "/idee — contenuti da value source\n"
    )

@bot.on(events.NewMessage(pattern='/radar'))
async def radar(event):
    await handle_radar(event)

@bot.on(events.NewMessage(pattern='/google_sheets'))
async def google_sheets(event):
    await handle_google_sheets_command(event)

@bot.on(events.NewMessage(pattern='/finale'))
async def finale(event):
    await handle_finale_commands(event)

print("🤖 Bot avviato!")
bot.run_until_disconnected()
