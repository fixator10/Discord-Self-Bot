# -*- coding: utf-8 -*-
import colorsys
import datetime
import itertools
import random
import re
import time

import aiohttp
import discord
from discord.ext import commands
from yandex_translate import YandexTranslate

from modules.utils.helpers import Checks
import modules.utils.color_converter as cc
import modules.utils.chat_formatting as chat
from modules.utils.dataIO import dataIO

config = dataIO.load_json("data/SelfBot/config.json")

translate = YandexTranslate(config["yandex_translate_API_key"])


class General:
    def __init__(self, bot: discord.Client):
        self.bot = bot
        self.session = aiohttp.ClientSession(loop=self.bot.loop)

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
    async def translate(self, ctx, language: str, *, text: str):
        """Translate text

        Language may be just "ru" (target language to translate)
        or "en-ru" (original text's language - target language)"""
        text = text.strip("`")  # To avoid code blocks formatting failures
        try:
            response = translate.translate(text, language)
        except Exception as e:
            if str(e) == "ERR_LANG_NOT_SUPPORTED":
                await self.bot.say("An error has been occurred: Language `" + language + "` is not supported")
            elif str(e) == "ERR_TEXT_TOO_LONG":
                # Discord will return BAD REQUEST (400) sooner than this happen, but whatever...
                await self.bot.say("An error has been occurred: Text that you provided is too big to translate")
            elif str(e) == "ERR_KEY_INVALID":
                await self.bot.say("<https://translate.yandex.ru/apikeys>\n"
                                   "Setup your API key in `data/SelfBot/config.json`\n"
                                   "And reload module with `self.reload custom`")
            elif str(e) == "ERR_UNPROCESSABLE_TEXT":
                await self.bot.say(
                    "An error has been occurred: Provided text \n```\n" + text + "``` is unprocessable by "
                                                                                 "translation server")
            elif str(e) == "ERR_SERVICE_NOT_AVAIBLE":
                await self.bot.say("An error has been occurred: Service Unavailable. Try again later")
            else:
                await self.bot.say("An error has been occurred: " + str(e))
            return
        if response["code"] == 200:
            await self.bot.say("**Input:** ```\n" + text + "``` ")
            await self.bot.say("**Translation:** ```\n" + response["text"][0] + "```")
        else:
            # According to yandex.translate source code this cannot happen too, but whatever...
            await self.bot.say(
                "An error has been occurred. Translation server returned code `" + response["code"] + "`")

    @commands.command(pass_context=True, aliases=["ецихо"])
    async def eciho(self, ctx, *, text: str):
        """Translate text (cyrillic/latin) to "eciho"
        eciho - language created by Фражуз ZRZ1 СВ#9268 (255682413445906433)

        This is unusable shit, i know, but whatever"""
        char = "сзчшщжуюваёяэкгфйыъьд"
        tran = "ццццццооооееехххииииб"
        table = str.maketrans(char, tran)
        text = text.translate(table)
        char = char.upper()
        tran = tran.upper()
        table = str.maketrans(char, tran)
        text = text.translate(table)
        text = ''.join(c for c, _ in itertools.groupby(text))
        char = "uavwjyqkhfxdzs"
        tran = "ooooiigggggbcc"
        table = str.maketrans(char, tran)
        text = text.translate(table)
        char = char.upper()
        tran = tran.upper()
        table = str.maketrans(char, tran)
        text = text.translate(table)
        await self.bot.say(text)

    @commands.group()
    async def leet(self):
        """Leet (1337) translation commands"""

    @leet.command(pass_context=True, name="leet", aliases=["1337"])
    async def _leet(self, ctx, *, text: str):
        """Translates provided text to 1337"""
        text = text.upper()
        dic = {
            "A": random.choice(["/-|", "4"]),
            "B": "8",
            "C": random.choice(["(", "["]),
            "D": "|)",
            "E": "3",
            "F": random.choice(["|=", "ph"]),
            "G": "6",
            "H": "|-|",
            "I": random.choice(["|", "!", "1"]),
            "J": ")",
            "K": random.choice(["|<", "|("]),
            "L": random.choice(["|_", "1"]),
            "M": random.choice(["|\\/|", "/\\/\\"]),
            "N": random.choice(["|\\|", "/\\/"]),
            "O": random.choice(["0", "()"]),
            "P": "|>",
            "Q": random.choice(["9", "0"]),
            "R": random.choice(["|?", "|2"]),
            "S": random.choice(["5", "$"]),
            "T": random.choice(["7", "+"]),
            "U": "|_|",
            "V": "\\/",
            "W": random.choice(["\\/\\/", "\\X/"]),
            "X": random.choice(["*", "><"]),
            "Y": "'/",
            "Z": "2"
        }
        pattern = re.compile('|'.join(dic.keys()))
        result = pattern.sub(lambda x: dic[x.group()], text)
        await self.bot.say(chat.box(result))

    @leet.command(pass_context=True, aliases=["russian", "cyrillic"])
    async def cs(self, ctx, *, text: str):
        """Translate cyrillic to 1337"""
        text = text.upper()
        dic_cs = {
            "А": "A",
            "Б": "6",
            "В": "B",
            "Г": "r",
            "Д": random.choice(["D", "g"]),
            "Е": "E",
            "Ё": "E",
            "Ж": random.choice(["}|{", ">|<"]),
            "З": "3",
            "И": random.choice(["u", "N"]),
            "Й": "u*",
            "К": "K",
            "Л": random.choice(["JI", "/I"]),
            "М": "M",
            "Н": "H",
            "О": "O",
            "П": random.choice(["II", "n", "/7"]),
            "Р": "P",
            "С": "C",
            "Т": random.choice(["T", "m"]),
            "У": random.choice(["Y", "y"]),
            "Ф": random.choice(["cp", "(|)", "qp"]),
            "Х": "X",
            "Ц": random.choice(["U", "LL", "L|"]),
            "Ч": "4",
            "Ш": random.choice(["W", "LLI"]),
            "Щ": random.choice(["W", "LLL"]),
            "Ъ": random.choice(["~b", "`b"]),
            "Ы": "bl",
            "Ь": "b",
            "Э": "-)",
            "Ю": random.choice(["IO", "10"]),
            "Я": random.choice(["9", "9I"]),
            "%": "o\\o"
        }
        pattern = re.compile('|'.join(dic_cs.keys()))
        result = pattern.sub(lambda x: dic_cs[x.group()], text)
        await self.bot.say(chat.box(result))

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

    # noinspection PyPep8
    @commands.command(pass_context=True)
    async def emojify(self, ctx, *, message: str):
        """emojify text"""
        char = "abcdefghijklmnopqrstuvwxyz↓↑←→—.!"
        tran = "🇦🇧🇨🇩🇪🇫🇬🇭🇮🇯🇰🇱🇲🇳🇴🇵🇶🇷🇸🇹🇺🇻🇼🇽🇾🇿⬇⬆⬅➡➖⏺ℹ"
        table = str.maketrans(char, tran)
        name = message.translate(table)
        char = char.upper()
        table = str.maketrans(char, tran)
        name = name.translate(table)
        await self.bot.say(
            name.replace(" ", "　　")
                .replace("", "​")
                .replace("0", ":zero:")
                .replace("1", ":one:")
                .replace("2", ":two:")
                .replace("3", ":three:")
                .replace("4", ":four:")
                .replace("5", ":five:")
                .replace("6", ":six:")
                .replace("7", ":seven:")
                .replace("8", ":eight:")
                .replace("9", ":nine:")
                .replace("#", "#⃣")
                .replace("*", "*⃣"))

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
