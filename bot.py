import discord
from discord.ext import commands
import asyncio
import time
import datetime
import json
from pprint import pprint

startup_extensions = ["roles", "spongemock", "meme"]

bot = commands.Bot(command_prefix='!')
token = open("../token.txt", "r")

@bot.event
async def on_ready():
    print("----------")
    print("Logged in as: {}.".format(bot.user.name))
    print("Invite link: https://discordapp.com/oauth2/authorize?&client_id={}&scope=bot&permissions=0".format(bot.user.id))
    print("----------")

    for m in startup_extensions:
        bot.load_extension(m)
        print("Loaded {0}.py".format(m))

@bot.event
async def on_member_join(member):
    for channel in member.server.channels:
        if channel.name == "general":
            return await bot.send_message(channel, "Welcome {} to the server. Type `!role undergraduate`, `!role postgraduate`, `!role alumni` to receive your role.".format(member.mention))
    

if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

    bot.run(token.read())
