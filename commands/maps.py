import discord
from discord import app_commands
from discord.ext import commands
import urllib.request
from bs4 import BeautifulSoup
import re
import json

class Maps(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name='maps', description='Mostra os mapas em rotação no Valorant competitivo')
    async def maps(self, interaction: discord.Interaction):
        """Shows current Valorant competitive map rotation"""
        
        await interaction.response.defer()
        
        try:
            # First, get all map names from Valorant API
            api_req = urllib.request.Request('https://valorant-api.com/v1/maps')
            api_fp = urllib.request.urlopen(api_req)
            api_data = json.loads(api_fp.read().decode("utf8"))
            api_fp.close()
            
            # Extract map names (filter out practice range, tutorial, etc)
            known_maps = []
            for map_data in api_data.get('data', []):
                map_name = map_data.get('displayName', '')
                coordinates = map_data.get('coordinates', '')
                
                # Only include competitive maps (have coordinates, not Range/Tutorial)
                if (map_name and 
                    coordinates and 
                    'Range' not in map_name and 
                    'Tutorial' not in map_name):
                    known_maps.append(map_name)
            
            # Add headers to avoid blocking
            req = urllib.request.Request(
                'https://www.thespike.gg/valorant/maps/map-pool',
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
            )
            
            fp = urllib.request.urlopen(req)
            mybytes = fp.read()
            mystr = mybytes.decode("utf8")
            fp.close()
            
            # Parse HTML
            soup = BeautifulSoup(mystr, 'html.parser')
            
            # Find the h2 with id "current-map-rotation-in-valorant"
            h2_section = soup.find('h2', {'id': 'current-map-rotation-in-valorant'})
            
            if not h2_section:
                # Try finding by text content
                h2_section = soup.find('h2', string=re.compile(r'Current map rotation in VALORANT', re.IGNORECASE))
            
            patch_text = "Patch desconhecido"
            maps_list = []
            
            if h2_section:
                
                # Get the content after this h2 until the next h2
                section_content = []
                for sibling in h2_section.find_next_siblings():
                    if sibling.name == 'h2':
                        break
                    section_content.append(sibling)
                
                # Extract text from this section only
                section_text = ' '.join([elem.get_text() for elem in section_content])
                
                # Find patch number in this section
                patch_match = re.search(r'patch\s+(\d+\.\d+)', section_text, re.IGNORECASE)
                if patch_match:
                    patch_number = patch_match.group(1)
                    patch_text = f"Patch {patch_number}"
                
                # Find map names in this section only
                for element in section_content:
                    # Check all text in lists, paragraphs, etc
                    containers = element.find_all(['li', 'p', 'span', 'div', 'td', 'th'])
                    for container in containers:
                        text = container.get_text(strip=True)
                        for map_name in known_maps:
                            if map_name == text and map_name not in maps_list:
                                maps_list.append(map_name)
            
            
            # Create embed
            embed = discord.Embed(
                title="🗺️ Rotação de Mapas - Valorant Competitivo",
                description=f"**{patch_text}**",
                color=0xFF4655
            )
            
            if maps_list and len(maps_list) > 0:
                maps_text = "\n".join([f"• {map_name}" for map_name in sorted(maps_list)])
                embed.add_field(
                    name=f"📍 Mapas em Rotação ({len(maps_list)}/7)",
                    value=maps_text,
                    inline=False
                )
            else:
                embed.add_field(
                    name="📍 Mapas em Rotação",
                    value="Não foi possível obter a lista de mapas.\nO site pode estar a usar JavaScript para carregar os dados.",
                    inline=False
                )
            
            embed.set_footer(text="Fonte: thespike.gg")
            
            await interaction.followup.send(embed=embed)
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            await interaction.followup.send("❌ Erro ao processar informações dos mapas.")

async def setup(bot):
    await bot.add_cog(Maps(bot))
