from pynames import GENDER, LANGUAGE
from pynames.generators.elven import DnDNamesGenerator, WarhammerNamesGenerator
from pynames.generators.goblin import GoblinGenerator
from pynames.generators.korean import KoreanNamesGenerator
from pynames.generators.mongolian import MongolianNamesGenerator
from pynames.generators.orc import OrcNamesGenerator
from pynames.generators.russian import PaganNamesGenerator
from pynames.generators.scandinavian import ScandinavianNamesGenerator

from discord.ext import commands


class NameGenerator:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, name="name")
    async def _genname(self, ctx, generator: str = "Warhammer", gender: str = "Male", language: str = "RU"):
        """Generate random name

        Available generators:
        DnD
        Warhammer
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

        if generator == "DnD":
            name_gen = DnDNamesGenerator()
        elif generator == "Warhammer":
            name_gen = WarhammerNamesGenerator()
        elif generator == "Goblin":
            name_gen = GoblinGenerator()
        elif generator == "Korean":
            name_gen = KoreanNamesGenerator()
        elif generator == "Mongolian":
            name_gen = MongolianNamesGenerator()
        elif generator == "Orc":
            name_gen = OrcNamesGenerator()
        elif generator == "Russian":
            name_gen = PaganNamesGenerator()
        elif generator == "Scandinavian":
            name_gen = ScandinavianNamesGenerator()
        else:
            await self.bot.say("Incorrect generator provided. List of available "
                               "generators:\n```\nDnD\nWarhammer\nGoblin\nKorean\nMongolian\nOrc\nRussian"
                               "\nScandinavian```")
            await self.bot.delete_message(ctx.message)
            return

        if gender == "Male":
            gen_gen = GENDER.MALE
        elif gender == "Female":
            gen_gen = GENDER.FEMALE
        else:
            await self.bot.say("Incorrect gender provided. List of available genders:\n```\nMale\nFemale```")
            await self.bot.delete_message(ctx.message)
            return

        if language == ("RU" or "Russian"):
            lang_gen = LANGUAGE.RU
        elif language == ("EN" or "English"):
            lang_gen = LANGUAGE.EN
        else:
            await self.bot.say("Incorrect language provided. List of available languages:\n```\nEN\nRU```")
            await self.bot.delete_message(ctx.message)
            return

        warning = ""
        try:
            name = name_gen.get_name_simple(gen_gen, lang_gen)
        except KeyError:
            warning = "Sorry, but looks like something went wrong and we can't get name with provided settings (" \
                      "Language or Gender)\nName generated without provided parameters\n"
            name = name_gen.get_name_simple()
        await self.bot.say(warning + "Your generated name: `" + str(name) + "`")
        await self.bot.delete_message(ctx.message)


def setup(bot):
    bot.add_cog(NameGenerator(bot))
