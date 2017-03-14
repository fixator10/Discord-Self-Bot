import aiohttp
import discord
from discord.ext import commands
from asyncio import sleep

import modules.utils.chat_formatting as chat


class Admin:
    def __init__(self, bot: discord.Client):
        self.bot = bot
        self.session = aiohttp.ClientSession(loop=self.bot.loop)

    @commands.command(pass_context=True)
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, delete_messages: int = 1):
        """Bans a member
        User must have ban member permissions"""
        await self.bot.ban(member, delete_message_days=delete_messages)
        await self.bot.say(
            "User `" + member.name + "` banned\n" + str(delete_messages) + " days of user's messages removed")
        await self.bot.delete_message(ctx.message)

    @commands.command(pass_context=True)
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member):
        """Kicks a member
        User must have kick member permissions"""
        await self.bot.kick(member)
        await self.bot.say("User `" + member.name + "` kicked")
        await self.bot.delete_message(ctx.message)

    @commands.command(pass_context=True, aliases=["prune"])
    @commands.has_permissions(kick_members=True)
    async def cleanup(self, ctx, days: int = 1):
        """Cleanup inactive server members"""
        await self.bot.delete_message(ctx.message)
        to_kick = await self.bot.estimate_pruned_members(ctx.message.server, days=days)
        await self.bot.say(chat.warning("You about to kick **{}** inactive for **{}** days members from this server. "
                                        "Are you sure?\nTo agree, type \"yes\"".format(to_kick, days)))
        await sleep(3)
        resp = await self.bot.wait_for_message(author=ctx.message.author, channel=ctx.message.channel)
        if resp.content.lower().strip() == "yes":
            cleanup = await self.bot.prune_members(ctx.message.server, days=days)
            await self.bot.say(chat.info("**{}**/**{}** inactive members removed.\n"
                               "(They was inactive for **{}** days)".format(cleanup, to_kick, days)))
        else:
            await self.bot.say(chat.error("Inactive members cleanup canceled."))

    @commands.command(pass_context=True)
    @commands.has_permissions(create_instant_invite=True)
    async def invite(self, ctx):
        """Creates a server invite"""
        server = ctx.message.server
        invite = await self.bot.create_invite(server)
        await self.bot.say(invite.url)
        await self.bot.delete_message(ctx.message)

    @commands.command(pass_context=True)
    @commands.has_permissions(manage_emojis=True)
    async def add_emoji(self, ctx, emoji_name: str, emoji_url: str):
        """Adds an emoji to server
        Requires proper permissions
        PNG/JPG only"""
        try:
            async with self.session.get(emoji_url) as r:  # from Red's owner.py
                data = await r.read()
            await self.bot.create_custom_emoji(server=ctx.message.server, name=emoji_name, image=data)
            await self.bot.say("Done.")
        except Exception as e:
            await self.bot.say("Failed: " + chat.inline(e))
        await self.bot.delete_message(ctx.message)

    @commands.command(pass_context=True)
    @commands.has_permissions(manage_nicknames=True)
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
    @commands.has_permissions(manage_nicknames=True)
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
