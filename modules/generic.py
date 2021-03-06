﻿# -*- coding: utf-8 -*-
import colorsys
import datetime
import random
import re
import time

import discord
from discord.ext import commands

from modules.utils.helpers import Checks
import modules.utils.color_converter as cc
from modules.utils.dataIO import dataIO


config = dataIO.load_json("data/SelfBot/config.json")


class General:
    def __init__(self, bot: discord.Client):
        self.bot = bot

    # @commands.command(pass_context=True, aliases=["game"])
    # async def status(self, ctx, status: str, url: str = None):
    #     """Updates the user's status"""
    #     game = discord.Game()
    #     game.name = status
    #     if url is not None:
    #         game.url = url
    #         game.type = 1
    #     await self.bot.change_presence(game=discord.Game(name=status))
    #     await self.bot.say("Status updated to {}".format(status))

    @commands.command(pass_context=True)
    async def signed(self, ctx, *, message: str = None):
        """Says something with embedded signature

        Text changeable in config.json"""
        if not Checks.embeds_allowed(ctx.message):
            await self.bot.say("Not allowed to send embeds here. Lack `Embed Links` permission")
            return
        em = discord.Embed(title=config["signature_title"], description=config["signature_desc"],
                           url=config["signature_url"], colour=config["signature_colour"],
                           timestamp=ctx.message.timestamp)
        em.add_field(name=config["signature_field_name"], value=config["signature_field_content"], inline=False)
        em.set_footer(text=ctx.message.author.nick or ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
        await self.bot.say(message, embed=em)

    @commands.command(pass_context=True)
    async def embed(self, ctx, *, message: str):
        """Says something via embed
        Useful for using emojis on any server without Nitro
        
        Inline code markdown at start and at end of message will be removed"""
        if not Checks.embeds_allowed(ctx.message):
            await self.bot.say("Not allowed to send embeds here. Lack `Embed Links` permission")
            return
        message = re.sub(r'^\s*(`\s*)?|(\s*`)?\s*$', '', message)
        if ctx.message.server:
            em_color = ctx.message.author.colour
        else:
            em_color = discord.Colour.default()
        em = discord.Embed(description=message, colour=em_color)
        await self.bot.say(embed=em)

    @commands.command(pass_context=True)
    async def quote(self, ctx, messageid: str, *, response: str = None):
        """Quote an message by id"""
        message = discord.utils.get(self.bot.messages, id=messageid)
        if message is None:
            await self.bot.say("Failed to get message with id `" + messageid + "`")
        else:
            if message.channel.is_private:
                colour = discord.Colour.default()
                name = message.author.name
            else:
                colour = message.author.colour
                name = message.author.nick or message.author.name
            em = discord.Embed(description=message.content, colour=colour, timestamp=message.timestamp)
            em.set_author(name=name, icon_url=message.author.avatar_url)
            em.set_footer(text=message.author.name + "#" + message.author.discriminator)
            attachment = discord.utils.get(message.attachments)
            if attachment is not None:
                attachment = dict(attachment)
                em.set_image(url=attachment['url'])
            if Checks.embeds_allowed(ctx.message):
                await self.bot.say(response, embed=em)
            else:
                await self.bot.say((response or "") + "\n\n**Quote from " + message.author.name + "#" +
                                   message.author.discriminator + ":**\n```\n" + message.content + "```")

    @commands.command(pass_context=True, no_pm=True, aliases=['emojiinfo', 'emojinfo'])
    async def emoji(self, ctx, *, emoji: discord.Emoji):
        """Get info about emoji
        
        Works only with nonstandard emojis (non-unicode)"""
        allowed_roles = []
        for elem in emoji.roles:
            allowed_roles.append(elem.name)
        em = discord.Embed(title=emoji.name, colour=random.randint(0, 16777215))
        em.add_field(name="ID", value=emoji.id)
        em.add_field(name="Has existed since", value=emoji.created_at.strftime('%d.%m.%Y %H:%M:%S %Z'))
        em.add_field(name="\":\" required", value=str(emoji.require_colons).replace("True", "✔").replace("False", "❌"))
        em.add_field(name="Managed", value=str(emoji.managed).replace("True", "✔").replace("False", "❌"))
        em.add_field(name="Server", value=emoji.server)
        if len(allowed_roles) > 0:
            em.add_field(name="Roles", value="\n".join([str(x) for x in allowed_roles]))
        em.set_image(url=emoji.url)
        if Checks.embeds_allowed(ctx.message):
            await self.bot.say(embed=em)
        else:
            await self.bot.say("```\n" +
                               "ID: " + emoji.id +
                               "\nHas existed since: " + emoji.created_at.strftime('%d.%m.%Y %H:%M:%S %Z') +
                               "\n\":\" required: " + str(emoji.require_colons)
                               .replace("True", "✔").replace("False", "❌") +
                               "\nManaged: " + str(emoji.managed).replace("True", "✔").replace("False", "❌") +
                               "\nServer: " + str(emoji.server) +
                               "\nRoles: " + "\n".join([str(x) for x in allowed_roles]) +
                               "```" +
                               emoji.url)

    # noinspection PyUnboundLocalVariable
    @commands.command(pass_context=True)
    async def hug(self, ctx, user: discord.Member, intensity: int = 1):
        """Because everyone likes hugs

        Up to 10 intensity levels."""
        name = " *" + user.name + "*"
        if intensity <= 0:
            msg = "(っ˘̩╭╮˘̩)っ" + name
        elif intensity <= 3:
            msg = "(っ´▽｀)っ" + name
        elif intensity <= 6:
            msg = "╰(*´︶`*)╯" + name
        elif intensity <= 9:
            msg = "(つ≧▽≦)つ" + name
        elif intensity >= 10:
            msg = "(づ￣ ³￣)づ" + name + " ⊂(´・ω・｀⊂)"
        await self.bot.say(msg)

    @commands.command(pass_context=True)
    async def flip(self, ctx, user: discord.Member = None):
        """Flips a coin... or a user.

        Defaults to coin.
        """
        if user is not None:
            msg = ""
            char = "abcdefghijklmnopqrstuvwxyz"
            tran = "ɐqɔpǝɟƃɥᴉɾʞlɯuodbɹsʇnʌʍxʎz"
            table = str.maketrans(char, tran)
            name = user.display_name.translate(table)
            char = char.upper()
            tran = "∀qƆpƎℲפHIſʞ˥WNOԀQᴚS┴∩ΛMX⅄Z"
            table = str.maketrans(char, tran)
            name = name.translate(table)
            await self.bot.say(msg + "(╯°□°）╯︵ " + name[::-1])
        else:
            await self.bot.say("*flips a coin and... " + random.choice(["HEADS!*", "TAILS!*"]))

    @commands.command(pass_context=True, name='thetime')
    async def _thetime(self, ctx):
        """Send your current time"""
        await self.bot.say(datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S %Z'))

    @commands.command(pass_context=True, aliases=["pingtime", "ping"])
    async def pingt(self, ctx):
        """pseudo-ping time"""
        channel = ctx.message.channel
        t1 = time.perf_counter()
        await self.bot.send_typing(channel)
        t2 = time.perf_counter()
        await self.bot.say("pseudo-ping: `{}ms`".format(round((t2 - t1) * 1000)))

    @commands.command(pass_context=True, aliases=['HEX', 'hex'])
    async def color(self, ctx, color: str):
        """Shows some info about provided HEX color"""
        pattern = re.compile("^#([A-Fa-f0-9]{6})$")
        if pattern.match(color):
            colorrgb = cc.hex_to_rgb(color)
            colorint = cc.get_int_from_rgb(colorrgb)
            colorhsv = colorsys.rgb_to_hsv(colorrgb[0], colorrgb[1], colorrgb[2])
            colorhls = colorsys.rgb_to_hls(colorrgb[0], colorrgb[1], colorrgb[2])
            coloryiq = colorsys.rgb_to_yiq(colorrgb[0], colorrgb[1], colorrgb[2])
            colorcmyk = cc.rgb_to_cmyk(colorrgb[0], colorrgb[1], colorrgb[2])
            em = discord.Embed(title=str(color),
                               description="Provided HEX: " + color + "\nRGB: " + str(colorrgb) + "\nCMYK: " + str(
                                   colorcmyk) + "\nHSV: " + str(colorhsv) + "\nHLS: " + str(colorhls) + "\nYIQ: " + str(
                                   coloryiq) + "\nint: " + str(colorint),
                               url='http://www.colorpicker.com/' + str(color.lstrip('#')), colour=colorint,
                               timestamp=ctx.message.timestamp)
            em.set_thumbnail(url="https://xenforo.com/community/rgba.php?r=" + str(colorrgb[0]) + "&g=" + str(
                colorrgb[1]) + "&b=" + str(colorrgb[2]) + "&a=255")
            if Checks.embeds_allowed(ctx.message):
                await self.bot.say(embed=em)
            else:
                await self.bot.say("```\n" +
                                   "Provided HEX: " + color +
                                   "\nRGB: " + str(colorrgb) +
                                   "\nCMYK: " + str(colorcmyk) +
                                   "\nHSV: " + str(colorhsv) +
                                   "\nHLS: " + str(colorhls) +
                                   "\nYIQ: " + str(coloryiq) +
                                   "\nint: " + str(colorint) +
                                   "```")
        else:
            await self.bot.say(
                "Looks like the `{}`, that you provided is not color HEX\nOr it is too small/too big.\nExample of "
                "acceptable color HEX: `#1A2B3C`".format(color))


def setup(bot):
    bot.add_cog(General(bot))
