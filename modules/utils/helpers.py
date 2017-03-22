import discord
from modules.utils.dataIO import dataIO

config = dataIO.load_json("data/SelfBot/config.json")


class GenericHelper:
    """Useful helpers"""

    @staticmethod
    def check_param(param: str, default):
        """Check parameter for existence in config, or use default
        Used for version compatibility"""
        try:
            result = config[param]
        except:
            result = default
        return result


class Checks:
    """User's permissions check for provided message"""

    @staticmethod
    def embeds_allowed(message: discord.Message):
        return message.channel.permissions_for(message.author).embed_links
