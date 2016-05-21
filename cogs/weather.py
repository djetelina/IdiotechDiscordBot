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

# Remove ones not being used once done


class Weather:
    def __init__(self, bot):
        self.bot = bot

        self.key = t.weather_key  # gets key from tokens.py
        self.base_url = "http://api.openweathermap.org/data/2.5/weather?q="  # base url (before query and key)
        self.a_url = "&appid="  # additional url (comes after query and before key)

    @commands.command(passcontext=True, description="Weather", brief="Weather")
    async def weather(self,  *, loc: str):  # loc = location
        spaces = ' ' in loc  # checks if there is spaces in given text - False = No Spaces
        # print(spaces)  # debug - remove
        if not spaces:
            await s.destructmsg("***Getting Weather Status for {}. This make take a while.***".format(loc), 15, self.bot)

            weather_api = self.base_url + loc + self.a_url + self.key
            # print(weather_api)

            with aiohttp.ClientSession() as session:
                async with session.get(weather_api)as resp:
                    data = await resp.json()
                    # print(data)
                    temp = data["main"]["temp"]
                    brief = data["weather"][0]["main"] # ie cloudy
                    desc = data["weather"][0]["description"]  # ie very cloud/ overcast clouds and so on
                    name = data["name"]  # will return name without '_' and with capitalised words, saves effort
                    cloud = str(data["clouds"]["all"])
                    country = pycountry.countries.get(alpha2=data["sys"]["country"])

                    cel = kel_to_cel(temp)
                    fah = cel_to_fah(cel)

                    await s.destructmsg("__**{}, {} - Weather Status**__\n"
                                        "**Temperature:** {}c  -  {}f\n"
                                        "**Weather:** {} - {}\n"
                                        "**Cloudiness:** {} percent".format(name, country.name, str(cel)[0:5], fah,
                                                                            brief, desc, cloud), 50, self.bot)

        else:
            await s.destructmsg("**Error:** City cannot contains spaces, use underscores instead of spaces.\n"
                                "E.g. 'New_York' instead of 'New York'", 30, self.bot)


def setup(bot):
    bot.add_cog(Weather(bot))


def kel_to_cel(kelvin):
    result = int(kelvin) - 273.15
    return result


def cel_to_fah(cel):
    result = (int(cel)*1.8) + 32
    return result


