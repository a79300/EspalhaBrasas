import discord
from discord.ext import commands
from discord import app_commands

class HelpCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='help', description='Mostra todos os comandos disponíveis')
    async def help(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="📋 Comandos Disponíveis", 
            description="Lista de comandos do bot:",
            color=discord.Color.blue()
        )
        embed.add_field(
            name="/stats [game_mode] [player]", 
            value="Obtém as estatísticas de Valorant de um jogador\n**Formato:** `/stats competitive nome#TAG` ou `/stats premier nome#TAG`\n**Exemplo:** `/stats competitive Player#1234`", 
            inline=False
        )
        embed.add_field(
            name="/ranked [game_name] [horario]", 
            value="Procura jogadores para jogar ranked\n**Formato:** `/ranked NomeDoJogo HH:MM`\n**Exemplo:** `/ranked Valorant 20:30`\n*O horário é opcional - sem horário, a votação dura 1h*", 
            inline=False
        )
        embed.add_field(
            name="/ranked-cancel", 
            value="Cancela a tua sessão de procura de jogadores ativa", 
            inline=False
        )
        embed.add_field(
            name="/maps", 
            value="Mostra os mapas em rotação no Valorant competitivo\n**Exemplo:** `/maps`", 
            inline=False
        )
        embed.set_footer(text="Use os comandos com /")
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(HelpCommand(bot))
