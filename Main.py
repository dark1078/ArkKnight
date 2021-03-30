from sqlite3.dbapi2 import Cursor
import discord
from discord.flags import Intents
from epicstore_api import *
import urllib.request
from discord.ext import commands
import random
import SecretCode
import sqlite3
import datetime

intents = discord.Intents().all()
client = commands.Bot(command_prefix='.', intents=intents)


class Data:
    def __init__(self):
        self.welcome_channel = None
        self.goodbye_channel = None


data = Data()


@client.event
async def on_ready():
    # db = sqlite3.connect('main.sqlite')
    # cursor = db.cursor()
    # cursor.execute('''
    # CREATE TABLE IF NOT EXISTS main(
    #     guild_id TEXT,
    #     msg TEXT,
    #     channel_id TEXT
    #     )
    # ''')
    print("ArkNight is ready")
    return await client.change_presence(activity=discord.Activity(type=1, name='ArkNight', url='https://www.twitch.tv/zoramx'))


@client.event
async def on_member_join(member):
    if data.welcome_channel != None:
        embed = discord.Embed(
            colour=0x56ff39, title=f"Welcome to the Quaz's server! There are now {len(list(member.guild.members))} members.")
        embed.set_thumbnail(url=f"{member.avatar_url}")
        embed.set_author(name=f"{member.name}",
                         icon_url=f"{member.avatar_url}")
        embed.set_footer(text=f"{member.guild}",
                         icon_url=f"{member.guild.icon_url}")
        embed.timestamp = datetime.datetime.utcnow()
        await data.welcome_channel(embed=embed)
    else:
        print("Welcome channel not set")


@client.event
async def on_member_remove(member):
    if data.welcome_channel != None:
        embed = discord.Embed(
            colour=0xff0303, title=f"{member.name} has left the Quaz's server, there are now {len(list(member.guild.members))} members.")
        embed.set_thumbnail(url=f"{member.avatar_url}")
        embed.set_author(name=f"{member.name}",
                         icon_url=f"{member.avatar_url}")
        embed.set_footer(text=f"{member.guild}",
                         icon_url=f"{member.guild.icon_url}")
        embed.timestamp = datetime.datetime.utcnow()
        await data.welcome_channel.send(embed=embed)
    else:
        print("Goodbye channel not set")


@client.command()
async def game(channel):
    file_name = "game_image"
    file_path = "images/"
    game = grab_free_game()
    image = grab_image()
    embed = discord.Embed(
        colour=0x56ff39, title=f"Current free game: {game}")
    embed.set_image(url=(image))
    await channel.send(embed=embed)


@ client.command()
@ commands.has_permissions(administrator=True)
async def set_welcome_channel(ctx, channel_name=None):
    if channel_name != None:
        for channel in ctx.guild.channels:
            if channel.name == channel_name:
                data.welcome_channel = channel
                await ctx.channel.send(f"Welcome channel set to {channel.name}")
    else:
        await ctx.channel.send("Please include the name of the channel")


@ client.command()
@ commands.has_permissions(administrator=True)
async def set_goodbye_channel(ctx, channel_name=None):
    if channel_name != None:
        for channel in ctx.guild.channels:
            if channel.name == channel_name:
                data.goodbye_channel = channel
                await ctx.channel.send(f"Goodbye channel set to {channel.name}")
    else:
        await ctx.channel.send("Please include the name of the channel")


@ client.command()
@ commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="No reason provided"):
    await member.kick(reason=reason)
    await ctx.send(f"{member} has been kicked.")


@ client.command()
async def hentai(channel):
    code = ""
    for i in range(6):
        code += str(random.randint(0, 9))
    await channel.send(code)


@ client.command()
@ commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="No reason provided"):
    await member.ban(reason=reason)
    await ctx.send(f"{member} has been banned.")


@ client.command()
@ commands.has_permissions(manage_messages=True)
async def purge(ctx, count=1):
    await ctx.channel.purge(limit=count)


def grab_free_game():
    epic_api = EpicGamesStoreAPI()
    free_games = epic_api.get_free_games()
    for _ in free_games["data"]["Catalog"]["searchStore"]["elements"]:
        try:
            game = _["promotions"]["promotionalOffers"]
        except:
            pass
        for i in game:
            if len(game) == 0:
                continue
            else:
                return (_["title"])


def grab_image():
    epic_api = EpicGamesStoreAPI()
    free_games = epic_api.get_free_games()
    for _ in free_games["data"]["Catalog"]["searchStore"]["elements"]:
        try:
            game = _["promotions"]["promotionalOffers"]
        except:
            continue
        for i in game:
            if len(game) == 0:
                continue
            else:
                return _["keyImages"][1]["url"]


client.run(SecretCode.code)
