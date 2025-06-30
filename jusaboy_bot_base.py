from telethon import TelegramClient, events, Button

# === CONFIGURAZIONE ===
api_id = 21024442
api_hash = 'dd1acab8b7c4ee4904023e214dcfee04'
bot_token = '7911673480:AAHD9Y_tu5qkzJNCAlHpNmud_wbmSRXzab4'

bot = TelegramClient('jusaboy_session', api_id, api_hash).start(bot_token=bot_token)

# === COMANDO /start ===
@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    if event.is_private:
        await event.respond(
            "👋 *Benvenuto nel tuo Assistente Finanziario!*\n\nScegli cosa vuoi fare:",
            buttons=[
                [Button.text("📊 Radar Watchlist"), Button.text("➕ Aggiungi Ticker")],
                [Button.text("⚙️ Menu completo"), Button.text("❌ Esci")]
            ]
        )

# === COMANDO /menu ===
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

print("🤖 Bot avviato!")
bot.run_until_disconnected()
