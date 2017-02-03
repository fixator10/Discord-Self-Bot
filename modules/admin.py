import discord
from discord.ext import commands
import json

class Admin():
    def __init__(self, bot):
        self.bot = bot

    # Changes the bot's game
    @commands.command(pass_conext=True)
    async def status(self, *, status: str):
        """Updates the user's status
        Usage:
        self.status This is my status"""
        # Update the bots game
        await self.bot.change_presence(game=discord.Game(name=status), afk=True, status=discord.Status.idle)
        await self.bot.say("Status updated to {}".format(status))

    @commands.command(pass_context=True)
    async def invite(self, ctx):
        """Creates a server invite
        Usage:
        self.invite"""
        server = ctx.message.server
        invite = await self.bot.create_invite(server)
        await self.bot.say(invite.url)

def setup(bot):
    bot.add_cog(Admin(bot))
