import aiohttp
import discord
from typing import Optional, Dict, Any


def get_agent_icon(agent_name: str) -> str:
    """Retorna o URL do ícone do agente."""
    agent_icons = {
        "Jett": "https://media.valorant-api.com/agents/add6443a-41bd-e414-f6ad-e58d267f4e95/displayicon.png",
        "Reyna": "https://media.valorant-api.com/agents/a3bfb853-43b2-7238-a4f1-ad90e9e46bcc/displayicon.png",
        "Raze": "https://media.valorant-api.com/agents/f94c3b30-42be-e959-889c-5aa313dba261/displayicon.png",
        "Phoenix": "https://media.valorant-api.com/agents/eb93336a-449b-9c1b-0a54-a891f7921d69/displayicon.png",
        "Yoru": "https://media.valorant-api.com/agents/7f94d92c-4234-0a36-9646-3a87eb8b5c89/displayicon.png",
        "Neon": "https://media.valorant-api.com/agents/bb2a4828-46eb-8cd1-e765-15848195d751/displayicon.png",
        "Sage": "https://media.valorant-api.com/agents/569fdd95-4d10-43ab-ca70-79becc718b46/displayicon.png",
        "Skye": "https://media.valorant-api.com/agents/6f2a04ca-43e0-be17-7f36-b3908627744d/displayicon.png",
        "Omen": "https://media.valorant-api.com/agents/8e253930-4c05-31dd-1b6c-968525494517/displayicon.png",
        "Brimstone": "https://media.valorant-api.com/agents/9f0d8ba9-4140-b941-57d3-a7ad57c6b417/displayicon.png",
        "Astra": "https://media.valorant-api.com/agents/41fb69c1-4189-7b37-f117-bcaf1e96f1bf/displayicon.png",
        "Viper": "https://media.valorant-api.com/agents/707eab51-4836-f488-046a-cda6bf494859/displayicon.png",
        "Killjoy": "https://media.valorant-api.com/agents/1e58de9c-4950-5125-93e9-a0aee9f98746/displayicon.png",
        "Cypher": "https://media.valorant-api.com/agents/117ed9e3-49f3-6512-3ccf-0cada7e3823b/displayicon.png",
        "Sova": "https://media.valorant-api.com/agents/320b2a48-4d9b-a075-30f1-1f93a9b638fa/displayicon.png",
        "Breach": "https://media.valorant-api.com/agents/5f8d3a7f-467b-97f3-062c-13acf203c006/displayicon.png",
        "KAY/O": "https://media.valorant-api.com/agents/601dbbe7-43ce-be57-2a40-4abd24953621/displayicon.png",
        "Chamber": "https://media.valorant-api.com/agents/22697a3d-45bf-8dd7-4fec-84a9e28c69d7/displayicon.png",
        "Fade": "https://media.valorant-api.com/agents/dade69b4-4f5a-8528-247b-219e5a1facd6/displayicon.png",
        "Harbor": "https://media.valorant-api.com/agents/95b78ed7-4637-86d9-7e41-71ba8c293152/displayicon.png",
        "Gekko": "https://media.valorant-api.com/agents/e370fa57-4757-3604-3648-499e1f642d3f/displayicon.png",
        "Deadlock": "https://media.valorant-api.com/agents/cc8b64c8-4b25-4ff9-6e7f-37b4da43d235/displayicon.png",
        "Iso": "https://media.valorant-api.com/agents/0e38b510-41a8-5780-5e8f-568b2a4f2d6c/displayicon.png",
        "Clove": "https://media.valorant-api.com/agents/1dbf2edd-4729-0984-3115-daa5eed44993/displayicon.png",
        "Vyse": "https://media.valorant-api.com/agents/efba5359-4016-a1e5-7626-b1ae76895940/displayicon.png",
    }
    return agent_icons.get(agent_name, "")


