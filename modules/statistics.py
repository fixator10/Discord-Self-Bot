from discord.ext import commands
from .utils.dataIO import dataIO
import datetime
import asyncio
import discord
import os

try:
    import psutil
except:
    psutil = False


class Statistics:
    """
    Statistics
    """

    def __init__(self, bot):
        self.bot = bot
        self.settings = dataIO.load_json('data/statistics/settings.json')
        self.refresh_rate = self.settings['REFRESH_RATE']

    @commands.command()
    async def stats(self):
        """
        Retreive statistics
        """
        message = await self.retrieve_statistics()
        await self.bot.say(embed=message)

    async def retrieve_statistics(self):
        name = self.bot.user.name
        users = str(len(set(self.bot.get_all_members())))
        servers = str(len(self.bot.servers))
        text_channels = 0
        voice_channels = 0

        cpu_p = psutil.cpu_percent(interval=None, percpu=True)
        cpu_usage = sum(cpu_p) / len(cpu_p)

        mem_v = psutil.virtual_memory()

        for channel in self.bot.get_all_channels():
            if channel.type == discord.ChannelType.text:
                text_channels += 1
            elif channel.type == discord.ChannelType.voice:
                voice_channels += 1
        channels = text_channels + voice_channels

        em = discord.Embed(description='\a\n', color=discord.Color.red())
        avatar = self.bot.user.avatar_url if self.bot.user.avatar else self.bot.user.default_avatar_url
        em.set_author(name='Statistics of {}'.format(name), icon_url=avatar)
        em.add_field(name='**Uptime**', value='{}'.format(self.get_bot_uptime(brief=True)))

        em.add_field(name='**Users**', value=users)
        em.add_field(name='**Servers**', value=servers)

        em.add_field(name='**Channels**', value=str(channels))
        em.add_field(name='**Text channels**', value=str(text_channels))
        em.add_field(name='**Voice channels**', value=str(voice_channels))

        em.add_field(name='\a', value='\a')

        em.add_field(name='**Active cogs**', value=str(len(self.bot.cogs)))
        em.add_field(name='**Commands**', value=str(len(self.bot.commands)))
        em.add_field(name='\a', value='\a')

        em.add_field(name='\a', value='\a', inline=False)
        em.add_field(name='**CPU usage**', value='{0:.1f}%'.format(cpu_usage))
        em.add_field(name='**Memory usage**', value='{0:.1f}%'.format(mem_v.percent))

        em.add_field(name='\a', value='\a')
        em.set_footer(text='API version {}'.format(discord.__version__))
        return em

    def get_bot_uptime(self, *, brief=False):
        # Stolen from owner.py - Courtesy of Danny
        now = datetime.datetime.utcnow()
        delta = now - self.bot.uptime
        hours, remainder = divmod(int(delta.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)

        if not brief:
            if days:
                fmt = '{d} days, {h} hours, {m} minutes, and {s} seconds'
            else:
                fmt = '{h} hours, {m} minutes, and {s} seconds'
        else:
            fmt = '{h} H - {m} M - {s} S'
            if days:
                fmt = '{d} D - ' + fmt

        return fmt.format(d=days, h=hours, m=minutes, s=seconds)

    async def reload_stats(self):
        await asyncio.sleep(30)
        while self == self.bot.get_cog('Statistics'):
            if self.settings['CHANNEL_ID']:
                msg = await self.retrieve_statistics()
                channel = discord.utils.get(
                    self.bot.get_all_channels(), id=self.settings['CHANNEL_ID'])
                messages = False
                async for message in self.bot.logs_from(channel, limit=1):
                    messages = True
                    if message.author.name == self.bot.user.name:
                        await self.bot.edit_message(message, embed=msg)
                if not messages:
                    await self.bot.send_message(channel, embed=msg)
            else:
                pass
            await asyncio.sleep(self.refresh_rate)


def check_folder():
    if not os.path.exists('data/statistics'):
        print('Creating data/statistics folder...')
        os.makedirs('data/statistics')


def check_file():
    data = {}
    data['CHANNEL_ID'] = ''
    data['SENT_MESSAGES'] = 0
    data['RECEIVED_MESSAGES'] = 0
    data['REFRESH_RATE'] = 5
    f = 'data/statistics/settings.json'
    if not dataIO.is_valid_json(f):
        print('Creating default settings.json...')
        dataIO.save_json(f, data)


def setup(bot):
    if psutil is False:
        raise RuntimeError('psutil is not installed. Run `pip3 install psutil --upgrade` to use this cog.')
    else:
        check_folder()
        check_file()
        n = Statistics(bot)
        bot.add_cog(n)
        bot.loop.create_task(n.reload_stats())
