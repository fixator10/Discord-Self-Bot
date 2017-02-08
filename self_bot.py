import discord
from discord.ext import commands
from modules.utils.dataIO import fileIO
from modules.utils.dataIO import dataIO
import json
import asyncio
import inspect
import os
import argparse
import sys
import traceback

initial_extensions = [
    'admin',
    'moderation',
    'tags',
    'animelist',
    'custom',
    'penis'
]
    
# Set's bot's desciption and prefixes in a list
description = "FG17: Discord Selfbot"
bot = commands.Bot(command_prefix=["self."], description=description, self_bot=True)

# # load bot config
# with open("config/config.json") as f:
#     bot.config = json.load(f)

########################################################################################################################

@bot.event
async def on_ready():
    # Outputs login data to console
    print("---------------------------")
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print("---------------------------")
    
    print("Modules Loaded:")
    for extension in initial_extensions:
        try:
            bot.load_extension("modules." + extension)
            print("* " + extension)
        except Exception as e:
            print('Failed to load extension {}\n{}: {}'.format(
                extension, type(e).__name__, e))
    print("---------------------------")

    await bot.change_presence(afk=True, status=discord.Status.invisible)
    
@bot.event
async def on_command_error(error, ctx):
    if isinstance(error, commands.MissingRequiredArgument) or isinstance(error, commands.BadArgument):
        await bot.send_message(ctx.message.channel, str(error))
        await bot.delete_message(ctx.message)
    elif isinstance(error, commands.CommandNotFound):
        pass
    else:
        await bot.send_message(ctx.message.channel, "\u26A0 An error occurred: `" + str(error) + "`\nCheck console for further information\n\nIssue tracker: <https://github.com/fixator10/Discord-Self-Bot/issues>")
        await bot.delete_message(ctx.message)
        raise(error)
########################################################################################################################

# Ping Pong
# Testing the response of the bot
@bot.command()
async def ping():
    """Pong. Test's responsiveness of bot"""
    await bot.say("Pong")

@bot.command(pass_context=True, name='shutdown', aliases=['off', 'close', 'захлопнись', 'выключить'])
async def _botshutdown(ctx):
    """Shuts bot down"""
    await bot.close()

@bot.command()
async def source():
    """Source code"""
    await bot.say("<@95953002774413312>'s original: <https://github.com/DiNitride/Discord-Self-Bot>\n\n<@131813999326134272>'s fork (this): https://github.com/fixator10/Discord-Self-Bot")

# Invite link to the bot server
@bot.command()
async def server():
    """The bot's server, for updates or something"""
    await bot.say("https://discord.gg/Eau7uhf")
	
@bot.command(pass_context=True)
async def reload(ctx, module : str):
    """Reloads module"""
    try:
        bot.unload_extension("modules."+module)
        bot.load_extension("modules."+module)
    except Exception as e:
        await bot.say("{}: {}".format(type(e).__name__, e))
    await bot.delete_message(ctx.message)

@bot.command(pass_context=True, name="eval")
async def eval_(ctx, *, code: str):
    """Evaluates a line of code provided"""
    code = code.strip("` ")
    server = ctx.message.server
    message = ctx.message
    try:
        result = eval(code)
        if inspect.isawaitable(result):
            result = await result
    except Exception as e:
        await bot.say("```py\nInput: {}\n{}: {}```".format(code, type(e).__name__, e))
    else:
        await bot.say("```py\nInput: {}\nOutput: {}\n```".format(code, result))
    await bot.delete_message(message)

@bot.command(pass_context=True)
async def massnick(ctx, nickname: str):
    """Mass nicknames everyone on the server"""
    server = ctx.message.server
    counter = 0
    for user in server.members:
        if user.nick == None:
            nickname = "{} {}".format(nickname, user.name)
        else:
            nickname = "{} {}".format(nickname, user.nick)
        try:
            await bot.change_nickname(user, nickname)
        except discord.HTTPException:
            counter += 1
            continue
    await bot.say("Finished nicknaming server. {} nicknames could not be completed.".format(counter))

@bot.command(pass_context=True)
async def resetnicks(ctx):
    server = ctx.message.server
    for user in server.members:
        try:
            await bot.change_nickname(user, nickname=None)
        except discord.HTTPException:
            continue
    await bot.say("Finished resetting server nicknames")

########################################################################################################################

if __name__ == "__main__":

    if os.path.exists("self_token.txt"):
        userinfo = dataIO.load_json("self_token.txt")
        bot.run(userinfo["token"], bot=False)
    if os.path.exists("self_password.txt"):
        userinfo = dataIO.load_json("self_password.txt")
        bot.run(userinfo["login"], userinfo["password"], bot=False)
