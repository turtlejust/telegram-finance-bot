import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import json

# Configurazione Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_json_str = os.getenv('GOOGLE_CREDS_JSON')

# Carica credenziali da variabile ambiente come stringa JSON
creds_dict = json.loads(creds_json_str)
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

sheet_name = "WatchlistBot"
try:
    sheet = client.open(sheet_name).sheet1
except gspread.SpreadsheetNotFound:
    sheet = client.create(sheet_name).sheet1
    sheet.append_row(["Ticker"])

async def handle_google_sheets_command(event):
    await event.respond("Funzione Google Sheets in arrivo!")
    # Qui potrai implementare lettura/scrittura da Google Sheets quando vuoi
