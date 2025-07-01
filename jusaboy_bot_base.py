import os
from telethon import TelegramClient, events, Button

# Importa funzioni dai moduli separati
from jusaboy_bot_radar import handle_radar
from jusaboy_bot_google_sheets import handle_google_sheets_command
from jusaboy_bot_finale import handle_finale_commands

# Configurazione variabili ambiente
api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('TELEGRAM_BOT_TOKEN')

bot = TelegramClient('jusaboy_session', api_id, api_hash).start(bot_token=bot_token)

# Comando /start
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

# Comando /radar
@bot.on(events.NewMessage(pattern='/radar'))
async def radar(event):
    await handle_radar(event)

# Comando /google_sheets (esempio)
@bot.on(events.NewMessage(pattern='/google_sheets'))
async def google_sheets(event):
    await handle_google_sheets_command(event)

# Comandi extra gestiti in finale.py (/menu, /notizie, /rsi, ecc)
@bot.on(events.NewMessage(pattern='/menu'))
@bot.on(events.NewMessage(pattern='/notizie'))
@bot.on(events.NewMessage(pattern='/rsi'))
@bot.on(events.NewMessage(pattern='/vwap'))
@bot.on(events.NewMessage(pattern='/bilancio'))
@bot.on(events.NewMessage(pattern='/etf'))
@bot.on(events.NewMessage(pattern='/previsione'))
@bot.on(events.NewMessage(pattern='/idee'))
async def finale(event):
    await handle_finale_commands(event)

print("🤖 Bot avviato!")
bot.run_until_disconnected()
