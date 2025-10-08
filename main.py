import os
import asyncio
from dotenv import load_dotenv
import discord
from discord.ext import commands

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.voice_states = True

# Keep command_prefix for compatibility, but we'll primarily use slash commands
bot = commands.Bot(command_prefix="/", intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f"{bot.user.name} está online!")
    await bot.change_presence(activity=discord.Game(name="/help para ajuda"))
    
    # Sync slash commands
    try:
        synced = await bot.tree.sync()
        print(f"Sincronizados {len(synced)} comandos slash")
    except Exception as e:
        print(f"Falhou ao sincronizar comandos: {e}")

async def main():
    # Load all command/event cogs
    EXTENSIONS = [
        "commands.help",
        "commands.stats",
        "commands.lfg",
        "commands.maps",
        "events.error"
    ]

    for ext in EXTENSIONS:
        await bot.load_extension(ext)

    await bot.start(os.getenv("DISCORD_TOKEN"))

asyncio.run(main())
