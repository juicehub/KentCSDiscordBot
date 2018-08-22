import discord
from discord.ext import commands
import json
from pprint import pprint
import requests

username = "TDATHDiscord"
password = "TDATHDiscord123"


bot = commands.Bot("?")

memes = {"61520" : {
             "key-words" : ["Fry", "fry", "futurama", "orange hair", "not", "sure", "if", "not sure if", "not sure"]},
         "438680" : {
             "key-words" : ["Batman Slapping Robin", "batman", "robin", "slapping", "slap"]},
         "61579" : {
             "key-words" : ["One Does Not", "one", "does", "not", "simply", "one does not simply", "one does not", "one does"]},
         "61527" : {
             "key-words" : ["Y U NO", "y", "u", "no", "y u", "y u no"]},
         "61539" : {
             "key-words" : ["First World Problems", "fwp","first","world","problems","first world","problems"]},
         "146381" : {
             "key-words" : ["Angry Baby", "angry","baby","angry baby"]},
         "718432" : {
             "key-words" : ["Back in my day", "back", "in", "my", "day", "old man", "old", "back in my day", "in my day"]},
         "8072285" : {
             "key-words" : ["Doge", "doge", "dog", "shiba", "inu", "shiba inu", "dogo", "doggo"]},
	 "101287" : {
             "key-words" : ["Dancing African", "third","world","success","kid","success kid","third world","dancing","african","dancing african","happy"]},
	 "68690826" : {
             "key-words" : ["Caveman Spongebob", "spongebob", "sponge","bob","caveman","caveman spongebob"]}
         }

class Meme():
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(pass_context=True)
    async def meme(self, ctx, *, message=None):
        
        if message == None or message == "help" or message == "?":
            await self.bot.say("Enter in the format **?meme ID/text1/text2**. \nMeme ID list: https://api.imgflip.com/popular_meme_ids")
            return
        
        split = message.split("/", 3)
        ID = split[0].lower()
        mention = ctx.message.author.mention
        

        for k in memes.keys():
            if ID == k:
                pass
            elif ID in memes[k]["key-words"]:
                ID = k        

        payload = {"template_id" : ID,
                   "username" : username,
                   "password" : password,
                   "text0" : split[1],
                   "text1" : split[2]}
        r = requests.post("https://api.imgflip.com/caption_image", data=payload)
        data = json.loads(r.text)
        await self.bot.say("{0} created {1}".format(mention, data["data"]["page_url"]))
        await self.bot.delete_message(ctx.message)

    @commands.command()
    async def memelist(self):
        string = "```py\nFull list: https://api.imgflip.com/popular_meme_ids\n\n"
        for k in memes.keys():
            print(memes[k])
            string = string + k + " - " + str(memes[k]["key-words"][0]) + "\n"

        string = string + "```"

        await self.bot.say(string)


        

def setup(bot):
    bot.add_cog(Meme(bot))
