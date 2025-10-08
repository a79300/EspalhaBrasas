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
        self.api_key = os.getenv('HENRIK_API_KEY')
    
    @app_commands.command(name="stats", description="Mostra as estatísticas de Valorant de um jogador")
    @app_commands.describe(
        game_mode='Modo de jogo (competitive ou premier)',
        player='Nome do jogador no formato nome#TAG'
    )
    @app_commands.choices(game_mode=[
        app_commands.Choice(name='Competitive', value='competitive'),
        app_commands.Choice(name='Premier', value='premier')
    ])
    async def stats_info(self, interaction: discord.Interaction, game_mode: app_commands.Choice[str], player: str):
        """
        Comando para mostrar estatísticas de Valorant.
        
        Args:
            game_mode: Modo de jogo (competitive ou premier)
            player: Nome do jogador no formato nome#TAG
        """
        await interaction.response.defer()
        
        # Validar formato player#TAG
        if '#' not in player:
            await interaction.followup.send("❌ Formato inválido! Use: `nome#TAG`\nExemplo: `Player#EUW`")
            return
        
        parts = player.split('#')
        if len(parts) != 2:
            await interaction.followup.send("❌ Formato inválido! Use: `nome#TAG`\nExemplo: `Player#EUW`")
            return
        
        player_name, player_tag = parts
        
        # Validar que não estejam vazios
        if not player_name.strip() or not player_tag.strip():
            await interaction.followup.send("❌ Nome e TAG não podem estar vazios!")
            return
        
        # Validar tag (1-6 caracteres)
        if not (1 <= len(player_tag) <= 6):
            await interaction.followup.send("❌ A TAG deve ter entre 1 e 6 caracteres!")
            return
        
        try:
            # Buscar dados da API
            mode_value = game_mode.value
            data = await fetch_valorant_stats(player_name, player_tag, mode_value, self.api_key)
            
            # Criar embed
            mode_name = "Competitive" if mode_value == "competitive" else "Premier"
            embed = create_stats_embed(data, mode_name)
            
            # Enviar resposta
            await interaction.followup.send(embed=embed)
            
        except Exception as e:
            error_msg = str(e)
            if "Player not found" in error_msg or "404" in error_msg:
                await interaction.followup.send(f"❌ Jogador `{player}` não encontrado!")
            elif "No data found" in error_msg:
                await interaction.followup.send(f"❌ Sem dados disponíveis para `{player}` em modo {mode_name}!")
            else:
                await interaction.followup.send(f"❌ Erro ao obter estatísticas: {error_msg}")

async def setup(bot):
    await bot.add_cog(Stats(bot))
