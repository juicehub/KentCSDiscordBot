import discord
from discord.ext import commands
import asyncio

bot = commands.Bot(command_prefix='!')

class Roles():

    def __init__(self, bot):
        self.bot = bot

    def getRoleObj(self, rolename, server):
        for role in server.roles:
            if rolename == role.name:
                return role
        else:
            return -1
                
    @commands.command(pass_context=True)
    async def role(self, ctx, *, rolename: str = None):

        if rolename is None:
            return await self.bot.delete_message(ctx.message)

        rolename = rolename.lower()

        if rolename in ["under", "undergrad", "undergraduate", "undergraduates"]:
            rolename = "Undergraduates"
        elif rolename in ["post", "postgrad", "postgraduate", "postgraduates"]:
            rolename = "Postgraduates"
        elif rolename in ["alumni", "alumnus"]:
            rolename = "Alumni"

        roleObj = None

        for role in ctx.message.server.roles:
            if rolename == role.name:
                roleObj = role
        if roleObj == None:
            return

        if roleObj.name == "Postgraduates":
            for srole in ctx.message.server.roles:
                if srole.name == "Alumni" or srole.name == "Undergraduates":
                    await self.bot.remove_roles(ctx.message.author, srole)  
            await self.bot.add_roles(ctx.message.author, roleObj)
                
        elif roleObj.name == "Undergraduates":            
            for srole in ctx.message.server.roles:
                if srole.name == "Alumni" or srole.name == "Postgraduates":
                    await self.bot.remove_roles(ctx.message.author, srole)
                    
            await self.bot.add_roles(ctx.message.author, roleObj)
            
        elif roleObj.name == "Alumni":                     
            for srole in ctx.message.server.roles:
                if srole.name == "Postgraduates" or srole.name == "Undergraduates":
                    await self.bot.remove_roles(ctx.message.author, srole)
            
            await self.bot.add_roles(ctx.message.author, roleObj)

        return await self.bot.send_message(ctx.message.channel, "Role `{}` added to {}.".format(rolename, ctx.message.author.mention))            
    

def setup(bot):
    bot.add_cog(Roles(bot))
