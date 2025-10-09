import discord
from discord import app_commands
from discord.ext import commands
import urllib.request
from bs4 import BeautifulSoup
import re
import json
from datetime import datetime


class Maps(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="maps", description="Shows current Valorant competitive map rotation"
    )
    async def maps(self, interaction: discord.Interaction):
        """Shows current Valorant competitive map rotation"""

        await interaction.response.defer()

        try:
            # First, get all map names from Valorant API
            api_req = urllib.request.Request("https://valorant-api.com/v1/maps")
            api_fp = urllib.request.urlopen(api_req)
            api_data = json.loads(api_fp.read().decode("utf8"))
            api_fp.close()

            # Extract map names (filter out practice range, tutorial, etc)
            known_maps = []
            for map_data in api_data.get("data", []):
                map_name = map_data.get("displayName", "")
                coordinates = map_data.get("coordinates", "")

                # Only include competitive maps (have coordinates, not Range/Tutorial)
                if (
                    map_name
                    and coordinates
                    and "Range" not in map_name
                    and "Tutorial" not in map_name
                ):
                    known_maps.append(map_name)

            # Add headers to avoid blocking
            req = urllib.request.Request(
                "https://www.thespike.gg/valorant/maps/map-pool",
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                },
            )

            fp = urllib.request.urlopen(req)
            mybytes = fp.read()
            mystr = mybytes.decode("utf8")
            fp.close()

            # Parse HTML
            soup = BeautifulSoup(mystr, "html.parser")

            # Find the h2 with id "current-map-rotation-in-valorant"
            h2_section = soup.find("h2", {"id": "current-map-rotation-in-valorant"})

            if not h2_section:
                # Try finding by text content
                h2_section = soup.find(
                    "h2",
                    string=re.compile(
                        r"Current map rotation in VALORANT", re.IGNORECASE
                    ),
                )

            patch_text = "Unknown patch"
            maps_list = []

            if h2_section:

                # Get the content after this h2 until the next h2
                section_content = []
                for sibling in h2_section.find_next_siblings():
                    if sibling.name == "h2":
                        break
                    section_content.append(sibling)

                # Extract text from this section only
                section_text = " ".join([elem.get_text() for elem in section_content])

                # Find patch number in this section
                patch_match = re.search(
                    r"patch\s+(\d+\.\d+)", section_text, re.IGNORECASE
                )
                if patch_match:
                    patch_number = patch_match.group(1)
                    patch_text = f"Patch {patch_number}"

                # Find map names in this section only
                for element in section_content:
                    # Check all text in lists, paragraphs, etc
                    containers = element.find_all(
                        ["li", "p", "span", "div", "td", "th"]
                    )
                    for container in containers:
                        text = container.get_text(strip=True)
                        for map_name in known_maps:
                            if map_name == text and map_name not in maps_list:
                                maps_list.append(map_name)

            # Map emojis for visual appeal
            map_emojis = {
                "Ascent": "🏛️",
                "Bind": "🏜️",
                "Haven": "🏯",
                "Split": "🏙️",
                "Icebox": "❄️",
                "Breeze": "🏝️",
                "Fracture": "⚡",
                "Pearl": "🌊",
                "Lotus": "🪷",
                "Sunset": "🌅",
                "Abyss": "🕳️",
            }

            # Create embed
            embed = discord.Embed(
                title="🗺️ Competitive Map Rotation",
                description=f"```yaml\n{patch_text}\n```",
                color=discord.Color.from_rgb(255, 70, 85),  # Valorant red
            )

            # Add Valorant logo thumbnail
            embed.set_thumbnail(url="https://valorant-api.com/assets/img/logo.png?v=1")

            if maps_list and len(maps_list) > 0:
                # Sort maps alphabetically
                sorted_maps = sorted(maps_list)

                # Create formatted map list with emojis
                maps_text = ""
                for map_name in sorted_maps:
                    emoji = map_emojis.get(map_name, "🗺️")
                    maps_text += f"{emoji} **{map_name}**\n"

                embed.add_field(
                    name=f"📍 Active Maps ({len(maps_list)}/7)",
                    value=maps_text.strip(),
                    inline=False,
                )

                # Add spacing
                embed.add_field(name="\u200b", value="\u200b", inline=False)

            else:
                embed.add_field(
                    name="⚠️ Information Unavailable",
                    value="Could not fetch map list.\nPlease try again later.",
                    inline=False,
                )

            embed.set_footer(text="Source: thespike.gg • Valorant")
            embed.timestamp = datetime.utcnow()

            await interaction.followup.send(embed=embed)

        except Exception as e:
            import traceback

            traceback.print_exc()
            await interaction.followup.send("❌ Error processing map information.")


async def setup(bot):
    await bot.add_cog(Maps(bot))
