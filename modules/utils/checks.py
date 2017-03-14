import discord


def embeds_allowed(message: discord.Message):
    return message.channel.permissions_for(message.author).embed_links
