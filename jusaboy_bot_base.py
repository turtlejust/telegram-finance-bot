import os
import json
import asyncio
from telethon import TelegramClient, events, Button
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from jusaboy_bot_radar import handle_radar
from jusaboy_bot_google_sheets import handle_google_sheets_command
from jusaboy_bot_finale import handle_finale_commands

# --- CONFIG ---
api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('TELEGRAM_BOT_TOKEN')

# Avvia il client Telegram
bot = TelegramClient('jusaboy_session', api_id, api_hash).start(bot_token=bot_token)

# --- SCHEDULER ---
scheduler = AsyncIOScheduler(timezone="Europe/Rome")

async def morning_report():
    """
    Esempio di report mattutino:
    - Legge la watchlist da watchlist.json (o Google Sheets)
    - Costruisce un messaggio con placeholder per RSI/VWAP/etc.
    - Invia il report a tutti gli utenti iscritti
    """
    # 1. Carica tickers da locale
    tickers = []
    try:
        with open("watchlist.json") as f:
            tickers = json.load(f).get("tickers", [])
    except FileNotFoundError:
        pass
    # 2. Costruisci linee di report
    lines = [f"• {t.upper()}: RSI=--, VWAP=--" for t in tickers]
    report = "☀️ *Report Mattutino*

" + "\n".join(lines)

    # 3. Lista di utenti (da gestire tu/catalogare)
    subscribed_users = []  # TODO: carica qui i chat_id degli utenti iscritti

    # 4. Invia a ciascun utente
    for chat_id in subscribed_users:
        await bot.send_message(chat_id, report, parse_mode="markdown")

# Pianifica il report ogni giorni alle 08:00
scheduler.add_job(morning_report, 'cron', hour=8, minute=0)
scheduler.start()

# --- MENU INLINE ---
@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    if event.is_private:
        buttons = [
            [Button.inline("📊 Radar", b"radar")],
            [Button.inline("➕ Aggiungi Ticker", b"aggiungi")],
            [Button.inline("📝 Watchlist Sheets", b"google_sheets")],
            [Button.inline("⚙️ Comandi", b"menu")],
            [Button.inline("❌ Esci", b"esci")],
        ]
        await event.respond(
            "👋 *Benvenuto nel tuo Assistente Finanziario!*\n\nScegli cosa fare:",
            buttons=buttons,
            parse_mode="markdown"
        )

@bot.on(events.CallbackQuery)
async def callback_handler(event):
    data = event.data.decode()

    if data == "radar":
        await handle_radar(event)
    elif data == "aggiungi":
        await event.respond("✏️ Scrivi il ticker da aggiungere:")
    elif data == "google_sheets":
        await handle_google_sheets_command(event)
    elif data == "menu":
        # Richiama la lista comandi dal modulo esistente
        await event.respond(
            "📋 *Comandi disponibili:*\n"
            "/radar — panoramica titoli\n"
            "/notizie TICKER — ultime news\n"
            "/rsi TICKER — RSI attuale\n"
            "/vwap TICKER — VWAP vs prezzo\n"
            "/bilancio TICKER — check-up azienda\n"
            "/etf TICKER — ETF legati al titolo\n"
            "/previsione TICKER — forecast esterni\n"
            "/idee — contenuti da value source",
            buttons=[[Button.inline("◀️ Indietro", b"start")]],
            parse_mode="markdown"
        )
    elif data == "esci":
        await event.respond("👋 A presto!")
    elif data == "start":
        await start(event)
    else:
        # Fallback a comandi testuali per handle_finale
        await handle_finale_commands(event)

# Fallback per tutti gli altri messaggi
@bot.on(events.NewMessage)
async def fallback_handler(event):
    # Gestisci qui l'inserimento manuale di ticker dopo "aggiungi"
    # oppure passa ai comandi finali
    await handle_finale_commands(event)

print("🤖 Bot avviato con menu inline e scheduler APScheduler!")
bot.run_until_disconnected()
