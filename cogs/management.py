import discord
import asyncio

from discord.ext import commands
from discord.ext.commands.errors import MemberNotFound

class managementCommands(commands.Cog, name="Management"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def test(self, ctx):
        await ctx.send("This is a test!")
        return

    @commands.command()
    async def help2(self, ctx):
        helpC = discord.Embed(title="moderator Bot \nHelp Guide", description="discord bot built for moderation")
        helpC.set_thumbnail(url='https://imgur.com/EeMwdLX')
        helpC.add_field(name="Clear", value="To use this command type g:clear and the number of messages you would like to delete, the default is 5.", inline=False)
        helpC.add_field(name="kick/ban/unban", value="To use this command type g:kick/ban/unban then mention the user you would like to perform this on, NOTE: user must have permissions to use this command.", inline=False)

        await ctx.send(embed=helpC)

    #Checks whether the user has the correct permissions when this command is issued
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount=5):
        await ctx.channel.purge(limit=amount+1)
        msgdel = await ctx.send(f'{amount} messages deleted')
        await asyncio.sleep(2)
        await msgdel.delete()

    #Kick and ban work in a similar way as they both require a member to kick/ban and a reason for this
    #As long as the moderator has the right permissions the member will be banned/kicked
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member : discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f'Member {member} kicked')

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member : discord.Member=None, *, reason=None):
        if not member:
            await ctx.send("You must mention a member to ban!")
        elif not reason:
            await ctx.send("No reason given")
        else:
            await member.ban(reason=reason)
            await ctx.send(f'{member} has been banned!')

    #Unbanning a member is done via typing g:unban and the ID of the banned member
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member=None):
        if not member:
            await ctx.send("You must mention a member to unban!")
        else:
            banned_users = await ctx.guild.bans()
            member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

        (user.name, user.discriminator) == (member_name, member_discriminator)
        await ctx.guild.unban(user)
        await ctx.send(f'{user} have been unbanned sucessfully!')

    #Bans a member for a specific amount of time
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def softban(self, ctx, member : discord.Member, time=None, reason=None):
        #Asyncio uses seconds for its sleep function
        await member.ban(reason=reason)
        await ctx.send(f'{member} has been softbanned')
        if not member:
            await ctx.send("You must mention a member to softban!")
        elif not time:
            await ctx.send("You must mention a time!")
        else:
        #Now timed mute manipulation
            try:
                seconds = int(time[:-1]) #Gets the numbers from the time argument, start to -1
                duration = time[-1] #Gets the timed maniulation, s, m, h, d
                if duration == "s":
                    seconds_new = seconds * 1
                elif duration == "m":
                    seconds_new = seconds * 60
                elif duration == "h":
                    seconds_new = seconds * 3600
                elif duration == "d":
                    seconds_new = seconds * 86400
                else:
                    await ctx.send("Invalid duration input")
                    return
            except Exception as e:
                print(e)
                await ctx.send("Invalid time input")
                return
            print(seconds_new)
            await asyncio.sleep(int(seconds_new))
            print("Time to unban")
            await member.unban()
            await ctx.send(f'{member} softban has finished')


    #Timed mute this format: 1d, 20s, 30m, etc..
    @commands.command(aliases=['tempmute'])
    @commands.has_permissions(manage_messages=True)
    async def mute(self, ctx, member: discord.Member=None, time=None, *, reason=None):
        if not member:
            await ctx.send("You must mention a member to mute!")
        elif not time:
            await ctx.send("You must mention a time!")
        else:
            if not reason:
                reason="No reason given"
            #Now timed mute manipulation
            try:
                seconds = int(time[:-1]) #Gets the numbers from the time argument, start to -1
                duration = time[-1] #Gets the timed maniulation, s, m, h, d
                if duration == "s":
                    seconds = seconds * 1
                elif duration == "m":
                    seconds = seconds * 60
                elif duration == "h":
                    seconds = seconds * 60 * 60
                elif duration == "d":
                    seconds = seconds * 86400
                else:
                    await ctx.send("Invalid duration input")
                    return
            except Exception as e:
                print(e)
                await ctx.send("Invalid time input")
                return
            guild = ctx.guild
            Muted = discord.utils.get(guild.roles, name="Muted")
            if not Muted:
                Muted = await guild.create_role(name="Muted")
                for channel in guild.channels:
                    await channel.set_permissions(Muted, speak=False, send_messages=False, read_message_history=True, read_messages=False)
            await member.add_roles(Muted, reason=reason)
            muted_embed = discord.Embed(title="Muted a user", description=f'{member.mention} Was muted by {ctx.author.mention} for {reason} to {time}')
            sent1 = await ctx.send(embed=muted_embed)
            await asyncio.sleep(int(seconds))
            await member.remove_roles(Muted)
            unmute_embed = discord.Embed(title="Mute over!", description=f'{ctx.author.mention} mute to {member.mention} for {reason} is over after {time}')
            sent2 = await ctx.send(embed=unmute_embed)
            await asyncio.sleep(3)
            await sent1.delete()
            await asyncio.sleep(1)
            await sent2.delete()


async def setup(bot):
    await bot.add_cog(managementCommands(bot))
