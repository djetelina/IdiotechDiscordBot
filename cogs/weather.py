import aiohttp
import pycountry
from discord.ext import commands

from helpers import tokens as t, descriptions as desc


class Weather:
    def __init__(self, bot):
        self.bot = bot

        self.key = t.weather_key
        self.base_url = "http://api.openweathermap.org/data/2.5/weather?q="
        self.a_url = "&appid="

    @commands.command(passcontext=True, description=desc.weather, brief=desc.weatherb)
    async def weather(self, *, loc: str):
        spaces = ' ' in loc
        if not spaces:
            msg = await self.bot.say("***Getting Weather Status for {}. This may take a while.***".format(loc))

            weather_api = self.base_url + loc + self.a_url + self.key

            with aiohttp.ClientSession() as session:
                async with session.get(weather_api)as resp:
                    data = await resp.json()

                    temp = data["main"]["temp"]
                    brief = data["weather"][0]["main"]
                    desc = data["weather"][0]["description"]
                    name = data["name"]
                    cloud = str(data["clouds"]["all"])
                    country = pycountry.countries.get(alpha2=data["sys"]["country"])

                    desc = capital_everything(desc)
                    cel = to_1dp(str(kel_to_cel(temp)))
                    fah = to_1dp(str(cel_to_fah(cel)))

                    await self.bot.edit_message(msg, "__**{}, {} - Weather Status**__\n"
                                                     "**Temperature:** {}c  -  {}f\n"
                                                     "**Weather:** {} - {}\n"
                                                     "**Cloudiness:** {} percent".format(name, country.name, cel, fah,
                                                                                         brief, desc, cloud))

        else:
            await self.bot.say("**Error:** City name cannot contains spaces, use underscores instead of spaces.\n"
                               "E.g. 'New_York' instead of 'New York'")


def setup(bot):
    bot.add_cog(Weather(bot))


def kel_to_cel(kelvin):
    """
    Converts Kelvin to Celsius

    :param kelvin:
    :return: Celsius:
    """
    result = float(kelvin) - 273.15
    return result


def cel_to_fah(cels):
    """
    Converts Celsius to Fahrenheit

    :param cels: Celsius
    :return: Fahrenheit:
    """
    result = (float(cels) * 1.8) + 32
    return result


def capital_everything(string):
    """
    Takes a string, such as "hello world" and capitalizes each world
    returning "Hello World" for example

    :param string:
    :return: The capitalized words in a string:
    """
    listy = string.split()
    new_list = []
    for word in listy:
        thing = word.capitalize()
        new_list.append(thing)
    result = ' '.join(new_list)
    return result


def to_1dp(value):
    """
    Shortens a number to 1 decimal point

    :param value:
    :return: string of number to 1 decimal point
    """
    before, after = str(value).split(".")
    after = after[0:1]
    result = before + "." + after
    return result
