from pynames.generators.elven import DnDNamesGenerator, WarhammerNamesGenerator
from pynames.generators.goblin import GoblinGenerator
from pynames.generators.korean import KoreanNamesGenerator
from pynames.generators.mongolian import MongolianNamesGenerator
from pynames.generators.orc import OrcNamesGenerator
from pynames.generators.russian import PaganNamesGenerator
from pynames.generators.scandinavian import ScandinavianNamesGenerator
from pynames import GENDER, LANGUAGE
import modules.utils.chat_formatting as chat

from discord.ext import commands


class NameGenerator:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, name="name")
    async def _genname(self, ctx, generator: str = "WarHammer", gender: str = "Male", language: str = "RU"):
        """Generate random name

        Available generators:
        DnD
        WarHammer
        Goblin
        Korean
        Mongolian
        Orc
        Russian
        Scandinavian

        Available languages:
        RU, EN

        Available genders:
        Male, Female
        """
        generator = generator.lower()
        gender = gender.lower()
        language = language.lower()

        if generator == "dnd":
            name_gen = DnDNamesGenerator()
        elif generator == "warhammer":
            name_gen = WarhammerNamesGenerator()
        elif generator == "goblin":
            name_gen = GoblinGenerator()
        elif generator == "korean":
            name_gen = KoreanNamesGenerator()
        elif generator == "mongolian":
            name_gen = MongolianNamesGenerator()
        elif generator == "orc":
            name_gen = OrcNamesGenerator()
        elif generator == "russian":
            name_gen = PaganNamesGenerator()
        elif generator == "scandinavian":
            name_gen = ScandinavianNamesGenerator()
        else:
            await self.bot.say("Incorrect generator provided. List of available "
                               "generators:\n```\nDnD\nWarhammer\nGoblin\nKorean\nMongolian\nOrc\nRussian"
                               "\nScandinavian```")
            await self.bot.delete_message(ctx.message)
            return

        if gender == "male":
            gen_gen = GENDER.MALE
        elif gender == "female":
            gen_gen = GENDER.FEMALE
        else:
            await self.bot.say("Incorrect gender provided. List of available genders:\n```\nMale\nFemale```")
            await self.bot.delete_message(ctx.message)
            return

        if language == "ru":
            lang_gen = LANGUAGE.RU
        elif language == "en":
            lang_gen = LANGUAGE.EN
        else:
            await self.bot.say("Incorrect language provided. List of available languages:\n```\nEN\nRU```")
            await self.bot.delete_message(ctx.message)
            return

        warning = ""
        try:
            name = name_gen.get_name_simple(gen_gen, lang_gen)
        except KeyError:
            warning = chat.warning("Sorry, but looks like this generator doesn't support this provided language ({})\n"
                                   "Name generated with only possible default language\n".format(language))
            name = name_gen.get_name_simple(gen_gen)
        await self.bot.say(warning + "Your generated name: "+chat.inline(name))
        await self.bot.delete_message(ctx.message)


def setup(bot):
    bot.add_cog(NameGenerator(bot))
