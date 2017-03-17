try:
    from pynames.generators.elven import DnDNamesGenerator, WarhammerNamesGenerator
    from pynames.generators.goblin import GoblinGenerator
    from pynames.generators.korean import KoreanNamesGenerator
    from pynames.generators.mongolian import MongolianNamesGenerator
    from pynames.generators.orc import OrcNamesGenerator
    from pynames.generators.russian import PaganNamesGenerator
    from pynames.generators.scandinavian import ScandinavianNamesGenerator
    from pynames import GENDER
    import modules.utils.chat_formatting as chat

    ImportFail = False
except:
    ImportFail = True
    pass

from discord.ext import commands


class NameGenerator:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, name="name")
    async def _genname(self, ctx, generator: str = "WarHammer", gender: str = "Male"):
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

        Available genders:
        Male, Female
        """
        generator = generator.lower()
        gender = gender.lower()

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
            return

        if gender == "male":
            gen_gen = GENDER.MALE
        elif gender == "female":
            gen_gen = GENDER.FEMALE
        else:
            await self.bot.say("Incorrect gender provided. List of available genders:\n```\nMale\nFemale```")
            return

        name = name_gen.get_name(genders=gen_gen)
        mess_text = ""
        for lang in name.translations[gen_gen]:
            if isinstance(name.translations[gen_gen][lang], list):
                names = []
                for name_form in name.translations[gen_gen][lang]:
                    names.append(name_form)
                mess_text = mess_text + "\n" + str(lang).upper() + " (all forms):" \
                                                                   " " + chat.box("\n".join([str(x) for x in names]))
            else:
                mess_text = mess_text + "\n" + str(lang).upper() + ": " + chat.box(name.translations[gen_gen][lang])
        await self.bot.say(mess_text)


def setup(bot):
    if ImportFail:
        RuntimeError("Failed to import \"PyNames\" lib.\nInstall it by executing \"pip install pynames\" in command "
                     "line / terminal, or disable this module in \"config.json\"")
    else:
        bot.add_cog(NameGenerator(bot))
