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
    print(f"{bot.user.name} is online!")
    await bot.change_presence(activity=discord.Game(name="/help"))

    # Sync slash commands
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} slash commands")
    except Exception as e:
        print(f"Failed to sync commands: {e}")


async def main():
    # Load all command/event cogs
    EXTENSIONS = [
        "commands.help",
        "commands.stats",
        "commands.lfg",
        "commands.maps",
        "commands.vlr",
        "events.error",
    ]

    for ext in EXTENSIONS:
        await bot.load_extension(ext)

    await bot.start(os.getenv("DISCORD_TOKEN"))


asyncio.run(main())
