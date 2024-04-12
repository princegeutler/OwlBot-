from dotenv import load_dotenv
import os
import discord
from discord.ext import commands

# Load environment variables
load_dotenv()

# Get bot token from environment variables
BOT_TOKEN = os.environ.get('BOT_TOKEN')

# Create bot instance with custom intents
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# Event triggered when the bot is ready
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} - {bot.user.id}")

# Start the bot
bot.run(BOT_TOKEN)
