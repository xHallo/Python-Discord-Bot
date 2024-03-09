import discord
from discord.channel import VoiceChannel
from discord.ext import commands,tasks
# import youtube_dl
import yt_dlp
import os
import asyncio
import urllib.request
import re
import ffmpeg

def url_fetcher(key):
    if "://" in key:
        return key
    else: 
        key.split("_")
        key = '+'.join(str(x) for x in key)
        html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + key)
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode() ) 
        url = ("https://www.youtube.com/watch?v=" + video_ids[0])
        return url

yt_dlp.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}
ytdl = yt_dlp.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = ""

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            # take first item from a playlist
           data = data['entries'][0]
        filename = data['title'] if stream else ytdl.prepare_filename(data)
        return filename



class musicCommands(commands.Cog, name="Music"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def musictest(self,ctx):
        await ctx.send("hello")
    @commands.command(name='join', help="Allows the commands to join the channel")
    async def join(self,ctx):
        mevoicetrue = ctx.guild.me.voice
        if not ctx.message.author.voice:
            await ctx.send("{}, You are not connected to a channel".format(ctx.message.author.name))
            return
        elif mevoicetrue is not None:
            await ctx.send("I am already in a channel, switching channels now!")
            channel = ctx.message.author.voice.channel
        await channel.connect()

    @commands.command(name="play", help ="Makes the commands play any song in youtube.")
    async def play(self,ctx,url):
        mevoicetrue = ctx.guild.me.voice
        if not ctx.message.author.voice:
            await ctx.send("You are not in a channel!")
        elif mevoicetrue == None:
            await ctx.send("I am not currently in a channel!")
        else:
            server=ctx.message.guild
            voice_channel = server.voice_client

            async with ctx.typing():
                filename = await YTDLSource.from_url(url_fetcher(url),loop=self.bot.loop)
                voice_channel.play(discord.FFmpegPCMAudio(source=filename, executable = "D:\\?\\?\\bin\\ffmpeg")),
            await ctx.send("Song request received, playing now.")
           
    @commands.command(name='pause', help='This command pauses the song')
    async def pause(self,ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_playing():
            await voice_client.pause()
        else:
            await ctx.send("Song paused.")
    
    @commands.command(name='resume', help='Resumes the song')
    async def resume(self,ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_paused():
            await voice_client.resume()
        else:
            await ctx.send("Song resumed.")
    


    @commands.command(name='leave', help='To make the bot leave the voice channel')
    async def leave(self, ctx):
        mevoicetrue = ctx.guild.me.voice
        voice_client = ctx.message.guild.voice_client
        if mevoicetrue == None:
            await ctx.send("You are not in a voice channel")
        elif mevoicetrue is not None:
            await voice_client.disconnect()
        else:
            await ctx.send("Thank you for using me. Good bye!")

    @commands.command(name='stop', help='Stops the song')
    async def stop(self, ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_playing():
            await voice_client.stop()
        else:
            await ctx.send("Song stopped.")


async def setup(bot):
    await bot.add_cog(musicCommands(bot))
