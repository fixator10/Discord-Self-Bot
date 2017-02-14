# -*- coding: utf-8 -*-
from __future__ import print_function
import discord
from discord.ext import commands
from modules.utils.dataIO import dataIO
import inspect
import os

initial_extensions = [
    'admin',
    'moderation',
    'tags',
    'animelist',
    'custom',
    'penis',
    'eval'
]
version = "F10.0.0.17"

config = dataIO.load_json("data/SelfBot/config.json")

# Set's bot's description and prefixes in a list
description = config["description"]+"\n"+"Version: \""+version+"\""
bot = commands.Bot(command_prefix=[config["prefix"]], description=description, self_bot=True)


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
    if isinstance(error, commands.MissingRequiredArgument) or isinstance(error, commands.BadArgument) or isinstance(
            error, commands.NoPrivateMessage):
        await bot.send_message(ctx.message.channel, str(error))
        await bot.delete_message(ctx.message)
    elif isinstance(error, commands.CommandNotFound):
        pass
    else:
        await bot.send_message(ctx.message.channel, "\u26A0 An error occurred: `" + str(
            error) + "`\nCheck console for further information\n\nIssue tracker: "
                     "<https://github.com/fixator10/Discord-Self-Bot/issues>")
        await bot.delete_message(ctx.message)
        raise error


########################################################################################################################

# Ping Pong
# Testing the response of the bot
@bot.command()
async def ping():
    """Pong. Test's responsiveness of bot"""
    await bot.say("Pong")


@bot.command(name='shutdown', aliases=['off', 'close', 'захлопнись', 'выключить'])
async def _botshutdown():
    """Shuts bot down"""
    await bot.close()


@bot.command()
async def source():
    """Source code"""
    await bot.say(
        "<@95953002774413312>'s original: <https://github.com/DiNitride/Discord-Self-Bot>\n\n<@131813999326134272>'s "
        "fork (this): https://github.com/fixator10/Discord-Self-Bot")


# Invite link to the bot server
@bot.command()
async def server():
    """The bot's server, for updates or something"""
    await bot.say("https://discord.gg/Eau7uhf")


@bot.command(pass_context=True)
async def reload(ctx, module: str):
    """Reloads module"""
    try:
        bot.unload_extension("modules." + module)
        bot.load_extension("modules." + module)
    except Exception as e:
        await bot.say("{}: {}".format(type(e).__name__, e))
    await bot.delete_message(ctx.message)


@bot.command(pass_context=True, name="eval")
async def eval_(ctx, *, code: str):
    """Evaluates a line of code provided"""
    code = code.strip("` ")
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
        if user.nick is None:
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

    if os.path.exists("data/SelfBot/self_token.json"):
        userinfo = dataIO.load_json("data/SelfBot/self_token.json")
        bot.run(userinfo["token"], bot=False)
    if os.path.exists("data/SelfBot/self_password.json"):
        userinfo = dataIO.load_json("data/SelfBot/self_password.json")
        bot.run(userinfo["login"], userinfo["password"], bot=False)
