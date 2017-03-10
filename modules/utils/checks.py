import discord


def embeds_allowed(message: discord.Message):
    return message.channel.permissions_for(message.author).embed_links


def ban_allowed(message: discord.Message):
    return message.channel.permissions_for(message.author).ban_members


def kick_allowed(message: discord.Message):
    return message.channel.permissions_for(message.author).kick_members


def can_invite(message):
    return message.channel.permissions_for(message.author).create_instant_invite


def manage_emoji(message):
    return message.channel.permissions_for(message.author).manage_emojis
