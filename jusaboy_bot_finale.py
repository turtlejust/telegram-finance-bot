from telethon import events

async def handle_finale_commands(event):
    try:
        # Qui puoi aggiungere tutti i comandi finali del bot
        # Esempio: /notizie, /rsi, /vwap, /bilancio, /etf, /previsione, /idee

        text = event.raw_text.lower()

        if text.startswith("/notizie"):
            ticker = text.split(" ", 1)[1].upper() if " " in text else None
            if ticker:
                await event.respond(f"📰 Ultime notizie per {ticker} (placeholder).")
            else:
                await event.respond("❗ Usa: /notizie TICKER")
        elif text.startswith("/rsi"):
            ticker = text.split(" ", 1)[1].upper() if " " in text else None
            if ticker:
                await event.respond(f"📈 RSI attuale per {ticker} (placeholder).")
            else:
                await event.respond("❗ Usa: /rsi TICKER")
        elif text.startswith("/vwap"):
            ticker = text.split(" ", 1)[1].upper() if " " in text else None
            if ticker:
                await event.respond(f"📊 VWAP vs prezzo per {ticker} (placeholder).")
            else:
                await event.respond("❗ Usa: /vwap TICKER")
        elif text.startswith("/bilancio"):
            ticker = text.split(" ", 1)[1].upper() if " " in text else None
            if ticker:
                await event.respond(f"🏦 Bilancio aziendale per {ticker} (placeholder).")
            else:
                await event.respond("❗ Usa: /bilancio TICKER")
        elif text.startswith("/etf"):
            ticker = text.split(" ", 1)[1].upper() if " " in text else None
            if ticker:
                await event.respond(f"💼 ETF legati a {ticker} (placeholder).")
            else:
                await event.respond("❗ Usa: /etf TICKER")
        elif text.startswith("/previsione"):
            ticker = text.split(" ", 1)[1].upper() if " " in text else None
            if ticker:
                await event.respond(f"🔮 Previsioni esterne per {ticker} (placeholder).")
            else:
                await event.respond("❗ Usa: /previsione TICKER")
        elif text == "/idee":
            await event.respond("💡 Contenuti da value source (placeholder).")
        else:
            await event.respond("❓ Comando non riconosciuto.")
    except Exception as e:
        await event.respond(f"❗ Errore nel comando: {e}")
