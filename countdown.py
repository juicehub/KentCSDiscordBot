import discord
from discord.ext import commands
import asyncio

class Countdown():

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def createcountdown(self, ctx):
        message = ctx.message.content
        print(message)
    



def setup(bot):
    bot.add_cog(Countdown(bot))
