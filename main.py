import discord
import logging
from discord.ext import commands
import os

with open('bot-token', 'r') as tokenfile:
    BOT_TOKEN = (tokenfile.read())

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

intents = discord.Intents.all()
commandPrefix = 'g:'
bot = commands.Bot(command_prefix = commandPrefix, intents = intents)

bot.remove_command('help')

@bot.event
async def on_ready():
    print('Logged on!')
    extensions = ["cogs.help", "cogs.management", "cogs.game", "cogs.greetings"]
    for extension in extensions:
        await bot.load_extension(extension)

@bot.command(name="ping", aliases=["latency"])
async def ping(ctx):
    print("bot ping")
    await ctx.send(f"Pong! {round(bot.latency, 2)}ms")



bot.run(BOT_TOKEN)
