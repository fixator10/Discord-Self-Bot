import discord
from modules.utils.dataIO import dataIO

config = dataIO.load_json("data/SelfBot/config.json")


class CommandRemoval:
    """Removes command message"""
    def __init__(self, bot: discord.Client):
        self.bot = bot

    async def on_message(self, message: discord.Message):
        if message.content.startswith(config["prefix"]) and message.author.id == self.bot.user.id:
            await self.bot.delete_message(message)


def setup(bot):
    bot.add_cog(CommandRemoval(bot))
