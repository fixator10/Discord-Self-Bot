import discord
from discord.ext import commands


def can_invite(message):
    return message.channel.permissions_for(message.author).create_instant_invite


class Admin:
    def __init__(self, bot):
        self.bot = bot

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


def setup(bot):
    bot.add_cog(Admin(bot))