def get_rank_emoji(rank: str) -> str:
    """Retorna um emoji customizado do Discord baseado no rank."""
    if not rank:
        return "<:unranked:unranked>"

    # Dicionário com emojis customizados do Discord
    # Formato: <:nome_emoji:ID> para estático ou <a:nome_emoji:ID> para animado
    rank_emojis = {
        "unranked": "<:unranked:1425255090691768335>",
        "iron1": "<:iron:1425254956772098179>",
        "iron2": "<:iron:1425254956772098179>",
        "iron3": "<:iron:1425254956772098179>",
        "bronze1": "<:bronze:1425254915730837565>",
        "bronze2": "<:bronze:1425254915730837565>",
        "bronze3": "<:bronze:1425254915730837565>",
        "silver1": "<:silver:1425254914505969664>",
        "silver2": "<:silver:1425254914505969664>",
        "silver3": "<:silver:1425254914505969664>",
        "gold1": "<:gold:1425254912735838238>",
        "gold2": "<:gold:1425254912735838238>",
        "gold3": "<:gold:1425254912735838238>",
        "platinum1": "<:platinum:1425254911163105372>",
        "platinum2": "<:platinum:1425254911163105372>",
        "platinum3": "<:platinum:1425254911163105372>",
        "diamond1": "<:diamond:1425254907102888018>",
        "diamond2": "<:diamond:1425254907102888018>",
        "diamond3": "<:diamond:1425254907102888018>",
        "ascendant1": "<:ascendant:1425254905194741910>",
        "ascendant2": "<:ascendant:1425254905194741910>",
        "ascendant3": "<:ascendant:1425254905194741910>",
        "immortal1": "<:immortal:1425254902992605256>",
        "immortal2": "<:immortal:1425254902992605256>",
        "immortal3": "<:immortal:1425254902992605256>",
        "radiant": "<:radiant:1425254900136411249>",
    }

    # Converter rank para formato de chave (lowercase sem espaços)
    rank_key = rank.lower().replace(" ", "")
    return rank_emojis.get(rank_key, "<:unranked:unranked>")


async def fetch_valorant_stats(
    username: str, tag: str, mode: str, api_key: str
) -> Dict[str, Any]:
    """
    Busca estatísticas do Valorant para um jogador específico.

    Args:
        username: Nome do jogador
        tag: Tag do jogador (sem #)
        mode: Modo de jogo ('competitive' ou 'premier')
        api_key: Chave da API Henrik

    Returns:
        Dicionário com os dados: account, mmr, recent_matches, lifetime_matches
    """
    from urllib.parse import quote

    # URL encode para suportar espaços e caracteres especiais
    username_encoded = quote(username)
    tag_encoded = quote(tag)

    headers = {"Authorization": api_key}
    timeout = aiohttp.ClientTimeout(total=30)

    async with aiohttp.ClientSession(timeout=timeout, headers=headers) as session:
        # URLs das APIs com encoding
        api_url = f"https://api.henrikdev.xyz/valorant/v1/account/{username_encoded}/{tag_encoded}"
        mmr_url = f"https://api.henrikdev.xyz/valorant/v2/mmr/eu/{username_encoded}/{tag_encoded}"
        matches_url = f"https://api.henrikdev.xyz/valorant/v3/matches/eu/{username_encoded}/{tag_encoded}?mode={mode}&size=5"
        lifetime_url = f"https://api.henrikdev.xyz/valorant/v1/lifetime/matches/eu/{username_encoded}/{tag_encoded}?mode={mode}&size=20"

        # Buscar dados da conta
        async with session.get(api_url) as response:
            if response.status != 200:
                return {"error": "account", "status": response.status}
            account_data = await response.json()

        # Buscar dados de MMR/Rank (pode não existir se não jogou ranked)
        async with session.get(mmr_url) as response:
            if response.status == 200:
                mmr_data = await response.json()
            else:
                # Se não encontrar MMR, retornar dados vazios (unranked)
                mmr_data = {"data": None}

        # Buscar partidas recentes
        async with session.get(matches_url) as response:
            if response.status != 200:
                return {"error": "matches", "status": response.status}
            matches_data = await response.json()

        # Buscar histórico de partidas para estatísticas gerais
        async with session.get(lifetime_url) as response:
            if response.status != 200:
                return {"error": "lifetime", "status": response.status}
            lifetime_data = await response.json()

        return {
            "account": account_data,
            "mmr": mmr_data,
            "matches": matches_data,
            "lifetime": lifetime_data,
        }


