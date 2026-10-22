# PBotTA

Dice roller Discord per i giochi *Powered by the Apocalypse*.

## Comando

`/pbta [mod] [modalita] [nota]`

Il nome del comando si può cambiare con `COMMAND_NAME` in `.env` (solo minuscole, cifre, `-` e `_`).

- `mod`: modificatore da -10 a +10 (default 0)
- `modalita`: normale, vantaggio o svantaggio (3d6, tiene i due migliori o peggiori)
- `nota`: mossa o descrizione, mostrata nel risultato

Esito: 10+ successo pieno, 7-9 successo parziale, 6- fallimento.

## Avvio in locale

```bash
pip install -r requirements-dev.txt
cp .env.example .env   # inserisci il token
export $(grep -v '^#' .env | xargs)
python -m pbotta.bot
```

Con `DISCORD_GUILD_ID` impostato i comandi vengono registrati subito su quel server; senza, la registrazione globale può richiedere fino a un'ora.

## Docker

```bash
cp .env.example .env   # inserisci il token
docker compose up -d --build
```

Guida completa a Developer Portal e deploy: [docs/setup-discord.md](docs/setup-discord.md).

## Test

```bash
pytest
```

## Legale

- [Termini di Servizio](docs/terms.md)
- [Informativa sulla privacy](docs/privacy.md)
