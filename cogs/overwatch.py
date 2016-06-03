from discord.ext import commands
import descriptions as desc
import bs4
import requests
import asyncio


class Overwatch:
    def __init__(self, bot):
        """
        Edit self.dates with releases we want to track
        """
        self.bot = bot

    @commands.command(description=desc.ow, brief=desc.owb)
    async def overwatch(self, region: str, battletag: str):
        msg = await self.bot.say("Fetching Stats for {}".format(battletag))

        user = battletag.replace("#", "-")

        reg_eu = ["eu", "euro", "europe"]
        reg_us = ["australia", "aussie", "aus", "us", "usa", "na", "america", "au"]
        reg_kr = ["asia", "korea", "kr", "as", "china", "japan"]

        if region.lower() in reg_eu:
            reg = "eu"
        elif region.lower() in reg_us:
            reg = "us"
        elif region.lower() in reg_kr:
            reg = "kr"
        else:
            self.bot.edit_message(msg, "Unknown region: {}".format(region))
            return

        loop = asyncio.get_event_loop()
        future = loop.run_in_executor(
            None, requests.get, "https://playoverwatch.com/en-us/career/pc/{}/{}".format(reg, user))
        res = await future

        try:
            res.raise_for_status()
        except Exception as e:
            await self.bot.edit_message(msg, "**Error with request. Please check for mistakes before trying again.**"
                                             ".\nError: "+str(e))
            return

        doc = bs4.BeautifulSoup(res.text, "html.parser")
        page = doc.select('div')
        most_played = page[82].select('div')[2].getText()
        most_games = page[82].select('div')[3].getText()
        game_swon = int(page[1111].select('div')[0].select('td')[1].getText())
        games_played = int(page[1111].select('div')[0].select('td')[3].getText())
        time_played = page[1111].select('div')[0].select('td')[11].getText()
        games_lost = games_played - game_swon
        won_lost = "{}/{}".format(game_swon, games_lost)

        await self.bot.edit_message(msg, "**Overwatch Stats for {} - {}**\n\n"
                                         "Time Played:              *{}*\n"
                                         "Total Games:             *{}*\n"
                                         "Games Won/Lost:   *{}*\n"
                                         "Most Played Hero:   *{}, {} played*"
                                         "".format(battletag, reg.upper(), time_played, games_played,
                                                   won_lost, most_played, most_games))


def setup(bot):
    bot.add_cog(Overwatch(bot))