def create_stats_embed(data: Dict[str, Any], mode: str) -> discord.Embed:
    """
    Cria um embed com as estatísticas do jogador.

    Args:
        data: Dados retornados por fetch_valorant_stats
        mode: Modo de jogo ('competitive' ou 'premier')

    Returns:
        discord.Embed com as estatísticas formatadas
    """
    account_data = data["account"]
    mmr_data = data["mmr"]
    matches_data = data["matches"]
    lifetime_data = data["lifetime"]

    # Verificar se os dados essenciais existem
    if not account_data or "data" not in account_data:
        raise ValueError("Dados da conta não encontrados")

    # MMR pode ser None se o jogador nunca jogou ranked
    # Não lançar erro, apenas definir como Unranked

    if not matches_data or "data" not in matches_data:
        raise ValueError("Dados de partidas não encontrados")

    if not lifetime_data or "data" not in lifetime_data:
        raise ValueError("Histórico de partidas não encontrado")

    # Informações da conta
    player_name = account_data["data"].get("name", "Unknown")
    player_tag = account_data["data"].get("tag", "Unknown")
    account_level = str(account_data["data"].get("account_level", "?"))
    region = account_data["data"].get("region", "EU").upper()

    # Rank icons dictionary - URLs corretas da Valorant API
    rank_icons = {
        "unranked": "https://media.valorant-api.com/competitivetiers/03621f52-342b-cf4e-4f86-9350a49c6d04/0/largeicon.png",
        "iron1": "https://media.valorant-api.com/competitivetiers/03621f52-342b-cf4e-4f86-9350a49c6d04/3/largeicon.png",
        "iron2": "https://media.valorant-api.com/competitivetiers/03621f52-342b-cf4e-4f86-9350a49c6d04/4/largeicon.png",
        "iron3": "https://media.valorant-api.com/competitivetiers/03621f52-342b-cf4e-4f86-9350a49c6d04/5/largeicon.png",
        "bronze1": "https://media.valorant-api.com/competitivetiers/03621f52-342b-cf4e-4f86-9350a49c6d04/6/largeicon.png",
        "bronze2": "https://media.valorant-api.com/competitivetiers/03621f52-342b-cf4e-4f86-9350a49c6d04/7/largeicon.png",
        "bronze3": "https://media.valorant-api.com/competitivetiers/03621f52-342b-cf4e-4f86-9350a49c6d04/8/largeicon.png",
        "silver1": "https://media.valorant-api.com/competitivetiers/03621f52-342b-cf4e-4f86-9350a49c6d04/9/largeicon.png",
        "silver2": "https://media.valorant-api.com/competitivetiers/03621f52-342b-cf4e-4f86-9350a49c6d04/10/largeicon.png",
        "silver3": "https://media.valorant-api.com/competitivetiers/03621f52-342b-cf4e-4f86-9350a49c6d04/11/largeicon.png",
        "gold1": "https://media.valorant-api.com/competitivetiers/03621f52-342b-cf4e-4f86-9350a49c6d04/12/largeicon.png",
        "gold2": "https://media.valorant-api.com/competitivetiers/03621f52-342b-cf4e-4f86-9350a49c6d04/13/largeicon.png",
        "gold3": "https://media.valorant-api.com/competitivetiers/03621f52-342b-cf4e-4f86-9350a49c6d04/14/largeicon.png",
        "platinum1": "https://media.valorant-api.com/competitivetiers/03621f52-342b-cf4e-4f86-9350a49c6d04/15/largeicon.png",
        "platinum2": "https://media.valorant-api.com/competitivetiers/03621f52-342b-cf4e-4f86-9350a49c6d04/16/largeicon.png",
        "platinum3": "https://media.valorant-api.com/competitivetiers/03621f52-342b-cf4e-4f86-9350a49c6d04/17/largeicon.png",
        "diamond1": "https://media.valorant-api.com/competitivetiers/03621f52-342b-cf4e-4f86-9350a49c6d04/18/largeicon.png",
        "diamond2": "https://media.valorant-api.com/competitivetiers/03621f52-342b-cf4e-4f86-9350a49c6d04/19/largeicon.png",
        "diamond3": "https://media.valorant-api.com/competitivetiers/03621f52-342b-cf4e-4f86-9350a49c6d04/20/largeicon.png",
        "ascendant1": "https://media.valorant-api.com/competitivetiers/03621f52-342b-cf4e-4f86-9350a49c6d04/21/largeicon.png",
        "ascendant2": "https://media.valorant-api.com/competitivetiers/03621f52-342b-cf4e-4f86-9350a49c6d04/22/largeicon.png",
        "ascendant3": "https://media.valorant-api.com/competitivetiers/03621f52-342b-cf4e-4f86-9350a49c6d04/23/largeicon.png",
        "immortal1": "https://media.valorant-api.com/competitivetiers/03621f52-342b-cf4e-4f86-9350a49c6d04/24/largeicon.png",
        "immortal2": "https://media.valorant-api.com/competitivetiers/03621f52-342b-cf4e-4f86-9350a49c6d04/25/largeicon.png",
        "immortal3": "https://media.valorant-api.com/competitivetiers/03621f52-342b-cf4e-4f86-9350a49c6d04/26/largeicon.png",
        "radiant": "https://media.valorant-api.com/competitivetiers/03621f52-342b-cf4e-4f86-9350a49c6d04/27/largeicon.png",
    }

    # Rank
    rank = "Unranked"
    rank_emoji = "⚙️"
    rank_icon_url = rank_icons.get("unranked")
    rr = 0

    if mmr_data.get("data") and mmr_data["data"].get("current_data"):
        current_data = mmr_data["data"]["current_data"]
        rank = current_data.get("currenttierpatched", "Unranked")
        rank_emoji = get_rank_emoji(rank)
        rr = current_data.get("ranking_in_tier", 0)

        # Get rank icon from dictionary
        if rank and rank != "Unranked":
            # Remove espaços e converte para lowercase
            rank_key = rank.lower().replace(" ", "")
            rank_icon_url = rank_icons.get(rank_key)

            # Debug: printar se não encontrar o ícone
            if not rank_icon_url:
                rank_icon_url = rank_icons.get("unranked")

    # Calcular estatísticas gerais (últimas 20 partidas)
    total_kills = 0
    total_deaths = 0
    total_assists = 0
    total_headshots = 0
    total_bodyshots = 0
    total_legshots = 0
    total_dmg_per_round = 0.0
    wins = 0
    losses = 0
    agent_count = {}

    matches_played = 0
    if lifetime_data.get("data") and lifetime_data["data"]:
        for match in lifetime_data["data"]:
            if not match or "stats" not in match:
                continue

            matches_played += 1
            stats = match["stats"]

            # Kills, Deaths, Assists
            total_kills += stats.get("kills", 0)
            total_deaths += stats.get("deaths", 0)
            total_assists += stats.get("assists", 0)

            # Shots para headshot%
            if "shots" in stats:
                total_headshots += stats["shots"].get("head", 0)
                total_bodyshots += stats["shots"].get("body", 0)
                total_legshots += stats["shots"].get("leg", 0)

            # Damage per round for this match
            match_damage = (
                stats.get("damage", {}).get("made", 0)
                if isinstance(stats.get("damage"), dict)
                else 0
            )

            # Calculate total rounds from teams score
            match_rounds = 0
            if "teams" in match:
                teams = match["teams"]
                red_rounds = teams.get("red", 0)
                blue_rounds = teams.get("blue", 0)

                # Extract rounds if they are dicts
                if isinstance(red_rounds, dict):
                    red_rounds = red_rounds.get("rounds_won", 0)
                if isinstance(blue_rounds, dict):
                    blue_rounds = blue_rounds.get("rounds_won", 0)

                match_rounds = int(red_rounds) + int(blue_rounds)

            if match_rounds > 0 and match_damage > 0:
                match_dmg_per_round = match_damage / match_rounds
                total_dmg_per_round += match_dmg_per_round

            # Wins/Losses
            player_team = stats.get("team", "").lower()
            if player_team and "teams" in match:
                teams = match["teams"]

                # Extrair rounds - teams pode ser dict ou int
                red_data = teams.get("red", 0)
                blue_data = teams.get("blue", 0)

                # Se for dicionário, pegar rounds_won
                if isinstance(red_data, dict):
                    red_rounds = red_data.get("rounds_won", 0)
                else:
                    red_rounds = int(red_data) if red_data else 0

                if isinstance(blue_data, dict):
                    blue_rounds = blue_data.get("rounds_won", 0)
                else:
                    blue_rounds = int(blue_data) if blue_data else 0

                if player_team == "red":
                    if red_rounds > blue_rounds:
                        wins += 1
                    else:
                        losses += 1
                elif player_team == "blue":
                    if blue_rounds > red_rounds:
                        wins += 1
                    else:
                        losses += 1

            # Count agents
            character = stats.get("character", {}).get("name", "Unknown")
            agent_count[character] = agent_count.get(character, 0) + 1

    # Calculate averages
    kd_ratio = round(total_kills / total_deaths, 2) if total_deaths > 0 else total_kills

    total_shots = total_headshots + total_bodyshots + total_legshots
    headshot_percent = (
        round((total_headshots / total_shots) * 100, 1) if total_shots > 0 else 0
    )

    win_percent = round((wins / matches_played) * 100, 1) if matches_played > 0 else 0

    # Average DMG/Round across all matches
    avg_damage = (
        round(total_dmg_per_round / matches_played) if matches_played > 0 else 0
    )

    # Most played agent
    most_played_agent = (
        max(agent_count, key=agent_count.get) if agent_count else "Unknown"
    )
    agent_icon = get_agent_icon(most_played_agent)
    agent_games = (
        agent_count.get(most_played_agent, 0) if most_played_agent != "Unknown" else 0
    )

    # Create embed
    mode_title = "Ranked" if mode == "competitive" else "Premier"
    embed = discord.Embed(
        title=f"🎮 Valorant Profile - {player_name}#{player_tag}",
        description=f"┗━━ Region: **{region}**",
        color=0xFF4655,
    )

    # Set player card (small) as thumbnail (top right)
    if account_data.get("data") and "card" in account_data["data"]:
        card = account_data["data"].get("card")
        if card and "small" in card:
            embed.set_thumbnail(url=card["small"])

    # Set most played agent as author (top with icon)
    if agent_icon and most_played_agent != "Unknown":
        embed.set_author(
            name=f"Main: {most_played_agent} ({agent_games} matches)",
            icon_url=agent_icon,
        )

    # ═══════════════════════════════════════
    # GENERAL STATS SECTION
    # ═══════════════════════════════════════

    if matches_played > 0:  # Only show if we have stats
        # Add rank info with custom emoji
        rank_info = f"{rank_emoji} **{rank}** • Level **{account_level}** • **{wins}W - {losses}L**\n\n"

        # Create aligned stats with code block for clean table format
        stats_content = (
            f"```"
            f"K/D Ratio    {kd_ratio}\n"
            f"HS%          {headshot_percent}%\n"
            f"Win%         {win_percent}%\n"
            f"DMG/Round    {avg_damage}\n"
            f"─────────────────────\n"
            f"Kills        {total_kills}\n"
            f"Deaths       {total_deaths}\n"
            f"Assists      {total_assists}"
            f"```"
        )

        embed.add_field(
            name=f"🎯General Stats ({mode_title})",
            value=rank_info + stats_content,
            inline=False,
        )

    # Recent Match History
    if matches_data.get("data") and matches_data["data"]:
        match_history = ""
        for match in matches_data["data"][:5]:
            # Check if match and its properties exist
            if not match:
                continue
            if "players" not in match or match["players"] is None:
                continue
            if "all_players" not in match["players"]:
                continue

            # Encontrar os dados do jogador
            player_stats = None
            for player in match["players"]["all_players"]:
                if (
                    player["name"].lower() == player_name.lower()
                    and player["tag"].lower() == player_tag.lower()
                ):
                    player_stats = player
                    break

            if not player_stats:
                continue

            # Resultado
            player_team = player_stats["team"].lower()
            teams = match["teams"]
            won = False

            # Extrair rounds dos times
            red_data = teams.get("red", {})
            blue_data = teams.get("blue", {})

            if isinstance(red_data, dict):
                red_rounds = red_data.get("rounds_won", 0)
            else:
                red_rounds = int(red_data) if red_data else 0

            if isinstance(blue_data, dict):
                blue_rounds = blue_data.get("rounds_won", 0)
            else:
                blue_rounds = int(blue_data) if blue_data else 0

            if player_team == "red":
                won = red_rounds > blue_rounds
                score = f"{red_rounds}-{blue_rounds}"
            else:
                won = blue_rounds > red_rounds
                score = f"{blue_rounds}-{red_rounds}"

            result_emoji = "✅" if won else "❌"

            # Stats
            kills = player_stats["stats"]["kills"]
            deaths = player_stats["stats"]["deaths"]
            assists = player_stats["stats"]["assists"]
            match_kd = round(kills / deaths, 2) if deaths > 0 else kills

            # Map e Agent
            map_name = match["metadata"]["map"]
            agent = player_stats["character"]

            # Compact format in a single line
            line = (
                f"{result_emoji} **{map_name}** • {agent} • "
                f"`{score}` • `{kills}/{deaths}/{assists}` • `{match_kd}`"
            )

            match_history += line + "\n"

        if match_history:
            embed.add_field(name="🎯 Match History", value=match_history, inline=False)

    if len(embed.fields) == 0:
        embed.description += "\n⚠️ No statistics found for this player."

    # Add timestamp
    from datetime import datetime

    embed.timestamp = datetime.utcnow()

    embed.set_footer(
        text="Data from Henrik-3 API",
        icon_url="https://valorant-api.com/assets/img/logo.png?v=1",
    )

    # Set profile URL - URL encode to avoid invalid characters
    from urllib.parse import quote

    profile_url = f"https://tracker.gg/valorant/profile/riot/{quote(player_name)}%23{quote(player_tag)}/overview"
    embed.url = profile_url

    # Set player card (wide) as main image (bottom large banner)
    if account_data.get("data") and "card" in account_data["data"]:
        card = account_data["data"].get("card")
        if card and "wide" in card:
            embed.set_image(url=card["wide"])

    return embed
