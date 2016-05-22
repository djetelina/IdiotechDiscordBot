"""
================================================

REQUIRES INSTALLATION OF PYCOUNTRY

================================================
"""

from discord.ext import commands
import simplify as s
import aiohttp
import tokens as t
import pycountry


class Weather:
    def __init__(self, bot):
        self.bot = bot

        self.key = t.weather_key  # gets key from tokens.py
        self.base_url = "http://api.openweathermap.org/data/2.5/weather?q="  # base url (before query and key)
        self.a_url = "&appid="  # additional url (comes after query and before key)

    @commands.command(passcontext=True, description="Get Weather Status in <loc> (a given city name)",
                      brief="Finds Weather Status for input city")
    async def weather(self,  *, loc: str):  # loc = location
        spaces = ' ' in loc  # checks if there is spaces in given text - False = No Spaces
        if not spaces:
            await s.destructmsg("***Getting Weather Status for {}. This may take a while.***".format(loc), 15, self.bot)
            # seems to take around 15 seconds to find weather information

            weather_api = self.base_url + loc + self.a_url + self.key

            with aiohttp.ClientSession() as session:
                async with session.get(weather_api)as resp:
                    data = await resp.json()

                    temp = data["main"]["temp"]
                    brief = data["weather"][0]["main"]  # ie cloudy
                    desc = data["weather"][0]["description"]  # ie very cloudy/ overcast clouds and so on
                    name = data["name"]  # will return name without '_' and with capitalised words, saves effort
                    cloud = str(data["clouds"]["all"])
                    country = pycountry.countries.get(alpha2=data["sys"]["country"])

                    desc = capital_everything(desc)
                    cel = to_1dp(str(kel_to_cel(temp)))
                    fah = to_1dp(str(cel_to_fah(cel)))

                    await s.destructmsg("__**{}, {} - Weather Status**__\n"
                                        "**Temperature:** {}c  -  {}f\n"
                                        "**Weather:** {} - {}\n"
                                        "**Cloudiness:** {} percent".format(name, country.name, cel, fah,
                                                                            brief, desc, cloud), 50, self.bot)

        else:
            await s.destructmsg("**Error:** City cannot contains spaces, use underscores instead of spaces.\n"
                                "E.g. 'New_York' instead of 'New York'", 30, self.bot)


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
    result = (float(cels)*1.8) + 32
    return result


def capital_everything(string):
    """
    Takes a string, such as "hello world" and capitalizes each world
    returning "Hello World" in this example

    :param string:
    :return: The capitalized words in a string:
    """
    listy = string.split()  # () is same as " " apparently
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
