import discord
from discord.ext import commands
from discord import app_commands
import aiohttp
from bs4 import BeautifulSoup
from datetime import datetime
import re


class VLR(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def scrape_matches_from_url(self, url):
        """Scrape matches from a specific VLR.gg URL"""
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url) as response:
                if response.status != 200:
                    return []

                html = await response.text()
                soup = BeautifulSoup(html, "html.parser")

                matches = []

                # Find all match cards - VLR.gg uses 'match-item' class
                match_cards = soup.find_all("a", class_="match-item")

                for card in match_cards:
                    try:
                        match_data = {}

                        # Get match link
                        match_data["link"] = f"https://www.vlr.gg{card.get('href', '')}"

                        # Get match status/time
                        match_eta = card.find("div", class_="match-item-eta")
                        match_data["status"] = "Upcoming"
                        match_data["eta"] = ""

                        if match_eta:
                            # Check for ml div inside
                            ml_div = match_eta.find("div", class_="ml")
                            if ml_div:
                                status_div = ml_div.find("div", class_="ml-status")
                                if status_div:
                                    match_data["status"] = status_div.text.strip()

                                # Get the ETA time (ml-eta div)
                                eta_div = ml_div.find("div", class_="ml-eta")
                                if eta_div:
                                    match_data["eta"] = eta_div.text.strip()
                            else:
                                match_data["status"] = match_eta.text.strip()

                        # Get teams
                        team_divs = card.find_all("div", class_="match-item-vs-team")
                        if len(team_divs) >= 2:
                            team1_name_div = team_divs[0].find("div", class_="text-of")
                            team2_name_div = team_divs[1].find("div", class_="text-of")

                            if team1_name_div and team2_name_div:
                                match_data["team1"] = team1_name_div.get_text(
                                    strip=True
                                )
                                match_data["team2"] = team2_name_div.get_text(
                                    strip=True
                                )
                            else:
                                continue
                        else:
                            continue

                        # Get scores
                        score_divs = card.find_all(
                            "div", class_="match-item-vs-team-score"
                        )
                        if len(score_divs) >= 2:
                            match_data["score1"] = score_divs[0].text.strip()
                            match_data["score2"] = score_divs[1].text.strip()
                        else:
                            match_data["score1"] = "–"
                            match_data["score2"] = "–"

                        # Get event name
                        event_div = card.find("div", class_="match-item-event")
                        if event_div:
                            # Remove the series part to get just the event name
                            event_series = event_div.find(
                                "div", class_="match-item-event-series"
                            )
                            if event_series:
                                match_data["round"] = event_series.text.strip()
                                # Get the event name (text after series)
                                event_text = event_div.get_text(strip=True)
                                series_text = event_series.get_text(strip=True)
                                match_data["event"] = event_text.replace(
                                    series_text, ""
                                ).strip()
                            else:
                                match_data["event"] = event_div.text.strip()
                                match_data["round"] = ""
                        else:
                            match_data["event"] = "Unknown Event"
                            match_data["round"] = ""

                        # Get team flags/regions
                        match_data["flags"] = []
                        flag_spans = card.find_all("span", class_="flag")
                        for flag in flag_spans[:2]:
                            flag_class = flag.get("class", [])
                            for cls in flag_class:
                                if cls.startswith("mod-"):
                                    match_data["flags"].append(
                                        cls.replace("mod-", "").upper()
                                    )

                        matches.append(match_data)

                    except Exception as e:
                        print(f"Error parsing match: {e}")
                        continue

                return matches

    async def scrape_all_matches(self):
        """Scrape both upcoming/live matches and completed matches from today"""
        # Scrape upcoming and live matches
        upcoming_matches = await self.scrape_matches_from_url(
            "https://www.vlr.gg/matches"
        )

        # Scrape completed matches (results)
        completed_matches = await self.scrape_matches_from_url(
            "https://www.vlr.gg/matches/results"
        )

        # Combine all matches
        all_matches = []

        # Add completed matches first (sorted by most recent)
        if completed_matches:
            all_matches.extend(completed_matches[:5])  # Limit to 5 recent completed

        # Add upcoming/live matches
        if upcoming_matches:
            all_matches.extend(upcoming_matches[:10])  # Limit to 10 upcoming/live

        return all_matches

    def get_status_emoji(self, status):
        """Get emoji based on match status"""
        status_lower = status.lower()
        if "live" in status_lower:
            return "🟠"  # Orange for live
        elif "completed" in status_lower or "ago" in status_lower:
            return "🔴"  # Red for completed
        else:
            return "🟢"  # Green for upcoming

    @app_commands.command(
        name="vlr", description="Mostra os jogos de Valorant de hoje do VLR.gg"
    )
    async def vlr(self, interaction: discord.Interaction):
        await interaction.response.defer()

        matches = await self.scrape_all_matches()

        if not matches:
            embed = discord.Embed(
                title="❌ Erro",
                description="Não foi possível obter os jogos do VLR.gg",
                color=discord.Color.red(),
            )
            await interaction.followup.send(embed=embed)
            return

        if len(matches) == 0:
            embed = discord.Embed(
                title="📅 VLR.gg - Jogos de Hoje",
                description="Não há jogos programados para hoje.",
                color=discord.Color.blue(),
            )
            await interaction.followup.send(embed=embed)
            return

        # Separate matches by status
        completed = []
        live = []
        upcoming = []

        for match in matches:
            status_lower = match["status"].lower()
            if "live" in status_lower:
                live.append(match)
            elif "completed" in status_lower or "ago" in status_lower:
                completed.append(match)
            else:
                upcoming.append(match)

        # Create main embed
        embed = discord.Embed(
            title="🎮 VLR.gg - Jogos de Valorant",
            description=f"**{datetime.now().strftime('%A, %B %d, %Y').upper()}**",
            color=discord.Color.from_rgb(255, 70, 85),  # Valorant red color
            url="https://www.vlr.gg/matches",
        )

        # Add completed matches section
        if completed:
            for match in completed[:5]:
                status_emoji = self.get_status_emoji(match["status"])

                # Format team names with flags
                team1_flag = (
                    f":flag_{match['flags'][0].lower()}:"
                    if len(match.get("flags", [])) >= 1
                    else ""
                )
                team2_flag = (
                    f":flag_{match['flags'][1].lower()}:"
                    if len(match.get("flags", [])) >= 2
                    else ""
                )

                # Create compact format
                field_value = f"{team1_flag} **{match['team1']}** `{match['score1']}`\n"
                field_value += (
                    f"{team2_flag} **{match['team2']}** `{match['score2']}`\n\n"
                )
                field_value += f"**Evento:** {match['event']}\n"
                if match.get("round"):
                    field_value += f"**Fase:** {match['round']}\n"
                field_value += f"[🔗 Ver Detalhes]({match['link']})\n\u200b"  # Invisible character for spacing

                embed.add_field(
                    name=f"{status_emoji} {match['team1']} vs {match['team2']}",
                    value=field_value,
                    inline=False,
                )

        # Add live matches section
        if live:
            for match in live:
                status_emoji = self.get_status_emoji(match["status"])

                # Format team names with flags
                team1_flag = (
                    f":flag_{match['flags'][0].lower()}:"
                    if len(match.get("flags", [])) >= 1
                    else ""
                )
                team2_flag = (
                    f":flag_{match['flags'][1].lower()}:"
                    if len(match.get("flags", [])) >= 2
                    else ""
                )

                # Create compact format
                field_value = f"{team1_flag} **{match['team1']}** `{match['score1']}`\n"
                field_value += (
                    f"{team2_flag} **{match['team2']}** `{match['score2']}`\n\n"
                )
                field_value += f"**Evento:** {match['event']}\n"
                if match.get("round"):
                    field_value += f"**Fase:** {match['round']}\n"
                field_value += f"[🔗 Ver Detalhes]({match['link']})\n\u200b"  # Invisible character for spacing

                embed.add_field(
                    name=f"{status_emoji} {match['team1']} vs {match['team2']}",
                    value=field_value,
                    inline=False,
                )

        # Add upcoming matches section
        if upcoming:
            for match in upcoming[:5]:
                status_emoji = self.get_status_emoji(match["status"])

                # Format team names with flags
                team1_flag = (
                    f":flag_{match['flags'][0].lower()}:"
                    if len(match.get("flags", [])) >= 1
                    else ""
                )
                team2_flag = (
                    f":flag_{match['flags'][1].lower()}:"
                    if len(match.get("flags", [])) >= 2
                    else ""
                )

                # Create compact format
                time_info = match.get("eta", match["status"])
                field_value = f"⏰ **Upcoming** - {time_info}\n\n"
                field_value += f"{team1_flag} **{match['team1']}**\n"
                field_value += f"{team2_flag} **{match['team2']}**\n\n"
                field_value += f"**Evento:** {match['event']}\n"
                if match.get("round"):
                    field_value += f"**Fase:** {match['round']}\n"
                field_value += f"[🔗 Ver Detalhes]({match['link']})\n\u200b"  # Invisible character for spacing

                embed.add_field(
                    name=f"{status_emoji} {match['team1']} vs {match['team2']}",
                    value=field_value,
                    inline=False,
                )

        footer_text = "Dados obtidos de VLR.gg"

        embed.set_footer(text=footer_text)
        embed.timestamp = datetime.now()

        await interaction.followup.send(embed=embed)


async def setup(bot):
    await bot.add_cog(VLR(bot))
