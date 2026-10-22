# Configurazione su Discord Developer Portal

1. Apri <https://discord.com/developers/applications> e seleziona l'app.
2. **Bot**
   - Premi *Reset Token*, copia il token e mettilo in `.env` come `DISCORD_TOKEN`. Non condividerlo e non committarlo.
   - Lascia disattivati tutti i *Privileged Gateway Intents*: il bot usa solo slash command.
   - Lascia attivo *Public Bot* se vuoi che chiunque possa invitarlo.
3. **Installation** (o *OAuth2 → URL Generator*)
   - Scope: `bot` e `applications.commands`.
   - Permessi del bot: `Send Messages`, `Embed Links`. Bastano questi.
   - Copia il link d'invito e aprilo per aggiungere il bot a un server.
4. **Server di prova (facoltativo)**: attiva la modalità sviluppatore in Discord (*Impostazioni → Avanzate*), tasto destro sul server → *Copia ID server* e mettilo in `.env` come `DISCORD_GUILD_ID`. I comandi compaiono subito su quel server; senza questa variabile la registrazione globale può richiedere fino a un'ora.

# Deploy sulla VPS con Docker

```bash
git clone https://github.com/Sdrogo/PBotTA.git
cd PBotTA
cp .env.example .env    # inserisci token ed eventuale ID server
docker compose up -d --build
docker compose logs -f  # deve comparire "Connesso come ..."
```

Aggiornamento dopo nuove modifiche:

```bash
git pull
docker compose up -d --build
```

Il bot non espone porte e non usa volumi, quindi non entra in conflitto con gli altri container.
