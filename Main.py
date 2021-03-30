import discord
from epicstore_api import *
import urllib.request
from discord.ext import commands
import random
import SecretCode
client = commands.Bot(command_prefix='.')


@client.event
async def on_ready():
    print("ArkNight is ready")


@client.command()
async def game(channel):
    file_name = "game_image"
    file_path = "images/"
    game = grab_free_game()
    grab_image(file_path, file_name)
    await channel.send(game)
    await channel.send(file=discord.File(file_path+file_name+".jpg"))


@client.command()
async def kick(channel, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)


@client.command()
async def hentai(channel):
    code = ""
    for i in range(6):
        code += str(random.randint(0, 9))
    await channel.send(code)


@client.command()
async def ban(channel, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)


@client.command()
async def purge(channel, count=1):
    await channel.channel.purge(limit=count)


def grab_free_game():
    epic_api = EpicGamesStoreAPI()
    free_games = epic_api.get_free_games()
    for _ in free_games["data"]["Catalog"]["searchStore"]["elements"]:
        try:
            game = _["promotions"]["promotionalOffers"]
            print(game)
        except:
            pass
        for i in game:
            if len(game) == 0:
                continue
            else:
                return (_["title"])


def grab_image(file_path, file_name):
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
                path = file_path + file_name + ".jpg"
                urllib.request.urlretrieve(_["keyImages"][1]["url"], path)


client.run(SecretCode.code)
