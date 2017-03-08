import forecastio
import geocoder
import discord
from modules.utils.dataIO import dataIO
from discord.ext import commands


def embeds_allowed(message):
    return message.channel.permissions_for(message.author).embed_links


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
    "partly-cloudy-night": ":night_with_stars:"
}

config = dataIO.load_json("data/SelfBot/config.json")


class Weather:
    apikey = config["dark_sky_api_key"]

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def weather(self, ctx, place: str = None):
        """Shows weather in provided place"""
        await self.bot.delete_message(ctx.message)
        if place is None:
            place = config["hometown"]
        g = geocoder.google(place)
        if len(g.latlng) == 0:
            await self.bot.say("Cannot find a place `" + place + "`")
            return
        forecast = forecastio.load_forecast(self.apikey, g.latlng[0], g.latlng[1], units="si")
        by_hour = forecast.currently()
        place = place + " | " + g.country

        content = "Weather in " + place \
                  + ":\n" + by_hour.summary + "\n" + str(by_hour.temperature) + \
                  "˚C" + "\n" + dictionary.get(by_hour.icon)
        em = discord.Embed(description=content, colour=0xff0000, timestamp=by_hour.time)
        if embeds_allowed(ctx.message):
            await self.bot.say(embed=em)
        else:
            await self.bot.say(content)

    # @commands.command(pass_context=True)
    # async def time(self, ctx, place: str = None):
    #     await self.bot.delete_message(ctx.message)
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
    #     await self.bot.say("Current time in " + place + " is `" + by_hour.time.timetz().isoformat() + "`")


def setup(bot):
    bot.add_cog(Weather(bot))
