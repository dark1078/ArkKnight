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
    embed = discord.Embed(
        colour=0x56ff39, title=f"Welcome to the Quaz's server! There are now {len(list(member.guild.members))} members.")
    embed.set_thumbnail(url=f"{member.avatar_url}")
    embed.set_author(name=f"{member.name}",
                     icon_url=f"{member.avatar_url}")
    embed.set_footer(text=f"{member.guild}",
                     icon_url=f"{member.guild.icon_url}")
    embed.timestamp = datetime.datetime.utcnow()
    channel = client.get_channel(id=818600857075187745)
    await channel.send(embed=embed)


@client.event
async def on_member_remove(member):
    embed = discord.Embed(
        colour=0xff0303, title=f"{member.name} has left the Quaz's server, there are now {len(list(member.guild.members))} members.")
    embed.set_thumbnail(url=f"{member.avatar_url}")
    embed.set_author(name=f"{member.name}",
                     icon_url=f"{member.avatar_url}")
    embed.set_footer(text=f"{member.guild}",
                     icon_url=f"{member.guild.icon_url}")
    embed.timestamp = datetime.datetime.utcnow()
    channel = client.get_channel(id=818600857075187745)
    await channel.send(embed=embed)


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
async def kick(channel, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)


@ client.command()
async def hentai(channel):
    code = ""
    for i in range(6):
        code += str(random.randint(0, 9))
    await channel.send(code)


@ client.command()
async def ban(channel, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)


@ client.command()
async def purge(channel, count=1):
    await channel.channel.purge(limit=count)


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
