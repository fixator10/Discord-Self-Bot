import aiohttp
import discord
from discord.ext import commands

import modules.utils.checks as check


class Admin:
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession(loop=self.bot.loop)

    @commands.command(pass_context=True)
    async def ban(self, ctx, member: discord.Member, delete_messages: int = 1):
        """Bans a member
        User must have ban member permissions"""
        if not check.ban_allowed(ctx.message):
            await self.bot.say("Not allowed to ban someone here. Lack `Ban Members` permission.")
        await self.bot.ban(member, delete_message_days=delete_messages)
        await self.bot.say("User `"+member.name+"` banned\n"+str(delete_messages)+" days of user's messages removed")
        await self.bot.delete_message(ctx.message)

    @commands.command(pass_context=True)
    async def kick(self, ctx, member: discord.Member):
        """Kicks a member
        User must have kick member permissions"""
        if not check.kick_allowed(ctx.message):
            await self.bot.say("Not allowed to kick someone here. Lack `Kick Members` permission.")
        await self.bot.kick(member)
        await self.bot.say("User `"+member.name+"` kicked")
        await self.bot.delete_message(ctx.message)

    @commands.command(pass_context=True)
    async def invite(self, ctx):
        """Creates a server invite
        Usage:
        self.invite"""
        if not check.can_invite(ctx.message):
            await self.bot.say("Not allowed to create instant invite here. Lack `Create Instant Invite` permission")
            await self.bot.delete_message(ctx.message)
            return
        server = ctx.message.server
        invite = await self.bot.create_invite(server)
        await self.bot.say(invite.url)
        await self.bot.delete_message(ctx.message)

    @commands.command(pass_context=True)
    async def add_emoji(self, ctx, emoji_name: str, emoji_url: str):
        """Adds an emoji to server
        Requires proper permissions
        PNG/JPG only"""
        if not check.manage_emoji(ctx.message):
            await self.bot.say("Not allowed to add emojis here. Lack `Manage Emojis` permission")
            await self.bot.delete_message(ctx.message)
            return
        try:
            async with self.session.get(emoji_url) as r:  # from Red's owner.py
                data = await r.read()
            await self.bot.create_custom_emoji(server=ctx.message.server, name=emoji_name, image=data)
            await self.bot.say("Done.")
        except Exception as e:
            await self.bot.say("Failed: `"+str(e)+"`")
        await self.bot.delete_message(ctx.message)

    @commands.command(pass_context=True)
    async def massnick(self, ctx, nickname: str):
        """Mass nicknames everyone on the server"""
        server = ctx.message.server
        counter = 0
        for user in server.members:
            if user.nick is None:
                nickname = "{} {}".format(nickname, user.name)
            else:
                nickname = "{} {}".format(nickname, user.nick)
            try:
                await self.bot.change_nickname(user, nickname)
            except discord.HTTPException:
                counter += 1
                continue
        await self.bot.say("Finished nicknaming server. {} nicknames could not be completed.".format(counter))

    @commands.command(pass_context=True)
    async def resetnicks(self, ctx):
        server = ctx.message.server
        for user in server.members:
            try:
                await self.bot.change_nickname(user, nickname=None)
            except discord.HTTPException:
                continue
        await self.bot.say("Finished resetting server nicknames")


def setup(bot):
    bot.add_cog(Admin(bot))
