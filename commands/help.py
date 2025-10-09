import discord
from discord.ext import commands
from discord import app_commands


class HelpCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="help", description="Shows all available commands")
    async def help(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="📋 Available Commands",
            description="List of bot commands:",
            color=discord.Color.blue(),
        )
        embed.add_field(
            name="/stats [game_mode] [player]",
            value="Get Valorant player statistics\n**Format:** `/stats competitive name#TAG` or `/stats premier name#TAG`\n**Example:** `/stats competitive Player#1234`",
            inline=False,
        )
        embed.add_field(
            name="/ranked [game_name] [time]",
            value="Find players for ranked games\n**Format:** `/ranked GameName HH:MM`\n**Example:** `/ranked Valorant 20:30`\n*Time is optional - without time, voting lasts 1h*",
            inline=False,
        )
        embed.add_field(
            name="/ranked-cancel",
            value="Cancel your active player search session",
            inline=False,
        )
        embed.add_field(
            name="/maps",
            value="Shows current competitive Valorant map rotation\n**Example:** `/maps`",
            inline=False,
        )
        embed.add_field(
            name="/vlr",
            value="Shows today's professional Valorant matches (finished, live and upcoming)\n**Example:** `/vlr`\n*Data from VLR.gg*",
            inline=False,
        )
        embed.set_footer(text="Use commands with /")

        await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot):
    await bot.add_cog(HelpCommand(bot))
