# -*- coding: utf-8 -*-
import discord
from discord.ext import commands
import json
import asyncio
import re
import time, datetime
import matplotlib.colors as colors
import colorsys

class Custom():
    def __init__(self, bot):
        self.bot = bot
            
    @commands.command(pass_context=True)
    async def quote(self, ctx, messageid : str, *, response : str = None):
        """Quote an message by id"""
        message = discord.utils.get(self.bot.messages, id=messageid)
        if message == None:
            await self.bot.say("Failed to get message with id `"+messageid+"`")
        else:
            em = discord.Embed(description=message.content, colour=message.author.colour, timestamp=message.timestamp)
            em.set_author(name=message.author.nick or message.author.name, icon_url=message.author.avatar_url)
            em.set_footer(text=message.author.name+"#"+message.author.discriminator)
            attachment = discord.utils.get(message.attachments)
            if attachment != None:
                attachment = dict(attachment)
                em.set_image(url=attachment['url'])
            await self.bot.say(response, embed=em)
        await self.bot.delete_message(ctx.message)
		
    @commands.command(pass_context=True)
    async def roleinfo(self, ctx, role : discord.Role):
        """Get info about role"""
        em = discord.Embed(title=role.name, colour=role.colour)
        em.add_field(name="ID", value=role.id)
        em.add_field(name="Perms", value="["+str(role.permissions.value)+"](https://discordapi.com/permissions.html#"+str(role.permissions.value)+")")
        em.add_field(name="Has existed since", value=role.created_at.strftime('%d.%m.%Y %H:%M:%S %Z'))
        em.add_field(name="Hoist", value=str(role.hoist).replace("True","✔").replace("False","❌"))
        em.add_field(name="Position", value=role.position)
        em.add_field(name="Color", value=role.colour)
        em.add_field(name="Managed", value=str(role.managed).replace("True","✔").replace("False","❌"))
        em.add_field(name="Mentionable", value=str(role.mentionable).replace("True","✔").replace("False","❌"))
        em.add_field(name="Mention", value=role.mention+"\n`"+role.mention+"`")
        em.set_thumbnail(url="https://xenforo.com/community/rgba.php?r=" + str(role.colour.r) + "&g=" + str(role.colour.g) + "&b=" + str(role.colour.b) + "&a=255")
        await self.bot.say(embed=em)
        await self.bot.delete_message(ctx.message)
		
    @commands.command(pass_context=True)
    async def hug(self, ctx, user : discord.Member, intensity : int=1):
        """Because everyone likes hugs

        Up to 10 intensity levels."""
        name = " *" + user.name + "*"
        if intensity <= 0:
            msg = "(っ˘̩╭╮˘̩)っ" + name
        elif intensity <= 3:
            msg = "(っ´▽｀)っ" + name
        elif intensity <= 6:
            msg = "╰(*´︶`*)╯" + name
        elif intensity <= 9:
            msg = "(つ≧▽≦)つ" + name
        elif intensity >= 10:
            msg = "(づ￣ ³￣)づ" + name + " ⊂(´・ω・｀⊂)"
        await self.bot.say(msg)
        await self.bot.delete_message(ctx.message)
		
    @commands.command(pass_context=True)
    async def flip(self, ctx, user : discord.Member=None):
        """Flips a coin... or a user.

        Defaults to coin.
        """
        if user != None:
            msg = ""
            if user.id == self.bot.user.id:
                user = ctx.message.author
                msg = "Nice try. You think this is funny? How about *this* instead:\n\n"
            char = "abcdefghijklmnopqrstuvwxyz"
            tran = "ɐqɔpǝɟƃɥᴉɾʞlɯuodbɹsʇnʌʍxʎz"
            table = str.maketrans(char, tran)
            name = user.display_name.translate(table)
            char = char.upper()
            tran = "∀qƆpƎℲפHIſʞ˥WNOԀQᴚS┴∩ΛMX⅄Z"
            table = str.maketrans(char, tran)
            name = name.translate(table)
            await self.bot.say(msg + "(╯°□°）╯︵ " + name[::-1])
        else:
            await self.bot.say("*flips a coin and... " + choice(["HEADS!*", "TAILS!*"]))
        await self.bot.delete_message(ctx.message)
		
    @commands.command(pass_context=True, no_pm=True, name='thetime')
    async def _thetime(self, ctx):
        """Send your current time"""
        await self.bot.say(datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S %Z'))
        await self.bot.delete_message(ctx.message)
		
    @commands.command(pass_context=True)
    async def emojify(self, ctx, *, message : str):
        """emojify text"""
        char = "abcdefghijklmnopqrstuvwxyz↓↑←→—.!"
        tran = "🇦🇧🇨🇩🇪🇫🇬🇭🇮🇯🇰🇱🇲🇳🇴🇵🇶🇷🇸🇹🇺🇻🇼🇽🇾🇿⬇⬆⬅➡➖⏺ℹ"
        table = str.maketrans(char, tran)
        name = message.translate(table)
        char = char.upper()
        table = str.maketrans(char, tran)
        name = name.translate(table)
        await self.bot.say(name.replace(" ", "　　").replace("", "​").replace("0", ":zero:").replace("1", ":one:").replace("2", ":two:").replace("3", ":three:").replace("4", ":four:").replace("5", ":five:").replace("6", ":six:").replace("7", ":seven:").replace("8", ":eight:").replace("9", ":nine:").replace("#", "#⃣").replace("*", "*⃣"))
        await self.bot.delete_message(ctx.message)

    @commands.command(pass_context=True)
    async def pingtime(self,ctx):
        """pseudo-ping time"""
        channel = ctx.message.channel
        t1 = time.perf_counter()
        await self.bot.send_typing(channel)
        t2 = time.perf_counter()
        await self.bot.say("pseudo-ping: `{}ms`".format(round((t2-t1)*1000)))
        await self.bot.delete_message(ctx.message)

    @commands.command(pass_context=True, aliases=['HEX', 'hex'])
    async def color(self, ctx, color : str):
        """Shows some info about provided HEX color"""
        pattern = re.compile("^#([A-Fa-f0-9]{6})$")
        if pattern.match(color):
            colorrgb = self.hex_to_rgb(color)
            colorint = self.getIfromRGB(colorrgb)
            colorhsv = colorsys.rgb_to_hsv(colorrgb[0], colorrgb[1], colorrgb[2])
            colorhls = colorsys.rgb_to_hls(colorrgb[0], colorrgb[1], colorrgb[2])
            coloryiq = colorsys.rgb_to_yiq(colorrgb[0], colorrgb[1], colorrgb[2])
            colorcmyk = self.rgb_to_cmyk(colorrgb[0], colorrgb[1], colorrgb[2])
            em = discord.Embed(title=str(color), description="Provided HEX: "+color+"\nRGB: "+str(colorrgb)+"\nCMYK: "+str(colorcmyk)+"\nHSV: "+str(colorhsv)+"\nHLS: "+str(colorhls)+"\nYIQ: "+str(coloryiq)+"\nint: "+str(colorint), url='http://www.colorpicker.com/'+str(color.lstrip('#')), colour=colorint, timestamp=ctx.message.timestamp)
            em.set_thumbnail(url="https://xenforo.com/community/rgba.php?r=" + str(colorrgb[0]) + "&g=" + str(colorrgb[1]) + "&b=" + str(colorrgb[2]) + "&a=255")
            await self.bot.say(embed=em)
        else:
            await self.bot.say("Looks like the `{}`, that you provided is not color HEX\nOr it is too small/too big.\nExample of acceptable color HEX: `#1A2B3C`".format(color))
        await self.bot.delete_message(ctx.message)

    def rgb_to_cmyk(self,r,g,b):
        rgb_scale = 255
        cmyk_scale = 100
        if (r == 0) and (g == 0) and (b == 0):
            # black
            return 0, 0, 0, cmyk_scale

        # rgb [0,255] -> cmy [0,1]
        c = 1 - r / float(rgb_scale)
        m = 1 - g / float(rgb_scale)
        y = 1 - b / float(rgb_scale)

        # extract out k [0,1]
        min_cmy = min(c, m, y)
        c = (c - min_cmy) 
        m = (m - min_cmy) 
        y = (y - min_cmy) 
        k = min_cmy

        # rescale to the range [0,cmyk_scale]
        return c*cmyk_scale, m*cmyk_scale, y*cmyk_scale, k*cmyk_scale

    def cmyk_to_rgb(c,m,y,k):
        rgb_scale = 255
        cmyk_scale = 100
        """
        """
        r = rgb_scale*(1.0-(c+k)/float(cmyk_scale))
        g = rgb_scale*(1.0-(m+k)/float(cmyk_scale))
        b = rgb_scale*(1.0-(y+k)/float(cmyk_scale))
        return r,g,b
		
    def getRGBfromI(self,RGBint):
        blue =  RGBint & 255
        green = (RGBint >> 8) & 255
        red =   (RGBint >> 16) & 255
        return red, green, blue

    def getIfromRGB(self,rgb):
        red = rgb[0]
        green = rgb[1]
        blue = rgb[2]
        RGBint = (red<<16) + (green<<8) + blue
        return RGBint
		
    def hex_to_rgb(self,hex_string):
        rgb = colors.hex2color(hex_string)
        return tuple([int(255*x) for x in rgb])
    
    def rgb_to_hex(self,rgb_tuple):
        return colors.rgb2hex([1.0*x/255 for x in rgb_tuple])

def setup(bot):
    bot.add_cog(Custom(bot))
