import itertools
import random
import re
import base64
from urllib import parse

import discord
from discord.ext import commands
from yandex_translate import YandexTranslate

import modules.utils.chat_formatting as chat
from modules.utils.dataIO import dataIO

config = dataIO.load_json("data/SelfBot/config.json")

translate = YandexTranslate(config["yandex_translate_API_key"])


class Translaters:
    def __init__(self, bot: discord.Client):
        self.bot = bot

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
        input_lang = None
        output_lang = None
        if len(language) == 2:
            input_lang = translate.detect(text=text)
            output_lang = language
        elif len(language) == 5:
            input_lang = language[:2]
            output_lang = language[3:]
        if response["code"] == 200:
            await self.bot.say("**[{}] Input:** {}".format(input_lang.upper(), chat.box(text)))
            await self.bot.say("**[{}] Translation:** {}".format(output_lang.upper(), chat.box(response["text"][0])))
        else:
            # According to yandex.translate source code this cannot happen too, but whatever...
            await self.bot.say(
                "An error has been occurred. Translation server returned code `" + response["code"] + "`")

    @commands.command(pass_context=True, aliases=["ецихо"])
    async def eciho(self, ctx, *, text: str):
        """Translates text (cyrillic/latin) to "eciho"
        eciho - language created by Фражуз#9941 (255682413445906433)

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

    @commands.group(pass_context=True)
    async def leet(self, ctx):
        """Leet (1337) translation commands"""
        if ctx.invoked_subcommand is None:
            await self.bot.send_cmd_help(ctx)

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

    @commands.group(pass_context=True, name="base64")
    async def _base64(self, ctx):
        """Base64 text converter"""
        if ctx.invoked_subcommand is None:
            await self.bot.send_cmd_help(ctx)

    @_base64.command(pass_context=True, name="encode")
    async def _tobase64(self, ctx, *, text: str):
        """Encode text to base64"""
        text = text.encode()
        output = base64.standard_b64encode(text)
        result = output.decode()
        for page in chat.pagify(result):
            await self.bot.say(chat.box(page))

    @_base64.command(pass_context=True, name="decode")
    async def _frombase64(self, ctx, *, encoded: str):
        """Encode text to base64"""
        encoded = encoded.encode()
        decoded = base64.standard_b64decode(encoded)
        result = decoded.decode()
        await self.bot.say(chat.box(result))

    @commands.command(pass_context=True, name="urlencode", aliases=["url"])
    async def _urlencode(self, ctx, *, text: str):
        """Encode text to url-like format
        ('abc def') -> 'abc%20def'"""
        encoded_url = parse.quote(text)
        await self.bot.say(chat.box(encoded_url))


def setup(bot):
    bot.add_cog(Translaters(bot))
