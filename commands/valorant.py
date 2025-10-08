import discord
from discord.ext import commands
from discord import app_commands
import aiohttp
import os

class Valorant(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        # Agent icons dictionary
        self.agent_icons = {
            'astra': 'https://media.valorant-api.com/agents/41fb69c1-4189-7b37-f117-bcaf1e96f1bf/displayicon.png',
            'breach': 'https://media.valorant-api.com/agents/5f8d3a7f-467b-97f3-062c-13acf203c006/displayicon.png',
            'brimstone': 'https://media.valorant-api.com/agents/9f0d8ba9-4140-b941-57d3-a7ad57c6b417/displayicon.png',
            'chamber': 'https://media.valorant-api.com/agents/22697a3d-45bf-8dd7-4fec-84a9e28c69d7/displayicon.png',
            'clove': 'https://media.valorant-api.com/agents/1dbf2edd-4729-0984-3115-daa5eed44993/displayicon.png',
            'cypher': 'https://media.valorant-api.com/agents/117ed9e3-49f3-6512-3ccf-0cada7e3823b/displayicon.png',
            'deadlock': 'https://media.valorant-api.com/agents/cc8b64c8-4b25-4ff9-6e7f-37b4da43d235/displayicon.png',
            'fade': 'https://media.valorant-api.com/agents/dade69b4-4f5a-8528-247b-219e5a1facd6/displayicon.png',
            'gekko': 'https://media.valorant-api.com/agents/e370fa57-4757-3604-3648-499e1f642d3f/displayicon.png',
            'harbor': 'https://media.valorant-api.com/agents/95b78ed7-4637-86d9-7e41-71ba8c293152/displayicon.png',
            'iso': 'https://media.valorant-api.com/agents/0e38b510-41a8-5780-5e8f-568b2a4f2d6c/displayicon.png',
            'jett': 'https://media.valorant-api.com/agents/add6443a-41bd-e414-f6ad-e58d267f4e95/displayicon.png',
            'kayo': 'https://media.valorant-api.com/agents/601dbbe7-43ce-be57-2a40-4abd24953621/displayicon.png',
            'killjoy': 'https://media.valorant-api.com/agents/1e58de9c-4950-5125-93e9-a0aee9f98746/displayicon.png',
            'neon': 'https://media.valorant-api.com/agents/bb2a4828-46eb-8cd1-e765-15848195d751/displayicon.png',
            'omen': 'https://media.valorant-api.com/agents/8e253930-4c05-31dd-1b6c-968525494517/displayicon.png',
            'phoenix': 'https://media.valorant-api.com/agents/eb93336a-449b-9c1b-0a54-a891f7921d69/displayicon.png',
            'raze': 'https://media.valorant-api.com/agents/f94c3b30-42be-e959-889c-5aa313dba261/displayicon.png',
            'reyna': 'https://media.valorant-api.com/agents/a3bfb853-43b2-7238-a4f1-ad90e9e46bcc/displayicon.png',
            'sage': 'https://media.valorant-api.com/agents/569fdd95-4d10-43ab-ca70-79becc718b46/displayicon.png',
            'skye': 'https://media.valorant-api.com/agents/6f2a04ca-43e0-be17-7f36-b3908627744d/displayicon.png',
            'sova': 'https://media.valorant-api.com/agents/320b2a48-4d9b-a075-30f1-1f93a9b638fa/displayicon.png',
            'viper': 'https://media.valorant-api.com/agents/707eab51-4836-f488-046a-cda6bf494859/displayicon.png',
            'vyse': 'https://media.valorant-api.com/agents/efba5359-4016-a1e5-7626-b1ae76895940/displayicon.png',
            'yoru': 'https://media.valorant-api.com/agents/7f94d92c-4234-0a36-9646-3a87eb8b5c89/displayicon.png',
        }
        
        
        # Rank icons dictionary - URLs corretas da Valorant API
        self.rank_icons = {
            'unranked': 'https://media.valorant-api.com/competitivetiers/03621f52-342b-cf4e-4f86-9350a49c6d04/0/largeicon.png',
            'iron1': 'https://media.valorant-api.com/competitivetiers/03621f52-342b-cf4e-4f86-9350a49c6d04/3/largeicon.png',
            'iron2': 'https://media.valorant-api.com/competitivetiers/03621f52-342b-cf4e-4f86-9350a49c6d04/4/largeicon.png',
            'iron3': 'https://media.valorant-api.com/competitivetiers/03621f52-342b-cf4e-4f86-9350a49c6d04/5/largeicon.png',
            'bronze1': 'https://media.valorant-api.com/competitivetiers/03621f52-342b-cf4e-4f86-9350a49c6d04/6/largeicon.png',
            'bronze2': 'https://media.valorant-api.com/competitivetiers/03621f52-342b-cf4e-4f86-9350a49c6d04/7/largeicon.png',
            'bronze3': 'https://media.valorant-api.com/competitivetiers/03621f52-342b-cf4e-4f86-9350a49c6d04/8/largeicon.png',
            'silver1': 'https://media.valorant-api.com/competitivetiers/03621f52-342b-cf4e-4f86-9350a49c6d04/9/largeicon.png',
            'silver2': 'https://media.valorant-api.com/competitivetiers/03621f52-342b-cf4e-4f86-9350a49c6d04/10/largeicon.png',
            'silver3': 'https://media.valorant-api.com/competitivetiers/03621f52-342b-cf4e-4f86-9350a49c6d04/11/largeicon.png',
            'gold1': 'https://media.valorant-api.com/competitivetiers/03621f52-342b-cf4e-4f86-9350a49c6d04/12/largeicon.png',
            'gold2': 'https://media.valorant-api.com/competitivetiers/03621f52-342b-cf4e-4f86-9350a49c6d04/13/largeicon.png',
            'gold3': 'https://media.valorant-api.com/competitivetiers/03621f52-342b-cf4e-4f86-9350a49c6d04/14/largeicon.png',
            'platinum1': 'https://media.valorant-api.com/competitivetiers/03621f52-342b-cf4e-4f86-9350a49c6d04/15/largeicon.png',
            'platinum2': 'https://media.valorant-api.com/competitivetiers/03621f52-342b-cf4e-4f86-9350a49c6d04/16/largeicon.png',
            'platinum3': 'https://media.valorant-api.com/competitivetiers/03621f52-342b-cf4e-4f86-9350a49c6d04/17/largeicon.png',
            'diamond1': 'https://media.valorant-api.com/competitivetiers/03621f52-342b-cf4e-4f86-9350a49c6d04/18/largeicon.png',
            'diamond2': 'https://media.valorant-api.com/competitivetiers/03621f52-342b-cf4e-4f86-9350a49c6d04/19/largeicon.png',
            'diamond3': 'https://media.valorant-api.com/competitivetiers/03621f52-342b-cf4e-4f86-9350a49c6d04/20/largeicon.png',
            'ascendant1': 'https://media.valorant-api.com/competitivetiers/03621f52-342b-cf4e-4f86-9350a49c6d04/21/largeicon.png',
            'ascendant2': 'https://media.valorant-api.com/competitivetiers/03621f52-342b-cf4e-4f86-9350a49c6d04/22/largeicon.png',
            'ascendant3': 'https://media.valorant-api.com/competitivetiers/03621f52-342b-cf4e-4f86-9350a49c6d04/23/largeicon.png',
            'immortal1': 'https://media.valorant-api.com/competitivetiers/03621f52-342b-cf4e-4f86-9350a49c6d04/24/largeicon.png',
            'immortal2': 'https://media.valorant-api.com/competitivetiers/03621f52-342b-cf4e-4f86-9350a49c6d04/25/largeicon.png',
            'immortal3': 'https://media.valorant-api.com/competitivetiers/03621f52-342b-cf4e-4f86-9350a49c6d04/26/largeicon.png',
            'radiant': 'https://media.valorant-api.com/competitivetiers/03621f52-342b-cf4e-4f86-9350a49c6d04/27/largeicon.png'
        }

    @app_commands.command(name='ranked', description='Obtém as estatísticas competitivas de um jogador de Valorant')
    @app_commands.describe(playername='Nome do jogador no formato: utilizador#TAG')
    async def valorant_ranked(self, interaction: discord.Interaction, playername: str):
        """Fetch Valorant player information from Henrik's API"""
        await interaction.response.defer()
        
        # Validate the playername format
        if '#' not in playername:
            await interaction.followup.send("❌ Formato inválido! Usa o formato: `utilizador#TAG` (ex: Jogador#1234)")
            return
        
        parts = playername.split('#')
        if len(parts) != 2:
            await interaction.followup.send("❌ Formato inválido! Usa o formato: `utilizador#TAG` (ex: Jogador#1234)")
            return
        
        username, tag = parts
        
        # Validar que não estejam vazios
        if not username.strip() or not tag.strip():
            await interaction.followup.send("❌ Nome e TAG não podem estar vazios!")
            return
        
        if not username or not tag or len(tag) > 6:
            await interaction.followup.send("❌ Formato inválido! A tag deve ter entre 1 e 6 caracteres.")
            return
        
        # URL encode para caracteres especiais
        from urllib.parse import quote
        username_encoded = quote(username)
        tag_encoded = quote(tag)
        
        # Construct the API URLs
        api_url = f"https://api.henrikdev.xyz/valorant/v1/account/{username_encoded}/{tag_encoded}"
        mmr_url = f"https://api.henrikdev.xyz/valorant/v2/mmr/eu/{username_encoded}/{tag_encoded}"
        matches_url = f"https://api.henrikdev.xyz/valorant/v3/matches/eu/{username_encoded}/{tag_encoded}?size=5"
        # Get lifetime stats (all seasons)
        lifetime_url = f"https://api.henrikdev.xyz/valorant/v1/lifetime/matches/eu/{username_encoded}/{tag_encoded}?mode=competitive&size=20"
        profile_url = f"https://tracker.gg/valorant/profile/riot/{username_encoded}%23{tag_encoded}/overview"
        
        session = None
        try:
            timeout = aiohttp.ClientTimeout(total=30)
            session = aiohttp.ClientSession(timeout=timeout)
            
            # Get Henrik API key
            henrik_api_key = os.getenv("HENRIK_API_KEY")
            
            if not henrik_api_key or henrik_api_key == "your_henrik_api_key_here":
                await interaction.followup.send(
                    "❌ **API Key do Henrik não configurada!**\n\n"
                    "Para obter uma API key GRATUITA:\n"
                    "1. Entra no Discord do Henrik: https://discord.gg/X3GaVkX2YN\n"
                    "2. Vai ao canal de bots\n"
                    "3. Usa o comando `/api-key`\n"
                    "4. Adiciona ao `.env`: `HENRIK_API_KEY=a_tua_chave`"
                )
                return
            
            headers = {
                'Authorization': henrik_api_key,
                'User-Agent': 'Discord Bot - Valorant Stats',
                'Accept': 'application/json'
            }
            
            # Get account info
            async with session.get(api_url, headers=headers) as response:
                if response.status != 200:
                    await interaction.followup.send(f"❌ Erro ao obter dados da conta (Status: {response.status})")
                    return
                account_data = await response.json()
            
            # Get MMR info
            async with session.get(mmr_url, headers=headers) as response:
                mmr_data = await response.json() if response.status == 200 else None
            
            # Get matches
            async with session.get(matches_url, headers=headers) as response:
                matches_data = await response.json() if response.status == 200 else None
            
            # Get lifetime stats for general statistics
            async with session.get(lifetime_url, headers=headers) as response:
                lifetime_data = await response.json() if response.status == 200 else None
            
            # ═══════════════════════════════════════
            # CREATE EMBED
            # ═══════════════════════════════════════
            
            # Get account info first
            account_level = "?"
            region = "EU"
            
            if account_data.get('status') == 200 and 'data' in account_data:
                data = account_data['data']
                account_level = str(data.get('account_level', '?'))
                region = data.get('region', 'EU').upper()
            
            embed = discord.Embed(
                title=f"🎮 Perfil Valorant - {playername}",
                description=f"┗━━ Região: **{region}**",
                color=0xFF4655
            )
            
            # Get rank info first to set as main image
            current_rank = "Unranked"
            rank_emoji = "🎮"
            rank_icon_url = self.rank_icons.get('unranked')
            rr = 0
            
            if mmr_data and mmr_data.get('status') == 200 and 'data' in mmr_data:
                data = mmr_data['data']
                current_data = data.get('current_data', {})
                if current_data:
                    current_rank = current_data.get('currenttierpatched', 'Unranked')
                    rank_emoji = self.get_rank_emoji(current_rank)
                    rr = current_data.get('ranking_in_tier', 0)
                    
                    # Get rank icon from dictionary
                    rank_key = current_rank.lower().replace(' ', '')
                    rank_icon_url = self.rank_icons.get(rank_key, self.rank_icons.get('unranked'))
            
            # Set rank icon as main image (bottom)
            if rank_icon_url:
                embed.set_image(url=rank_icon_url)
            
            # Set player card (small) as thumbnail (top right)
            if account_data.get('status') == 200 and 'data' in account_data:
                data = account_data['data']
                
                if 'card' in data and 'small' in data['card']:
                    embed.set_thumbnail(url=data['card']['small'])
            
            # ═══════════════════════════════════════
            # CALCULATE GENERAL STATS FROM LIFETIME/SEASON DATA
            # ═══════════════════════════════════════
            
            # Variables for general stats
            total_kills = 0
            total_deaths = 0
            total_assists = 0
            wins = 0
            losses = 0
            total_damage = 0
            total_rounds = 0
            hs_percentages = []  # List to store HS% from each match
            agent_counter = {}  # Count most played agents
            
            # Use lifetime data for general stats (20 recent competitive matches)
            if lifetime_data and lifetime_data.get('status') == 200 and 'data' in lifetime_data:
                lifetime_matches = lifetime_data['data']
                
                for match in lifetime_matches:
                    if 'stats' not in match:
                        continue
                    
                    stats = match['stats']
                    
                    # Track agent usage
                    agent_name = stats.get('character', {}).get('name', 'Unknown')
                    agent_counter[agent_name] = agent_counter.get(agent_name, 0) + 1
                    
                    # Basic stats
                    total_kills += stats.get('kills', 0)
                    total_deaths += stats.get('deaths', 0)
                    total_assists += stats.get('assists', 0)
                    
                    # Calculate HS% for this match using shots data
                    shots = stats.get('shots', {})
                    if isinstance(shots, dict):
                        match_headshots = shots.get('head', 0)
                        match_bodyshots = shots.get('body', 0)
                        match_legshots = shots.get('leg', 0)
                        
                        # Total shots hit in this match
                        match_total_shots = match_headshots + match_bodyshots + match_legshots
                        
                        # Calculate HS% for this match and add to list
                        if match_total_shots > 0:
                            match_hs_pct = (match_headshots / match_total_shots) * 100
                            hs_percentages.append(match_hs_pct)
                    
                    # Total damage dealt
                    damage = stats.get('damage', {})
                    if isinstance(damage, dict):
                        total_damage += damage.get('made', 0)
                    
                    # Win/Loss calculation - Check player's team and compare rounds
                    player_team = stats.get('team', '').lower()  # 'red' or 'blue'
                    teams = match.get('teams', {})
                    
                    if player_team and teams:
                        try:
                            # Teams pode ser dict com rounds_won ou apenas números
                            red_data = teams.get('red', 0)
                            blue_data = teams.get('blue', 0)
                            
                            # Extrair o número de rounds
                            if isinstance(red_data, dict):
                                red_rounds = red_data.get('rounds_won', 0)
                            else:
                                red_rounds = int(red_data) if red_data else 0
                                
                            if isinstance(blue_data, dict):
                                blue_rounds = blue_data.get('rounds_won', 0)
                            else:
                                blue_rounds = int(blue_data) if blue_data else 0
                            
                            # Check if player's team won
                            if player_team == 'red':
                                if red_rounds > blue_rounds:
                                    wins += 1
                                else:
                                    losses += 1
                            elif player_team == 'blue':
                                if blue_rounds > red_rounds:
                                    wins += 1
                                else:
                                    losses += 1
                        except (TypeError, ValueError) as e:
                            print(f"⚠️ Erro ao processar win/loss: {e}")
                            print(f"   red_data: {red_data}, blue_data: {blue_data}")
                            continue
                    
                    # Count rounds played (estimate from team scores)
                    if teams:
                        try:
                            red_data = teams.get('red', 0)
                            blue_data = teams.get('blue', 0)
                            
                            # Extrair rounds para contagem total
                            if isinstance(red_data, dict):
                                total_rounds += red_data.get('rounds_won', 0)
                            else:
                                total_rounds += int(red_data) if red_data else 0
                                
                            if isinstance(blue_data, dict):
                                total_rounds += blue_data.get('rounds_won', 0)
                            else:
                                total_rounds += int(blue_data) if blue_data else 0
                        except (TypeError, ValueError) as e:
                            print(f"⚠️ Erro ao contar rounds: {e}")
                            continue
            
            # Calculate percentages from lifetime stats
            games = wins + losses
            kd = round(total_kills / total_deaths, 2) if total_deaths > 0 else total_kills
            
            # Calculate average HS% across all matches
            hs_pct = round(sum(hs_percentages) / len(hs_percentages), 1) if hs_percentages else 0
            
            win_pct = round((wins / games * 100), 1) if games > 0 else 0
            
            # DMG/Round - total_rounds is sum of all rounds from all games
            dmg_round = round(total_damage / total_rounds, 1) if total_rounds > 0 else 0
            
            # Get most played agent
            most_played_agent = None
            if agent_counter:
                most_played_agent = max(agent_counter, key=agent_counter.get)
                agent_icon_url = self.get_agent_icon(most_played_agent)
                if agent_icon_url:
                    embed.set_author(
                        name=f"Main: {most_played_agent} ({agent_counter[most_played_agent]} partidas)",
                        icon_url=agent_icon_url
                    )
            
            # ═══════════════════════════════════════
            # GENERAL STATS SECTION
            # ═══════════════════════════════════════
            
            if games > 0:  # Only show if we have stats
                # Header with rank and W/L (sem emoji porque já temos a thumbnail do rank)
                stats_header = f"**{current_rank}** • Nível **{account_level}** • **{wins}W - {losses}L**\n"
                
                # Create aligned stats with code block for clean table format
                stats_content = (
                    f"```"
                    f"K/D Ratio    {kd}\n"
                    f"HS%          {hs_pct}%\n"
                    f"Win%         {win_pct}%\n"
                    f"DMG/Round    {dmg_round}\n"
                    f"─────────────────────\n"
                    f"Kills        {total_kills}\n"
                    f"Deaths       {total_deaths}\n"
                    f"Assists      {total_assists}"
                    f"```"
                )
                
                embed.add_field(
                    name="📊 Estatísticas Gerais (Últimas 20 Partidas Competitivas)",
                    value=stats_header + stats_content,
                    inline=False
                )
            
            # ═══════════════════════════════════════
            # MATCH HISTORY (Bottom Section) - Last 5 matches
            # ═══════════════════════════════════════
            
            if matches_data and matches_data.get('status') == 200 and 'data' in matches_data:
                matches = matches_data['data']
                match_lines = []
                
                for match in matches[:5]:
                    if 'players' not in match or 'all_players' not in match['players']:
                        continue
                    
                    for player in match['players']['all_players']:
                        if player.get('name', '').lower() != username.lower():
                            continue
                        if player.get('tag', '').lower() != tag.lower():
                            continue
                        
                        # Match details
                        stats = player.get('stats', {})
                        k = stats.get('kills', 0)
                        d = stats.get('deaths', 0)
                        a = stats.get('assists', 0)
                        
                        metadata = match.get('metadata', {})
                        map_name = metadata.get('map', 'Unknown')
                        agent = player.get('character', 'Unknown')
                        
                        # Score
                        team = player.get('team', '').lower()
                        teams = match.get('teams', {})
                        
                        if team == 'red':
                            won = teams.get('red', {}).get('has_won', False)
                            r_rounds = teams.get('red', {}).get('rounds_won', 0)
                            b_rounds = teams.get('blue', {}).get('rounds_won', 0)
                            score = f"{r_rounds}:{b_rounds}"
                        else:
                            won = teams.get('blue', {}).get('has_won', False)
                            b_rounds = teams.get('blue', {}).get('rounds_won', 0)
                            r_rounds = teams.get('red', {}).get('rounds_won', 0)
                            score = f"{b_rounds}:{r_rounds}"
                        
                        result = "✅" if won else "❌"
                        match_kd = round(k / d, 2) if d > 0 else k
                        
                        # Compact format in a single line
                        line = (
                            f"{result} **{map_name}** • {agent} • "
                            f"`{score}` • `{k}/{d}/{a}` • `{match_kd}`"
                        )
                        
                        match_lines.append(line)
                        break
                
                if match_lines:
                    embed.add_field(
                        name="🎯 Histórico de Partidas",
                        value="\n".join(match_lines),
                        inline=False
                    )
            
            if len(embed.fields) == 0:
                embed.description += "\n⚠️ Não foram encontradas estatísticas para este jogador."
            
            # Add timestamp
            from datetime import datetime
            embed.timestamp = datetime.utcnow()
            
            embed.set_footer(
                text="Dados da API Henrik-3",
                icon_url="https://i.imgur.com/JgB0Kxw.png"
            )
            embed.url = profile_url
            
            await interaction.followup.send(embed=embed)
                    
        except aiohttp.ClientError as e:
            await interaction.followup.send(f"❌ Erro de rede: {str(e)}")
        except Exception as e:
            print(f"❌ Erro: {str(e)}")
            import traceback
            traceback.print_exc()
            await interaction.followup.send(f"❌ Ocorreu um erro: {str(e)}")
        finally:
            if session:
                await session.close()
    
    def get_agent_icon(self, agent_name: str) -> str:
        """Get agent icon URL from name"""
        agent_lower = agent_name.lower()
        return self.agent_icons.get(agent_lower, '')
    
    def get_rank_emoji(self, rank: str) -> str:
        """Get emoji for rank tier"""
        rank_lower = rank.lower()
        if 'radiant' in rank_lower:
            return '💎'
        elif 'immortal' in rank_lower:
            return '👑'
        elif 'ascendant' in rank_lower:
            return '🌟'
        elif 'diamond' in rank_lower:
            return '💠'
        elif 'platinum' in rank_lower:
            return '🔷'
        elif 'gold' in rank_lower:
            return '🥇'
        elif 'silver' in rank_lower:
            return '🥈'
        elif 'bronze' in rank_lower:
            return '🥉'
        elif 'iron' in rank_lower:
            return '⚙️'
        else:
            return '🎮'

async def setup(bot):
    await bot.add_cog(Valorant(bot))
