# -*- coding: utf-8 -*-
from __future__ import print_function
import inspect
import os
import sys

import discord
from discord.ext import commands

import modules.utils.anojibothelp as helpformat
from modules.utils.dataIO import dataIO

initial_extensions = [
    "admin",
    "moderation",
    "tags",
    "animelist",
    "generic",
    "penis",
    "eval",
    "weather",
    "namegen",
]
version = "F10.0.0.28"

config = dataIO.load_json("data/SelfBot/config.json")

try:
    modules = config["modules"]
except KeyError:
    modules = initial_extensions

formatter = helpformat.CustomHelp(show_check_failure=False)

# Set's bot's description and prefixes in a list
description = config["description"] + "\n" + "Version: \"" + version + "\""
bot = commands.Bot(command_prefix=[config["prefix"]], description=description, self_bot=True, formatter=formatter)


########################################################################################################################

@bot.event
async def on_ready():
    # Outputs login data to console
    print("---------------------------")
    print('Logged in as')
    print(bot.user.name+"#"+str(bot.user.discriminator))
    print(bot.user.id)
    print("---------------------------")

    print("Modules Loaded:")
    for extension in modules:
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
# @bot.command()
# async def ping():
#     """Pong. Test's responsiveness of bot"""
#     await bot.say("Pong")


@bot.command(pass_context=True, name='shutdown', aliases=['off', 'close', 'захлопнись', 'выключить'])
async def _botshutdown(ctx):
    """Shuts bot down"""
    await bot.say("SelfBot shutting down...")
    await bot.delete_message(ctx.message)
    await bot.close()


@bot.command(pass_context=True)
async def source(ctx):
    """Source code"""
    await bot.say(
        "<@95953002774413312>'s original: <https://github.com/DiNitride/Discord-Self-Bot>\n\n<@131813999326134272>'s "
        "fork (this): https://github.com/fixator10/Discord-Self-Bot")
    await bot.delete_message(ctx.message)


@bot.command(pass_context=True, aliases=["bug", "issue"])
async def server(ctx):
    """The bot's server, for updates or something"""
    await bot.say("Original bot's server: \nhttps://discord.gg/Eau7uhf\nThis fork's server: https://discord.gg/TrQRkTN")
    await bot.delete_message(ctx.message)


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


########################################################################################################################

if __name__ == "__main__":

    if os.path.exists("data/SelfBot/self_token.json"):
        userinfo = dataIO.load_json("data/SelfBot/self_token.json")
        try:
            bot.run(userinfo["token"], bot=False)
        except discord.LoginFailure as e:
            print("Failed to login with token.\nLaunch login.bat and authorise again or create and fill "
                  "self_token.json manually\n"+str(e))
    elif os.path.exists("data/SelfBot/self_password.json"):
        userinfo = dataIO.load_json("data/SelfBot/self_password.json")
        try:
            bot.run(userinfo["login"], userinfo["password"], bot=False)
        except discord.LoginFailure as e:
            print("Failed to login with login and pass.\nLaunch login.bat and authorise again or create and fill "
                  "self_password.json manually\n"+str(e))
    else:
        print("Credentials not found.\nLaunch login.bat or create and fill up self_token.json or self_password.json "
              "manually")
        exit()  # exit before that connection will throw unclosed warning
