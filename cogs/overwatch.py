import asyncio
import logging

import bs4
import requests
from discord.ext import commands

from helpers import descriptions as desc

log = logging.getLogger(__name__)

class Overwatch:
    def __init__(self, bot):
        """
        Edit self.dates with releases we want to track
        """
        self.bot = bot

    @commands.command(description=desc.ow, brief=desc.owb)
    async def overwatch(self, region: str, battletag: str):
        games_played = 0
        games_won = 0
        time_played = 0
        count = 0
        stat_count = 0

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
            log.exception("Error with request")
            return

        doc = bs4.BeautifulSoup(res.text, "html.parser")
        page = doc.select('div')

        # eof = len(page) - 1   # eof = end of file - left in as you could use it for the for loop "stuff in page" maybe

        most_played = page[82].select('div')[2].getText()
        most_games = page[82].select('div')[3].getText()

        for stuff in page:
            try:
                if str(page[count].select('div')[0].select('td')[0].getText()) == "Games Won":
                    try:
                        stats = page[count].select('div')[0].select('td')

                        for stat in stats:
                            if stats[stat_count].getText() == "Games Won":
                                games_won = int(stats[stat_count + 1].getText())
                            if stats[stat_count].getText() == "Games Played":
                                games_played = int(stats[stat_count + 1].getText())
                            elif stats[stat_count].getText() == "Time Played":
                                time_played = stats[stat_count + 1].getText()
                            stat_count += 1

                    except Exception as e:
                        log.exception("Parsing HTML")

            except Exception:
                pass  # This will print a lot of errors if we log it

            count += 1

        games_lost = int(games_played) - int(games_won)
        won_lost = "{}/{}".format(games_won, games_lost)

        await self.bot.edit_message(msg, "**Overwatch Stats for {} - {}**\n\n"
                                         "Time Played:              *{}*\n"
                                         "Total Games:             *{}*\n"
                                         "Games Won/Lost:   *{}*\n"
                                         "Most Played Hero:   *{}, {} played*"
                                         "".format(battletag, reg.upper(), time_played, games_played,
                                                   won_lost, most_played, most_games))


def setup(bot):
    bot.add_cog(Overwatch(bot))
