async def handle_finale_commands(event):
    text = event.raw_text.lower()
    
    if text.startswith('/menu'):
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
    
    elif text.startswith('/notizie'):
        # TODO: inserisci codice per /notizie
        await event.respond("Funzione /notizie in arrivo!")

    elif text.startswith('/rsi'):
        # TODO: inserisci codice per /rsi
        await event.respond("Funzione /rsi in arrivo!")

    elif text.startswith('/vwap'):
        # TODO: inserisci codice per /vwap
        await event.respond("Funzione /vwap in arrivo!")

    elif text.startswith('/bilancio'):
        # TODO: inserisci codice per /bilancio
        await event.respond("Funzione /bilancio in arrivo!")

    elif text.startswith('/etf'):
        # TODO: inserisci codice per /etf
        await event.respond("Funzione /etf in arrivo!")

    elif text.startswith('/previsione'):
        # TODO: inserisci codice per /previsione
        await event.respond("Funzione /previsione in arrivo!")

    elif text.startswith('/idee'):
        # TODO: inserisci codice per /idee
        await event.respond("Funzione /idee in arrivo!")
