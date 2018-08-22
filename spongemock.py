import discord
from discord.ext import commands
import random


bot = commands.Bot(command_prefix="!")

class Spongemock():
    def __init__(self, bot):
        self.bot = bot

    
    
    @commands.command(pass_context=True)
    async def spongemock(self, ctx, *, message=None):

        if message == None or message == "help" or message == "?":
            await self.bot.say("Enter in the format **?spongemock text**.")
            return
        mention = ctx.message.author.mention
        
        text = randomtext(message)
        await self.bot.send_file(ctx.message.channel, "spongemock.jpg", content=text)


def randomtext(message):
    length = len(message)
    ls = []
    final = ""
    
    for i in range(0, length):
        num = random.randint(0,1)
        if num == 0:
            ls.append(message[i].upper())
        elif num == 1:
            ls.append(message[i].lower())

    for i in range(0, length):
        final = final + ls[i]
    
    return final
 
def setup(bot):
    bot.add_cog(Spongemock(bot))


