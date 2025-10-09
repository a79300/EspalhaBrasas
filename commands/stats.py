import discord
from discord import app_commands
from discord.ext import commands
import os
import sys

# Adicionar o diretório pai ao path para importar utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.valorant_stats import fetch_valorant_stats, create_stats_embed


class Stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_key = os.getenv("HENRIK_API_KEY")

    @app_commands.command(name="stats", description="Shows Valorant player statistics")
    @app_commands.describe(
        game_mode="Game mode (competitive or premier)",
        player="Player name in name#TAG format",
    )
    @app_commands.choices(
        game_mode=[
            app_commands.Choice(name="Competitive", value="competitive"),
            app_commands.Choice(name="Premier", value="premier"),
        ]
    )
    async def stats_info(
        self,
        interaction: discord.Interaction,
        game_mode: app_commands.Choice[str],
        player: str,
    ):
        """
        Command to show Valorant statistics.

        Args:
            game_mode: Game mode (competitive or premier)
            player: Player name in name#TAG format
        """
        await interaction.response.defer()

        # Validate player#TAG format
        if "#" not in player:
            await interaction.followup.send(
                "❌ Invalid format! Use: `name#TAG`\nExample: `Player#EUW`"
            )
            return

        parts = player.split("#")
        if len(parts) != 2:
            await interaction.followup.send(
                "❌ Invalid format! Use: `name#TAG`\nExample: `Player#EUW`"
            )
            return

        player_name, player_tag = parts

        # Validate they're not empty
        if not player_name.strip() or not player_tag.strip():
            await interaction.followup.send("❌ Name and TAG cannot be empty!")
            return

        # Validate tag (1-6 characters)
        if not (1 <= len(player_tag) <= 6):
            await interaction.followup.send(
                "❌ TAG must be between 1 and 6 characters!"
            )
            return

        try:
            # Fetch API data
            mode_value = game_mode.value
            data = await fetch_valorant_stats(
                player_name, player_tag, mode_value, self.api_key
            )

            # Create embed
            mode_name = "Competitive" if mode_value == "competitive" else "Premier"
            embed = create_stats_embed(data, mode_name)

            # Send response
            await interaction.followup.send(embed=embed)

        except Exception as e:
            error_msg = str(e)
            if "Player not found" in error_msg or "404" in error_msg:
                await interaction.followup.send(f"❌ Player `{player}` not found!")
            elif "No data found" in error_msg:
                await interaction.followup.send(
                    f"❌ No data available for `{player}` in {mode_name} mode!"
                )
            else:
                await interaction.followup.send(f"❌ Error fetching stats: {error_msg}")


async def setup(bot):
    await bot.add_cog(Stats(bot))
