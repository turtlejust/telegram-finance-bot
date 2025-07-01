import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Carica la variabile d'ambiente con le credenziali JSON di Google Sheets
creds_json_str = os.getenv('GOOGLE_CREDS_JSON')
if not creds_json_str:
    raise RuntimeError("La variabile d'ambiente GOOGLE_CREDS_JSON non è impostata o è vuota!")

creds_dict = json.loads(creds_json_str)

# Configurazione Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

sheet_name = "WatchlistBot"  # Cambia con il nome del tuo Sheet
try:
    sheet = client.open(sheet_name).sheet1
except gspread.SpreadsheetNotFound:
    sheet = client.create(sheet_name).sheet1
    sheet.append_row(["Ticker"])

async def handle_google_sheets_command(event):
    try:
        tickers = sheet.col_values(1)[1:]  # Escludi header
        if tickers:
            lista = "\n".join(f"• {t}" for t in tickers)
            await event.respond(f"📄 *Watchlist da Google Sheets:*\n\n{lista}", parse_mode="markdown")
        else:
            await event.respond("⚠️ La watchlist su Google Sheets è vuota.")
    except Exception as e:
        await event.respond(f"❗ Errore nel comando Google Sheets: {e}")
