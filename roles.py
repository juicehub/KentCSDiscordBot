import discord
from discord.ext import commands
import asyncio



class Roles():

    def __init__(self, bot):
        self.bot = bot

    def getRoleObj(rolename, server):
        for role in server.roles:
            if rolename == role.name:
                return role
        else:
            return -1
                
    @commands.command(pass_context=True)
    async def role(self, ctx, *, role: str = None):
            if role is None:
                return await self.bot.delete_message(ctx.message)

            role = role.lower()
            
            if role in ["under", "undergrad", "undergraduate", "undergraduates"]:
                role = "Undergraduates"
            elif role in ["post", "postgrad", "postgraduate", "postgraduates"]:
                role = "Postgraduates"
            elif role in ["alumni", "alumnus"]:
                role = "Alumni"


            r = Roles()
            
            roleObj = Roles().getRoleObj(role, ctx.message.server)
            if roleObj == -1:
                return

            
            
            if roleObj.name == "Postgraduates":
                for srole in ctx.message.server.roles:
                    if srole.name == "Alumni" or srole.name == "Undergraduates":
                        await self.bot.remove_roles(ctx.message.author, srole)
                        
                await self.bot.add_roles(ctx.message.author, roleObj)
            
            if roleObj.name == "Undergraduates":            
                for srole in ctx.message.server.roles:
                    if srole.name == "Alumni" or srole.name == "Postgraduates":
                        await self.bot.remove_roles(ctx.message.author, srole)
                        
                await self.bot.add_roles(ctx.message.author, roleObj)
            
            if roleObj.name == "Alumni":                     
                for srole in ctx.message.server.roles:
                    if srole.name == "Postgraduates" or srole.name == "Undergraduates":
                        await self.bot.remove_roles(ctx.message.author, srole)
                
                await self.bot.add_roles(ctx.message.author, roleObj)

            return await self.bot.delete_message(ctx.message)
                
    

def setup(bot):
    bot.add_cog(Roles(bot))
