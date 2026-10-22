"""Bot Discord: espone il comando /roll."""

from __future__ import annotations

import logging
import os

import discord
from discord import app_commands

from pbotta.dice import MAX_MODIFIER, MIN_MODIFIER, Mode, Outcome, RollResult, roll

log = logging.getLogger("pbotta")

COLORS = {
    Outcome.STRONG_HIT: discord.Color.green(),
    Outcome.WEAK_HIT: discord.Color.gold(),
    Outcome.MISS: discord.Color.red(),
}


def format_dice(result: RollResult) -> str:
    """Mostra i dadi tenuti in grassetto e quelli scartati barrati."""
    remaining = list(result.kept)
    parts = []
    for die in result.dice:
        if die in remaining:
            remaining.remove(die)
            parts.append(f"**{die}**")
        else:
            parts.append(f"~~{die}~~")
    return " ".join(parts)


def build_embed(result: RollResult, user: discord.abc.User, note: str | None) -> discord.Embed:
    title = f"{result.outcome.value} ({result.total})"
    embed = discord.Embed(title=title, color=COLORS[result.outcome])
    embed.set_author(name=user.display_name, icon_url=user.display_avatar.url)
    if note:
        embed.description = note
    embed.add_field(name="Dadi", value=format_dice(result), inline=True)
    embed.add_field(name="Modificatore", value=f"{result.modifier:+d}", inline=True)
    if result.mode is not Mode.NORMAL:
        embed.add_field(name="Modalità", value=result.mode.value.capitalize(), inline=True)
    return embed


class PBotTA(discord.Client):
    def __init__(self) -> None:
        super().__init__(intents=discord.Intents.none())
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self) -> None:
        guild_id = os.getenv("DISCORD_GUILD_ID")
        if guild_id:
            # Sincronizzazione immediata su un server di prova.
            guild = discord.Object(id=int(guild_id))
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)
        else:
            await self.tree.sync()

    async def on_ready(self) -> None:
        log.info("Connesso come %s", self.user)


client = PBotTA()


@client.tree.command(name="roll", description="Tira 2d6 + modificatore (PbtA)")
@app_commands.describe(
    mod="Modificatore da aggiungere al tiro",
    modalita="Vantaggio o svantaggio: tira 3d6 e tiene i due migliori o peggiori",
    nota="Mossa o descrizione del tiro",
)
@app_commands.choices(
    modalita=[app_commands.Choice(name=m.value.capitalize(), value=m.value) for m in Mode]
)
async def roll_command(
    interaction: discord.Interaction,
    mod: app_commands.Range[int, MIN_MODIFIER, MAX_MODIFIER] = 0,
    modalita: app_commands.Choice[str] | None = None,
    nota: app_commands.Range[str, 1, 200] | None = None,
) -> None:
    mode = Mode(modalita.value) if modalita else Mode.NORMAL
    result = roll(mod, mode)
    await interaction.response.send_message(embed=build_embed(result, interaction.user, nota))


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    token = os.environ.get("DISCORD_TOKEN")
    if not token:
        raise SystemExit("Variabile d'ambiente DISCORD_TOKEN mancante")
    client.run(token, log_handler=None)


if __name__ == "__main__":
    main()
