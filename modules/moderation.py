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
    @commands.command(pass_context=True, no_pm=True)
    async def info(self, ctx, member : discord.Member = None):
        """Infomation on a user"""
        if member == None:
            member = ctx.message.author
        rolelist = []
        for elem in member.roles:
            rolelist.append(elem.name)
        em = discord.Embed(title=member.nick, colour=member.colour)
        em.add_field(name="Name", value=member.name)
        em.add_field(name="Joined server", value=member.joined_at.strftime('%d.%m.%Y %H:%M:%S %Z'))
        em.add_field(name="ID", value=member.id)
        em.add_field(name="Has existed since", value=member.created_at.strftime('%d.%m.%Y %H:%M:%S %Z'))
        em.add_field(name="Color", value=member.colour)
        em.add_field(name="Bot?", value=str(member.bot).replace("True","✔").replace("False","❌"))
        em.add_field(name="Server perms", value="["+str(member.server_permissions.value)+"](https://discordapi.com/permissions.html#"+str(member.server_permissions.value)+")")
        em.add_field(name="Roles", value="\n".join([str(x) for x in rolelist] ), inline=False)
        em.set_image(url=member.avatar_url)
        em.set_thumbnail(url="https://xenforo.com/community/rgba.php?r=" + str(member.colour.r) + "&g=" + str(member.colour.g) + "&b=" + str(member.colour.b) + "&a=255")
        await self.bot.say(embed=em)

    # Server Info
    @commands.command(pass_context=True, no_pm=True)
    async def serverinfo(self, ctx, server : str = None):
        """Shows server information"""
        if server == None:
            server = ctx.message.server
        else:
            server = discord.utils.get(self.bot.servers, id=server)
        if server == None:
            await self.bot.say("Failed to get server with provided ID")
            await self.bot.delete_message(ctx.message)
            return
        afk = server.afk_timeout / 60
        vip_regs = str("VIP_REGIONS" in server.features).replace("True","✔").replace("False","❌")
        van_url = str("VANITY_URL" in server.features).replace("True","✔").replace("False","❌")
        inv_splash = "INVITE_SPLASH" in server.features
        em = discord.Embed(title="Server info", colour=server.owner.colour)
        em.add_field(name="Name", value=server.name)
        em.add_field(name="Server ID", value=server.id)
        em.add_field(name="Region", value=server.region)
        em.add_field(name="Existed since", value=server.created_at.strftime('%d.%m.%Y %H:%M:%S %Z'))
        em.add_field(name="Owner", value=server.owner)
        em.add_field(name="AFK Timeout and Channel", value=str(afk)+" min in "+str(server.afk_channel))
        em.add_field(name="Verification level", value=str(server.verification_level).replace("none","None").replace("low","Low").replace("medium","Medium").replace("high","(╯°□°）╯︵ ┻━┻"))
        em.add_field(name="2FA admins", value=str(server.mfa_level).replace("0","❌").replace("1","✔"))
        em.add_field(name="Member Count", value=server.member_count)
        em.add_field(name="Role Count", value=len(server.roles))
        em.add_field(name="Channel Count", value=len(server.channels))
        em.add_field(name="VIP Voice Regions", value=vip_regs)
        em.add_field(name="Vanity URL", value=van_url)
        if inv_splash == False:
            em.add_field(name="Invite Splash", value="❌")
        elif server.splash_url == "":
            em.add_field(name="Invite Splash", value="✔")
        else:
            em.add_field(name="Invite Splash", value="✔ [🔗]("+server.splash_url+")")
        em.set_image(url=server.icon_url)
        await self.bot.say(embed=em)
        await self.bot.delete_message(ctx.message)

def setup(bot):
    bot.add_cog(Moderation(bot))
