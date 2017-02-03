import discord
from discord.ext import commands
import random

class Moderation():
    def __init__(self, bot):
        self.bot = bot

    # Banning and Kicking commands

    # Bans a member
    @commands.command()
    async def ban(self, member: discord.Member = None):
        """Bans a member
        Usage:
        self.ban @recchan
        User must have ban member permissions"""
        # Are they trying to ban nobody? Are they stupid?
        # Why do they have mod powers if they're this much of an idiot?
        if member is None:
            return
        # Is the person being banned me? No we don't allow that
        elif member.id == '95953002774413312':
            await self.bot.say("http://i.imgur.com/BSbBniw.png")
            return
        # Bans the user
        await self.bot.ban(member, delete_message_days=1)
        # Prints to console

    # Kicks a member
    @commands.command()
    async def kick(self, member: discord.Member = None):
        """Kicks a member
        Usage:
        self.kick @recchan
        User must have kick member permissions"""
        # Same as above, are they stupid
        if member is None:
            return
        # Still not allowed to kick me
        elif member.id == '95953002774413312':
            await self.bot.say("http://i.imgur.com/BSbBniw.png")
            return
        # Kicks the user
        await self.bot.kick(member)
        # Prints to console

    # Information commands
    # Server info and member info

    # Gives the user some basic info on a user
    @commands.command(pass_context=True)
    async def info(self, ctx, member : discord.Member = None):
        """Infomation on a user
        Usage:
        self.info @DiNitride
        If no member is specified, it defaults to the sender"""
        if member == None:
            member = ctx.message.author
        em = discord.Embed(title=member.nick, colour=member.colour)
        em.add_field(name="Name", value=member.name)
        em.add_field(name="Joined server", value=member.joined_at.strftime('%d.%m.%Y %H:%M:%S %Z'))
        em.add_field(name="ID", value=member.id)
        em.add_field(name="Has existed since", value=member.created_at.strftime('%d.%m.%Y %H:%M:%S %Z'))
        em.add_field(name="Color", value=member.colour)
        em.add_field(name="Bot?", value=str(member.bot).replace("True","✔").replace("False","❌"))
        em.set_image(url=member.avatar_url)
        em.set_thumbnail(url="https://xenforo.com/community/rgba.php?r=" + str(member.colour.r) + "&g=" + str(member.colour.g) + "&b=" + str(member.colour.b) + "&a=255")
        await self.bot.say(embed=em)

    # Server Info
    @commands.command(pass_context=True)
    async def serverinfo(self, ctx):
        """Shows server information
        Usage:
        self.serverinfo"""
        server = ctx.message.server
        afk = server.afk_timeout / 60
        em = discord.Embed(title="Server info", colour=random.randint(0, 16777215))
        em.add_field(name="Name", value=server.name)
        em.add_field(name="Server ID", value=server.id)
        em.add_field(name="Region", value=server.region)
        em.add_field(name="Existed since", value=server.created_at.strftime('%d.%m.%Y %H:%M:%S %Z'))
        em.add_field(name="Owner", value=server.owner)
        em.add_field(name="AFK Timeout and Channel", value=str(afk)+" min in "+str(server.afk_channel))
        em.add_field(name="Member Count", value=server.member_count)
        em.set_image(url=server.icon_url)
        await self.bot.say(embed=em)

def setup(bot):
    bot.add_cog(Moderation(bot))
