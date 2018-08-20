import discord
from discord.ext import commands
import asyncio
import time
import datetime
import json
from pprint import pprint

bot = commands.Bot(command_prefix='!')
token = open("../token.txt", "r")

@bot.command(pass_context=True)
async def role(ctx, *, role: str = None):
        if role is None:
            return await bot.delete_message(ctx.message)

        role = role.lower()
        
        if role == "under" or role == "undergrad" or role == "undergraduate" or role == "undergraduates":
            role = "Undergraduates"
        elif role == "post" or role == "postgrad" or role == "postgraduate" or role == "postgraduates":
            role = "Postgraduates"
        elif role == "alumni" or role == "alumnus":
            role = "Alumni"
            
        roleObj = getRoleObj(role, ctx.message.server)

        if roleObj.name == "Postgraduates":
            for srole in ctx.message.server.roles:
                if srole.name == "Alumni" or srole.name == "Undergraduates":
                    await bot.remove_roles(ctx.message.author, srole)
                    
            await bot.add_roles(ctx.message.author, roleObj)
        
        if roleObj.name == "Undergraduates":            
            for srole in ctx.message.server.roles:
                if srole.name == "Alumni" or srole.name == "Postgraduates":
                    await bot.remove_roles(ctx.message.author, srole)
                    
            await bot.add_roles(ctx.message.author, roleObj)
        
        if roleObj.name == "Alumni":                     
            for srole in ctx.message.server.roles:
                if srole.name == "Postgraduates" or srole.name == "Undergraduates":
                    await bot.remove_roles(ctx.message.author, srole)
            
            await bot.add_roles(ctx.message.author, roleObj)

        return await bot.delete_message(ctx.message)
            
def getRoleObj(rolename, server):
    for role in server.roles:
        if rolename == role.name:
            return role
    else:
        return -1

@bot.event
async def on_ready():
    with open("config.json") as f:
        data = json.load(f) 

    newmessage = data["role requests"]["new message"]
    emojis = data["role requests"]["emojis"]
    
    for s in bot.servers:
        if s.name == "bot testing":
            server = s
    for channel in server.channels:
        if channel.name == data["role requests"]["channel name"]:
            async for message in bot.logs_from(channel):
                await bot.delete_message(message)
            msg = await bot.send_message(channel, newmessage)
            data["role requests"]["messageID"] = msg.id

                        
            for emoji in server.emojis:
                for emoji2 in emojis:
                    if emoji.name == emoji2:
                        await bot.add_reaction(msg, emoji)
                        
    with open('config.json', 'w') as outfile:  
        json.dump(data, outfile)

@bot.event
async def on_reaction_add(reaction, user):

    with open("config.json") as f:
        data = json.load(f)
    
    message = reaction.message
    # check if the msg ID is the one we want
    if message.id == data["role requests"]["messageID"]:
        occupied = True
        # check if bot isn't adding the reactions
        if user.id != "480713727226675214":
            # go through list of emojis, check for match in between
            for i in range(0, len(data["role requests"]["emojis"])):
                if reaction.emoji.name == data["role requests"]["emojis"][i]:
                    # if reaction is in the list of emojis in JSON file, we use i to get the corresponding role name
                    roleObj = getRoleObj(data["role requests"]["roles"][i], reaction.message.server)
                    if roleObj in user.roles:
                        # user already has role so remove
                        print("{} removed from {}".format(roleObj.name, user.name))
                        return await bot.remove_roles(user, roleObj)
                    else:
                        # user doesn't have role so add
                        print("{} added to {}".format(roleObj.name, user.name))
                        return await bot.add_roles(user, roleObj)
                    
@bot.event
async def on_reaction_remove(reaction, user):

    with open("config.json") as f:
        data = json.load(f)
    
    message = reaction.message
    # check if the msg ID is the one we want
    if message.id == data["role requests"]["messageID"]:
        occupied = True
        # check if bot isn't adding the reactions
        if user.id != "480713727226675214":
            # go through list of emojis, check for match in between
            for i in range(0, len(data["role requests"]["emojis"])):
                if reaction.emoji.name == data["role requests"]["emojis"][i]:
                    # if reaction is in the list of emojis in JSON file, we use i to get the corresponding role name
                    roleObj = getRoleObj(data["role requests"]["roles"][i], reaction.message.server)
                    if roleObj in user.roles:
                        # user already has role so remove
                        print("{} removed from {}".format(roleObj.name, user.name))
                        return await bot.remove_roles(user, roleObj)
                    else:
                        # user doesn't have role so add
                        print("{} added to {}".format(roleObj.name, user.name))
                        return await bot.add_roles(user, roleObj)
                        
                  
            


bot.run(token.read())
