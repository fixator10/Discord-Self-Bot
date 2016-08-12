import discord
from discord.ext import commands
import json
import asyncio

# Set's bot's desciption and prefixes in a list
description = "A self bot to do things that are useful"
bot = commands.Bot(command_prefix=['self.'], description=description, self_bot=True)

###################
## Startup Stuff ##
###################

@bot.event
async def on_ready():
    # Outputs login data to console
    print("---------------------------")
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print("---------------------------")

    # Outputs the state of loading the modules to the console
    # So I know they have loaded correctly
    print("Loading Modules")
    print("---------------------------")
    bot.load_extension("modules.misc")
    print("Loaded Misc")
    bot.load_extension("modules.moderation")
    print("Loaded Moderation")
    bot.load_extension("modules.rng")
    print("loaded RNG")
    print("---------------------------")

######################
## Misc and Testing ##
######################

# Ping Pong
# Testing the response of the bot
@bot.command(pass_context=True,hidden=True)
async def ping(ctx):
    """Pong"""
    await bot.say("Pong")
    print("Ping Pong")

# Invite link to the bot server
@bot.command()
async def server():
    """The bot's server, for updates or something"""
    await bot.say("https://discord.gg/Eau7uhf")
    print("Run: Server")

# Bot's source code
@bot.command()
async def source():
    """Source code"""
    await bot.say("https://github.com/DiNitride/GAFBot")
    print("Run: Source")

@bot.command()
async def gaf_server():
    """GAF Server Invite Link"""

##############################
## FANCY TOKEN LOGIN STUFFS ##
##############################

with open("self_token.txt") as token:
    bot.run(token.read(), bot=False)
