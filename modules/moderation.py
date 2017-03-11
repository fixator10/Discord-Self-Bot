import random

import discord
from discord.ext import commands
import modules.utils.color_converter as cc
import modules.utils.checks as check


class Moderation:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, no_pm=True, aliases=['memberinfo', 'meminfo', 'membinfo',
                                                              'member', 'userinfo', 'user'])
    async def info(self, ctx, member: discord.Member = None):
        """Information on a user"""
        if member is None:
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
        em.add_field(name="Bot?", value=str(member.bot).replace("True", "✔").replace("False", "❌"))
        em.add_field(name="Server perms", value="[" + str(
            member.server_permissions.value) + "](https://discordapi.com/permissions.html#" + str(
            member.server_permissions.value) + ")")
        em.add_field(name="Roles", value="\n".join([str(x) for x in rolelist]), inline=False)
        em.set_image(url=member.avatar_url)
        em.set_thumbnail(url="https://xenforo.com/community/rgba.php?r=" + str(member.colour.r) + "&g=" + str(
            member.colour.g) + "&b=" + str(member.colour.b) + "&a=255")
        if check.embeds_allowed(ctx.message):
            await self.bot.say(embed=em)
        else:
            await self.bot.say("```\n" +
                               "Name: "+member.name +
                               "\nJoined server: "+member.joined_at.strftime('%d.%m.%Y %H:%M:%S %Z') +
                               "\nID: "+member.id +
                               "\nHas existed since: "+member.created_at.strftime('%d.%m.%Y %H:%M:%S %Z') +
                               "\nColor: "+str(member.color) +
                               "\nBot?: "+str(member.bot).replace("True", "✔").replace("False", "❌") +
                               "\nServer perms: "+str(member.server_permissions.value) +
                               "\nRoles: "+"\n".join([str(x) for x in rolelist]) +
                               "```\n" +
                               member.avatar_url)
        await self.bot.delete_message(ctx.message)

    @commands.command(pass_context=True, no_pm=True, aliases=['servinfo', 'serv', 'sv'])
    async def serverinfo(self, ctx, server: str = None):
        """Shows server information"""
        if server is None:
            server = ctx.message.server
        else:
            server = self.bot.get_server(server)
        if server is None:
            await self.bot.say("Failed to get server with provided ID")
            await self.bot.delete_message(ctx.message)
            return
        afk = server.afk_timeout / 60
        vip_regs = str("VIP_REGIONS" in server.features).replace("True", "✔").replace("False", "❌")
        van_url = str("VANITY_URL" in server.features).replace("True", "✔").replace("False", "❌")
        inv_splash = "INVITE_SPLASH" in server.features
        em = discord.Embed(title="Server info", colour=server.owner.colour)
        em.add_field(name="Name", value=server.name)
        em.add_field(name="Server ID", value=server.id)
        em.add_field(name="Region", value=server.region)
        em.add_field(name="Existed since", value=server.created_at.strftime('%d.%m.%Y %H:%M:%S %Z'))
        em.add_field(name="Owner", value=server.owner)
        em.add_field(name="AFK Timeout and Channel", value=str(afk) + " min in " + str(server.afk_channel))
        em.add_field(name="Verification level",
                     value=str(server.verification_level)
                     .replace("none", "None")
                     .replace("low", "Low")
                     .replace("medium", "Medium")
                     .replace("high", "(╯°□°）╯︵ ┻━┻"))
        em.add_field(name="2FA admins", value=str(server.mfa_level).replace("0", "❌").replace("1", "✔"))
        em.add_field(name="Member Count", value=server.member_count)
        em.add_field(name="Role Count", value=str(len(server.roles)))
        em.add_field(name="Channel Count", value=str(len(server.channels)))
        em.add_field(name="VIP Voice Regions", value=vip_regs)
        em.add_field(name="Vanity URL", value=van_url)
        if not inv_splash:
            em.add_field(name="Invite Splash", value="❌")
        elif server.splash_url == "":
            em.add_field(name="Invite Splash", value="✔")
        else:
            em.add_field(name="Invite Splash", value="✔ [🔗](" + server.splash_url + ")")
        em.set_image(url=server.icon_url)
        if check.embeds_allowed(ctx.message):
            await self.bot.say(embed=em)
        else:
            await self.bot.say("```\n" +
                               "Name: "+server.name +
                               "\nServer ID: "+server.id +
                               "\nRegion: "+str(server.region) +
                               "\nExisted since: "+server.created_at.strftime('%d.%m.%Y %H:%M:%S %Z') +
                               "\nOwner: "+str(server.owner) +
                               "\nAFK timeout and Channel: "+str(afk) + " min in " + str(server.afk_channel) +
                               "\nVerification level: " +
                               str(server.verification_level).replace("none", "None").replace("low", "Low")
                               .replace("medium", "Medium").replace("high", "(╯°□°）╯︵ ┻━┻") +
                               "\n2FA admins: "+str(server.mfa_level).replace("0", "❌").replace("1", "✔") +
                               "\nMember Count: "+str(server.member_count) +
                               "\nRole Count: "+str(len(server.roles)) +
                               "\nChannel Count: "+str(len(server.channels)) +
                               "\nVIP Voice Regions: "+vip_regs +
                               "\nVanity URL: "+van_url +
                               "\nInvite Splash: "+str(inv_splash).replace("True", "✔").replace("False", "❌") +
                               "\nInvite Splash URL: "+server.splash_url +
                               "```\n" +
                               server.icon_url)
        await self.bot.delete_message(ctx.message)

    @commands.command(pass_context=True, no_pm=True, aliases=['channelinfo', 'chaninfo', 'chan'])
    async def channel(self, ctx, *, channel: discord.Channel):
        """Get info about channel"""
        changed_roles = []
        for elem in channel.changed_roles:
            changed_roles.append(elem.name)
        em = discord.Embed(title=channel.name, description=channel.topic, colour=random.randint(0, 16777215))
        em.add_field(name="ID", value=channel.id)
        em.add_field(name="Type", value=str(channel.type).replace("voice", "🔈").replace("text", "📰"))
        em.add_field(name="Has existed since", value=channel.created_at.strftime('%d.%m.%Y %H:%M:%S %Z'))
        em.add_field(name="Position", value=channel.position)
        em.add_field(name="Changed roles permissions",
                     value="\n".join([str(x) for x in changed_roles]) or "`Not set`")
        em.add_field(name="Mention", value=channel.mention + "\n`" + channel.mention + "`")
        if check.embeds_allowed(ctx.message):
            await self.bot.say(embed=em)
        else:
            await self.bot.say("```\n" +
                               "Name: " + channel.name +
                               "\nTopic: " + channel.topic +
                               "\nID: " + channel.id +
                               "\nType: " + channel.type.name +
                               "\nHas existed since: " + channel.created_at.strftime('%d.%m.%Y %H:%M:%S %Z') +
                               "\nPosition: " + str(channel.position) +
                               "\nChanged roles permissions: " + "\n".join([str(x) for x in changed_roles]) +
                               "\nMention: " + channel.mention +
                               "```")
        await self.bot.delete_message(ctx.message)

    @commands.command(pass_context=True, no_pm=True, aliases=['channellist', 'listchannels'])
    async def channels(self, ctx, server: str = None):
        """Get all channels on server"""
        if server is None:
            server = ctx.message.server
        else:
            server = discord.utils.get(self.bot.servers, id=server)
        if server is None:
            await self.bot.say("Failed to get server with provided ID")
            await self.bot.delete_message(ctx.message)
            return
        vchans = []
        tchans = []
        for elem in server.channels:
            if str(elem.type) == "voice":
                vchans.append(elem.name)
            elif str(elem.type) == "text":
                tchans.append(elem.name)
        em = discord.Embed(title="Channels list", colour=random.randint(0, 16777215))
        em.add_field(name="Text channels:", value="\n".join([str(x) for x in tchans]), inline=False)
        em.add_field(name="Voice channels:", value="\n".join([str(x) for x in vchans]), inline=False)
        em.set_footer(text="Total count of channels: " + str(len(server.channels)) +
                           " | Text Channels: " + str(len(tchans)) + " | Voice Channels: " + str(len(vchans)))
        if check.embeds_allowed(ctx.message):
            await self.bot.say(embed=em)
        else:
            await self.bot.say("**Text channels:**\n```" + "\n".join([str(x) for x in tchans]) +
                               "```**Voice channels:**\n```" + "\n".join([str(x) for x in vchans]) +
                               "```\nTotal count: " + str(len(server.channels)) +
                               " | Text Channels: " + str(len(tchans)) +
                               " | Voice Channels: " + str(len(vchans)))
        await self.bot.delete_message(ctx.message)

    @commands.command(pass_context=True, no_pm=True, aliases=['roleinfo'])
    async def role(self, ctx, *, role: discord.Role):
        """Get info about role"""
        em = discord.Embed(title=role.name, colour=role.colour)
        em.add_field(name="ID", value=role.id)
        em.add_field(name="Perms",
                     value="[" + str(role.permissions.value) + "](https://discordapi.com/permissions.html#" + str(
                         role.permissions.value) + ")")
        em.add_field(name="Has existed since", value=role.created_at.strftime('%d.%m.%Y %H:%M:%S %Z'))
        em.add_field(name="Hoist", value=str(role.hoist)
                     .replace("True", "✔")
                     .replace("False", "❌"))
        em.add_field(name="Position", value=role.position)
        em.add_field(name="Color", value=role.colour)
        em.add_field(name="Managed", value=str(role.managed).replace("True", "✔").replace("False", "❌"))
        em.add_field(name="Mentionable", value=str(role.mentionable).replace("True", "✔").replace("False", "❌"))
        em.add_field(name="Mention", value=role.mention + "\n`" + role.mention + "`")
        em.set_thumbnail(url="https://xenforo.com/community/rgba.php?r=" + str(role.colour.r) + "&g=" + str(
            role.colour.g) + "&b=" + str(role.colour.b) + "&a=255")
        if check.embeds_allowed(ctx.message):
            await self.bot.say(embed=em)
        else:
            await self.bot.say("```\n" +
                               "ID: " + role.id +
                               "\nPerms: " + str(role.permissions.value) +
                               "\nHas existed since: " + role.created_at.strftime('%d.%m.%Y %H:%M:%S %Z') +
                               "\nHoist: " + str(role.hoist).replace("True", "✔").replace("False", "❌") +
                               "\nPosition: " + str(role.position) +
                               "\nColor: " + str(cc.rgb_to_hex(cc.get_rgb_from_int(role.colour.value))) +
                               "\nManaged: " + str(role.managed).replace("True", "✔").replace("False", "❌") +
                               "\nMentionable: " + str(role.mentionable).replace("True", "✔").replace("False", "❌") +
                               "\nMention: " + str(role.mention) +
                               "```")
        await self.bot.delete_message(ctx.message)

    @commands.command(pass_context=True, no_pm=True, aliases=['listroles', 'rolelist'])
    async def roles(self, ctx, server: str = None):
        """Get all roles on server"""
        if server is None:
            server = ctx.message.server
        else:
            server = discord.utils.get(self.bot.servers, id=server)
        if server is None:
            await self.bot.say("Failed to get server with provided ID")
            await self.bot.delete_message(ctx.message)
            return
        roles = []
        for elem in server.role_hierarchy:
            roles.append(elem.name)
        em = discord.Embed(title="List of roles", description="\n".join([str(x) for x in roles]),
                           colour=random.randint(0, 16777215))
        em.set_footer(text="Total count of roles: " + str(len(server.roles)))
        if check.embeds_allowed(ctx.message):
            await self.bot.say(embed=em)
        else:
            await self.bot.say("**List of roles:**\n```" + "\n".join([str(x) for x in roles]) +
                               "```\nTotal count: " + str(len(server.roles)))
        await self.bot.delete_message(ctx.message)


def setup(bot):
    bot.add_cog(Moderation(bot))
