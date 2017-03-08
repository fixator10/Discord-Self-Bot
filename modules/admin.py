import aiohttp
from discord.ext import commands


def can_invite(message):
    return message.channel.permissions_for(message.author).create_instant_invite


def manage_emoji(message):
    return message.channel.permissions_for(message.author).manage_emojis


class Admin:
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession(loop=self.bot.loop)

    # # Changes the bot's game
    # @commands.command(pass_conext=True)
    # async def status(self, *, status: str):
    #     """Updates the user's status
    #     Usage:
    #     self.status This is my status"""
    #     # Update the bots game
    #     await self.bot.change_presence(game=discord.Game(name=status), afk=True, status=discord.Status.idle)
    #     await self.bot.say("Status updated to {}".format(status))
    #     await self.bot.delete_message(ctx.message)

    @commands.command(pass_context=True)
    async def invite(self, ctx):
        """Creates a server invite
        Usage:
        self.invite"""
        if not can_invite(ctx.message):
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
        if not manage_emoji(ctx.message):
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


def setup(bot):
    bot.add_cog(Admin(bot))
