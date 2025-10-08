import discord
from discord.ext import commands
from discord import app_commands

class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("Comando não encontrado. Use /help para ver a lista de comandos disponíveis.")
        elif isinstance(error, commands.MemberNotFound):
            await ctx.send("Membro não encontrado.")
        else:
            await ctx.send("Ocorreu um erro.")
            print(f"Erro: {error}")

    @commands.Cog.listener()
    async def on_app_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            await interaction.response.send_message(f"Comando em cooldown. Tenta novamente em {error.retry_after:.2f}s.", ephemeral=True)
        elif isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message("Não tens permissões para usar este comando.", ephemeral=True)
        else:
            await interaction.response.send_message("Ocorreu um erro ao executar o comando.", ephemeral=True)
            print(f"Erro no comando slash: {error}")

async def setup(bot):
    await bot.add_cog(ErrorHandler(bot))
