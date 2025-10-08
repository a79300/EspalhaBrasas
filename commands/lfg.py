import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime, timedelta
import asyncio

class LFGView(discord.ui.View):
    """View com botão para juntar-se à sessão LFG"""
    def __init__(self, cog, message_id: int):
        super().__init__(timeout=None)  # Sem timeout para manter o botão ativo
        self.cog = cog
        self.message_id = message_id
    
    @discord.ui.button(label="✅ Juntar-me", style=discord.ButtonStyle.green, custom_id="lfg_join")
    async def join_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Botão para juntar-se à sessão"""
        session = self.cog.active_lfgs.get(self.message_id)
        
        if not session:
            await interaction.response.send_message("Esta sessão já terminou!", ephemeral=True)
            return
        
        user = interaction.user
        
        # Verifica se já está na lista
        if user.id in session["players"]:
            # Remove se já estiver (toggle)
            session["players"].remove(user.id)
            # Apenas defer para não mostrar mensagem
            await interaction.response.defer()
            # Atualiza o embed
            await self.cog.update_lfg_embed(session)
        else:
            # Adiciona à lista
            session["players"].append(user.id)
            # Apenas defer para não mostrar mensagem
            await interaction.response.defer()
            
            # Se chegou a 5 jogadores, finaliza a sessão imediatamente
            if len(session["players"]) >= 5:
                await self.cog.finish_lfg_session(self.message_id, interaction.channel)
            else:
                # Atualiza o embed
                await self.cog.update_lfg_embed(session)

class LFG(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_lfgs = {}  # Store active LFG sessions
        
    @app_commands.command(name='ranked', description='Procura jogadores para jogar ranked')
    @app_commands.describe(
        game_name='Nome do jogo (ex: Valorant, CS2, League of Legends)',
        horario='Horário para começar (formato HH:MM, opcional)'
    )
    async def ranked(self, interaction: discord.Interaction, game_name: str, horario: str = None):
        """Find players to play with - creates a voting session"""
        
        # Parse and validate time if provided
        end_time = None
        time_str = ""
        
        if horario:
            try:
                # Validate HH:MM format
                hours, minutes = horario.split(':')
                hours = int(hours)
                minutes = int(minutes)
                
                if not (0 <= hours <= 23 and 0 <= minutes <= 59):
                    await interaction.response.send_message(
                        "❌ Formato inválido! Usa o formato HH:MM (ex: 14:30, 20:00)",
                        ephemeral=True
                    )
                    return
                
                # Calculate end time (5 minutes before game time)
                now = datetime.now()
                game_time = now.replace(hour=hours, minute=minutes, second=0, microsecond=0)
                
                # If game time is in the past, assume it's for tomorrow
                if game_time < now:
                    game_time += timedelta(days=1)
                
                end_time = game_time - timedelta(minutes=5)
                
                # Check if end time is in the past
                if end_time < now:
                    await interaction.response.send_message(
                        "❌ O horário especificado já passou! Escolhe um horário futuro.",
                        ephemeral=True
                    )
                    return
                
                time_str = f" às **{horario}**"
                
            except ValueError:
                await interaction.response.send_message(
                    "❌ Formato inválido! Usa o formato HH:MM (ex: 14:30, 20:00)",
                    ephemeral=True
                )
                return
        else:
            # Default: 1 hour voting duration
            end_time = datetime.now() + timedelta(hours=1)
            time_str = ""
        
        # Calculate duration for display
        duration = end_time - datetime.now()
        hours = int(duration.total_seconds() // 3600)
        minutes = int((duration.total_seconds() % 3600) // 60)
        
        if hours > 0:
            duration_str = f"{hours}h {minutes}min"
        else:
            duration_str = f"{minutes}min"
        
        # Create embed
        embed = discord.Embed(
            title=f"🎮 À procura de jogadores para {game_name}",
            description=f"{interaction.user.mention} está à procura de jogadores{time_str}!",
            color=0xFF4655
        )
        
        # Add creator's avatar
        embed.set_author(
            name=f"Criado por {interaction.user.display_name}",
            icon_url=interaction.user.display_avatar.url
        )
        embed.set_thumbnail(url=interaction.user.display_avatar.url)
        
        # Show creator as first player
        embed.add_field(
            name="📊 Jogadores Interessados (1/5)",
            value=f"1. {interaction.user.mention}",
            inline=False
        )
        
        embed.add_field(
            name="⏰ Votação termina em",
            value=f"`{duration_str}`",
            inline=True
        )
        
        if horario:
            embed.add_field(
                name="🕐 Hora do jogo",
                value=f"`{horario}`",
                inline=True
            )
        
        # Send message with button view
        await interaction.response.send_message(embed=embed)
        message = await interaction.original_response()
        
        # Store LFG session
        message_id = message.id
        self.active_lfgs[message_id] = {
            'message': message,
            'creator': interaction.user,
            'game_name': game_name,
            'end_time': end_time,
            'game_time': horario,
            'players': [interaction.user.id]  # Creator is automatically in
        }
        
        # Add button view
        view = LFGView(self, message_id)
        await message.edit(view=view)
        
        # Start timer task
        self.bot.loop.create_task(self.lfg_timer(message_id, interaction.channel))
        
        # Start auto-update task (updates countdown every 30 seconds)
        self.bot.loop.create_task(self.auto_update_countdown(message_id))
    
    async def auto_update_countdown(self, message_id: int):
        """Auto-update the countdown timer every 60 seconds"""
        
        while message_id in self.active_lfgs:
            try:
                # Wait 60 seconds before updating
                await asyncio.sleep(60)
                
                # Check if session is still active
                if message_id not in self.active_lfgs:
                    break
                
                session = self.active_lfgs[message_id]
                
                # Update the embed with new countdown
                await self.update_lfg_embed(session)
                
            except Exception as e:
                print(f"❌ Erro no auto-update: {str(e)}")
                break
    
    async def lfg_timer(self, message_id: int, channel):
        """Timer to end LFG session and notify players"""
        
        if message_id not in self.active_lfgs:
            return
        
        lfg_data = self.active_lfgs[message_id]
        end_time = lfg_data['end_time']
        
        # Wait until end time
        wait_seconds = (end_time - datetime.now()).total_seconds()
        
        if wait_seconds > 0:
            await asyncio.sleep(wait_seconds)
        
        # Check if still active (might have been completed early)
        if message_id not in self.active_lfgs:
            return
        
        # Check if we have enough players
        players = lfg_data['players']
        
        if len(players) >= 5:
            # Team is complete - finish the session normally
            await self.finish_lfg_session(message_id, channel)
        else:
            # Not enough players - cancel
            try:
                message = await channel.fetch_message(lfg_data['message'].id)
                game_name = lfg_data['game_name']
                
                embed = discord.Embed(
                    title=f"❌ Votação cancelada",
                    description=f"A sessão de **{game_name}** foi cancelada por falta de jogadores.\nApenas **{len(players)} de 5** jogadores confirmaram.",
                    color=0xFF0000
                )
                
                embed.set_footer(text="Tenta novamente mais tarde!")
                
                # Edit original message and remove button
                await message.edit(embed=embed, view=None)
                
            except discord.NotFound:
                pass  # Message was deleted
            except Exception as e:
                print(f"❌ Erro no timer LFG: {str(e)}")
            
            # Remove from active sessions
            if message_id in self.active_lfgs:
                del self.active_lfgs[message_id]
    
    async def update_lfg_embed(self, session):
        """Update the LFG embed with current player list"""
        try:
            message = session['message']
            players = session['players']
            game_name = session['game_name']
            end_time = session['end_time']
            horario = session['game_time']
            
            # Get player list with avatars as individual lines
            if len(players) > 0:
                player_list = ""
                for i, player_id in enumerate(players, 1):
                    user = await self.bot.fetch_user(player_id)
                    # Each player gets their own line with clickable avatar
                    player_list += f"{i}. {user.mention}\n"
            else:
                player_list = "Ninguém se juntou ainda..."
            
            # Calculate remaining time
            duration = end_time - datetime.now()
            hours = int(duration.total_seconds() // 3600)
            minutes = int((duration.total_seconds() % 3600) // 60)
            
            if hours > 0:
                duration_str = f"{hours}h {minutes}min"
            else:
                duration_str = f"{minutes}min"
            
            # Update embed
            embed = discord.Embed(
                title=f"🎮 À procura de jogadores para {game_name}",
                description=f"{session['creator'].mention} está à procura de jogadores{' às **' + horario + '**' if horario else ''}!",
                color=0xFF4655
            )
            
            # Add creator's avatar as author icon
            embed.set_author(
                name=f"Criado por {session['creator'].display_name}",
                icon_url=session['creator'].display_avatar.url
            )
            
            # If there are players, show the first player's avatar as thumbnail
            if len(players) > 0:
                first_player = await self.bot.fetch_user(players[0])
                embed.set_thumbnail(url=first_player.display_avatar.url)
            
            embed.add_field(
                name=f"📊 Jogadores Interessados ({len(players)}/5)",
                value=player_list,
                inline=False
            )
            
            embed.add_field(
                name="⏰ Votação termina em",
                value=f"`{duration_str}`",
                inline=True
            )
            
            if horario:
                embed.add_field(
                    name="🕐 Hora do jogo",
                    value=f"`{horario}`",
                    inline=True
                )
            
            await message.edit(embed=embed)
            
        except Exception as e:
            print(f"❌ Erro ao atualizar embed: {str(e)}")
    
    async def finish_lfg_session(self, message_id: int, channel):
        """Finish LFG session when team is full or time expires"""
        
        if message_id not in self.active_lfgs:
            return
        
        lfg_data = self.active_lfgs[message_id]
        
        try:
            message = await channel.fetch_message(lfg_data['message'].id)
            
            players = lfg_data['players']
            game_name = lfg_data['game_name']
            game_time = lfg_data['game_time']
            
            # Get user mentions list
            player_list = ""
            player_mentions = []
            for i, player_id in enumerate(players, 1):
                user = await self.bot.fetch_user(player_id)
                player_list += f"{i}. {user.mention}\n"
                player_mentions.append(user.mention)
            
            # Create final embed
            embed = discord.Embed(
                title=f"✅ Equipa formada para {game_name}!",
                description=f"**{len(players)} jogadores** confirmados!",
                color=0xFF4655
            )
            
            # Add first player's avatar as thumbnail
            first_player = await self.bot.fetch_user(players[0])
            embed.set_thumbnail(url=first_player.display_avatar.url)
            
            embed.add_field(
                name="👥 Jogadores",
                value=player_list,
                inline=False
            )
            
            if game_time:
                embed.add_field(
                    name="🕐 Hora do jogo",
                    value=f"`{game_time}`",
                    inline=False
                )
            
            embed.set_footer(text="Boa sorte e divirtam-se! 🎯")
            
            # Edit original message to show completion (instead of deleting)
            await message.edit(content=None, embed=embed, view=None)
            
            # Send notification with mentions
            notification = f"🎮 {' '.join(player_mentions)}\n\n**Equipa completa para {game_name}!**"
            if game_time:
                notification += f"\n🕐 Hora: **{game_time}**"
            
            await channel.send(notification)
            
        except discord.NotFound:
            pass  # Message was deleted
        except Exception as e:
            print(f"❌ Erro ao finalizar sessão: {str(e)}")
        
        # Remove from active sessions
        if message_id in self.active_lfgs:
            del self.active_lfgs[message_id]
    
    @app_commands.command(name='ranked-cancel', description='Cancela a tua sessão de procura de jogadores ativa')
    async def ranked_cancel(self, interaction: discord.Interaction):
        """Cancel your active LFG session"""
        
        # Find user's active LFG
        user_lfg = None
        for message_id, lfg_data in self.active_lfgs.items():
            if lfg_data['creator'].id == interaction.user.id:
                user_lfg = message_id
                break
        
        if not user_lfg:
            await interaction.response.send_message(
                "❌ Não tens nenhuma sessão ativa!",
                ephemeral=True
            )
            return
        
        # Cancel the session
        lfg_data = self.active_lfgs[user_lfg]
        
        try:
            message = lfg_data['message']
            
            embed = discord.Embed(
                title=f"❌ Sessão de {lfg_data['game_name']} cancelada",
                description=f"Cancelada por {interaction.user.mention}",
                color=0xFF0000
            )
            
            await message.edit(embed=embed, view=None)
            
        except discord.NotFound:
            pass
        
        # Remove from active sessions
        del self.active_lfgs[user_lfg]
        
        await interaction.response.send_message(
            "✅ Sessão cancelada com sucesso!",
            ephemeral=True
        )

async def setup(bot):
    await bot.add_cog(LFG(bot))
