from telethon import TelegramClient, events, Button
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import os

# === CONFIGURAZIONE TELEGRAM ===
import os

api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('TELEGRAM_BOT_TOKEN')


bot = TelegramClient('jusaboy_session', api_id, api_hash).start(bot_token=bot_token)

# === CONFIGURAZIONE GOOGLE SHEETS ===
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
google_creds_path = os.getenv('GOOGLE_CREDS_PATH')
creds = ServiceAccountCredentials.from_json_keyfile_name(google_creds_path, scope)
client = gspread.authorize(creds)

sheet_name = "WatchlistBot"  # Cambia col nome del tuo Sheet
try:
    sheet = client.open(sheet_name).sheet1
except:
    sheet = client.create(sheet_name).sheet1
    sheet.append_row(["Ticker"])

# === CONFIGURAZIONE FILE LOCALE JSON ===
json_file = "watchlist.json"
if not os.path.exists(json_file):
    with open(json_file, "w") as f:
        json.dump({"tickers": []}, f)

def read_local_watchlist():
    with open(json_file, "r") as f:
        data = json.load(f)
    return data.get("tickers", [])

def save_local_watchlist(tickers):
    with open(json_file, "w") as f:
        json.dump({"tickers": tickers}, f, indent=2)

# Sincronizza locale -> sheet (all'avvio)
local_tickers = read_local_watchlist()
sheet.clear()
sheet.append_row(["Ticker"])
for t in local_tickers:
    sheet.append_row([t])

# === /start ===
@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    if event.is_private:
        await event.respond(
            "👋 *Benvenuto nel tuo Assistente Finanziario!* \nScegli un'opzione:",
            buttons=[
                [Button.text("📥 Aggiungi Ticker"), Button.text("🗑️ Rimuovi Ticker")],
                [Button.text("✏️ Modifica Ticker"), Button.text("📄 Mostra Watchlist")],
                [Button.text("❌ Esci")]
            ]
        )

# === /aggiungi TICKER ===
@bot.on(events.NewMessage(pattern='/aggiungi'))
async def aggiungi(event):
    try:
        ticker = event.raw_text.split(" ", 1)[1].strip().upper()
        tickers = read_local_watchlist()
        if ticker in tickers:
            await event.respond(f"⚠️ Il ticker *{ticker}* è già presente.", parse_mode="markdown")
            return
        tickers.append(ticker)
        save_local_watchlist(tickers)
        sheet.append_row([ticker])
        await event.respond(f"✅ Ticker *{ticker}* aggiunto alla watchlist!", parse_mode="markdown")
    except Exception as e:
        await event.respond(f"❗ Usa il comando così:\n/aggiungi TICKER\nErrore: {e}")

# === /rimuovi TICKER ===
@bot.on(events.NewMessage(pattern='/rimuovi'))
async def rimuovi(event):
    try:
        ticker = event.raw_text.split(" ", 1)[1].strip().upper()
        tickers = read_local_watchlist()
        if ticker not in tickers:
            await event.respond(f"⚠️ Il ticker *{ticker}* non è presente.", parse_mode="markdown")
            return
        tickers.remove(ticker)
        save_local_watchlist(tickers)

        # Rimuovi dallo sheet
        cell = sheet.find(ticker)
        if cell:
            sheet.delete_row(cell.row)

        await event.respond(f"✅ Ticker *{ticker}* rimosso dalla watchlist.", parse_mode="markdown")
    except Exception as e:
        await event.respond(f"❗ Usa il comando così:\n/rimuovi TICKER\nErrore: {e}")

# === /modifica VECCHIO_TICKER NUOVO_TICKER ===
@bot.on(events.NewMessage(pattern='/modifica'))
async def modifica(event):
    try:
        args = event.raw_text.split(" ", 2)
        if len(args) < 3:
            await event.respond("❗ Usa il comando così:\n/modifica VECCHIO_TICKER NUOVO_TICKER")
            return
        old_ticker = args[1].strip().upper()
        new_ticker = args[2].strip().upper()

        tickers = read_local_watchlist()
        if old_ticker not in tickers:
            await event.respond(f"⚠️ Il ticker *{old_ticker}* non è presente.", parse_mode="markdown")
            return
        if new_ticker in tickers:
            await event.respond(f"⚠️ Il ticker *{new_ticker}* è già presente.", parse_mode="markdown")
            return

        # Aggiorna locale
        idx = tickers.index(old_ticker)
        tickers[idx] = new_ticker
        save_local_watchlist(tickers)

        # Aggiorna sheet
        cell = sheet.find(old_ticker)
        if cell:
            sheet.update_cell(cell.row, cell.col, new_ticker)

        await event.respond(f"✅ Ticker *{old_ticker}* modificato in *{new_ticker}*.", parse_mode="markdown")

    except Exception as e:
        await event.respond(f"❗ Usa il comando così:\n/modifica VECCHIO_TICKER NUOVO_TICKER\nErrore: {e}")

# === /mostra (legge watchlist) ===
@bot.on(events.NewMessage(pattern='/mostra'))
async def mostra(event):
    try:
        tickers = read_local_watchlist()
        if tickers:
            lista = "\n".join(f"• {t}" for t in tickers)
            await event.respond(f"📄 *Watchlist attuale:*\n\n{lista}", parse_mode="markdown")
        else:
            await event.respond("⚠️ La watchlist è vuota.")
    except Exception as e:
        await event.respond(f"Errore: {e}")

print("🤖 Bot con Google Sheets e JSON avviato!")
bot.run_until_disconnected()
