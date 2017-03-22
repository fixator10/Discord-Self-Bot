import forecastio
import geocoder
import discord
import datetime
from modules.utils.dataIO import dataIO
from modules.utils.helpers import Checks
from discord.ext import commands


def xstr(s):
    if s is None:
        return ''
    return str(s)


dictionary = {
    "clear-day": ":sunny:",
    "clear-night": ":night_with_stars:",
    "rain": ":cloud_rain:",
    "snow": ":cloud_snow:",
    "sleet": ":snowflake:",
    "wind": ":wind_blowing_face: ",
    "fog": ":foggy:",
    "cloudy": ":white_sun_cloud:",
    "partly-cloudy-day": ":white_sun_small_cloud:",
    "partly-cloudy-night": ":night_with_stars:",
    "": ":sunny:"
}

config = dataIO.load_json("data/SelfBot/config.json")


class Weather:
    apikey = config["dark_sky_api_key"]

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def weather(self, ctx, place: str = None):
        """Shows weather in provided place"""
        if place is None:
            place = config["hometown"]
        g = geocoder.google(place)
        if len(g.latlng) == 0:
            await self.bot.say("Cannot find a place `" + place + "`")
            return
        forecast = forecastio.load_forecast(self.apikey, g.latlng[0], g.latlng[1], units="si")
        by_hour = forecast.currently()
        place = g.city_long + " | " + xstr(g.country_long)

        content = "Weather in " + place \
                  + ":\n" + by_hour.summary + "\n" + str(by_hour.temperature) + \
                  "˚C" + "\n" + dictionary.get(xstr(by_hour.icon))
        em = discord.Embed(description=content, colour=0xff0000, timestamp=by_hour.time)
        if Checks.embeds_allowed(ctx.message):
            await self.bot.say(embed=em)
        else:
            await self.bot.say(content)

    # @commands.command(pass_context=True)
    # async def time(self, ctx, place: str = None):
    #     if place is None:
    #         forecast = forecastio.load_forecast(self.apikey, "40.241495", "-75.283786", units="si")
    #         by_hour = forecast.currently()
    #         place = "Lansdale, PA"
    #     else:
    #         g = geocoder.google(place)
    #         if len(g.latlng) == 0:
    #             await self.bot.say("Cannot find a place " + place)
    #             return
    #         forecast = forecastio.load_forecast(self.apikey, g.latlng[0], g.latlng[1], units="si")
    #         by_hour = forecast.currently()
    #
    #     await self.bot.say("Time in " + place + " " + by_hour.time.timetz().isoformat())

    @commands.command(pass_context=True)
    async def forecast(self, ctx, place: str = None):
        """Shows 7 days forecast for provided place"""
        if place is None:
            place = config["hometown"]
        g = geocoder.google(place)
        if len(g.latlng) == 0:
            await self.bot.say("Cannot find a place `" + place + "`")
            return
        forecast = forecastio.load_forecast(self.apikey, g.latlng[0], g.latlng[1], units="si")
        by_hour = forecast.daily()
        place = g.city_long + " | " + xstr(g.country_long)

        content = "Weather in " + place + ":\n"
        for i in range(0, 6):
            content = content + \
                      "__***" + by_hour.data[i].time.strftime("%d/%m") + ":***__       " + \
                      xstr(by_hour.data[i].temperatureMin) + " - " + \
                      xstr(by_hour.data[i].temperatureMax) + "˚C       " \
                      + dictionary.get(xstr(by_hour.data[i].icon)) + "\n"
        em = discord.Embed(description=content, colour=0xff0000, timestamp=datetime.datetime.now())
        if Checks.embeds_allowed(ctx.message):
            await self.bot.say(embed=em)
        else:
            await self.bot.say(content)


def setup(bot):
    bot.add_cog(Weather(bot))
