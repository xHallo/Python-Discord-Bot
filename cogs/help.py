import discord
from discord.ext import commands

class helpCommand(commands.Cog, name="help"):
    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    async def help(self, ctx, *args):
        embed = discord.Embed(color=0x175f27)
        embed.description = "Hello, and welcome! I have a couple of commands that you may find useful! \n g:tictactoe \n g:nihao \n g:test \n g:help2"
        embed.set_author(name="Testing bot")
        await ctx.send(embed=embed)
        return
    pass

async def setup(bot):
    await bot.add_cog(helpCommand(bot))