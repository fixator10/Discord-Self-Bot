import discord
from discord.ext import commands
import json
import asyncio
import inspect
import argparse
import sys
import traceback


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

    # Outputs the state of loading the modules to the console
    # So I know they have loaded correctly
    print("Loading Modules")
    print("---------------------------")
    bot.load_extension("modules.moderation")
    print("Loaded Moderation")
    bot.load_extension("modules.admin")
    print("Loaded Admin")
    bot.load_extension("modules.tags")
    print("Loaded Tags")
    bot.load_extension("modules.animelist")
    print("Loaded Anime")
    bot.load_extension("modules.custom")
    print("Loaded Custom")
    print("---------------------------")

    await bot.change_presence(afk=True, status=discord.Status.invisible)
    
@bot.event
async def on_command_error(error, ctx):
    if isinstance(error, commands.CommandNotFound) or isinstance(error, commands.MissingRequiredArgument) or isinstance(error, commands.BadArgument):
        await bot.send_message(ctx.message.channel, "An error occured: `" + str(error) + "`")
        await bot.delete_message(ctx.message)
    else:
        await bot.send_message(ctx.message.channel, "An error occured: `" + str(error) + "`")
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
    await bot.say("https://github.com/DiNitride/Discord-Self-Bot\nhttps://github.com/fixator10/Discord-Self-Bot")

# Invite link to the bot server
@bot.command()
async def server():
    """The bot's server, for updates or something"""
    await bot.say("https://discord.gg/Eau7uhf")
	
@bot.command(pass_context=True)
async def reload(ctx, module : str = None):
    """Reloads module"""
    if module == None:
        await bot.say("Please, specify a module to reload")
    else:
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

    with open("self_token.txt") as token:
        bot.run(token.read(), bot=False)
