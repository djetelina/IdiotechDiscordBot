import asyncio
import logging

import bs4
import requests
from discord.ext import commands

from helpers import descriptions as desc

log = logging.getLogger(__name__)


class Overwatch:
    def __init__(self, bot):
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
                                             ".\nError: {}".format(str(e)))
            log.exception("Error with request")
            return

        doc = bs4.BeautifulSoup(res.text, "html.parser")
        page = doc.select('div')

        most_played = page[82].select('div')[2].getText()
        most_games = page[82].select('div')[3].getText()

        stats = doc.find_all('td')
        # print(stats)

        games_won = find_value(stats, "Games Won")
        games_played = find_value(stats, "Games Played")
        time_played = find_value(stats, "Time Played")

        games_lost = int(games_played) - int(games_won)
        won_lost = "{}/{}".format(games_won, games_lost)

        win_percent = round(((games_won / games_played) * 100), 1)

        await self.bot.edit_message(msg, "**Overwatch Stats for {0} - {1}**\n\n"
                                         "Time Played:              *{2}*\n"
                                         "Total Games:             *{3}*\n"
                                         "Games Won/Lost:   *{4}* ({7}% win rate)\n"
                                         "Most Played Hero:   *{5}, {6} played*"
                                         "".format(battletag, reg.upper(), time_played, games_played,
                                                   won_lost, most_played, most_games, win_percent))


def find_value(stats, name):
    """
    :param stats: stats list
    :param name: name of value to find (i.e. Games Won)
    :return: largest value for name (there are multiple game won's but the biggest will be the overall games won
    rather than a character specific games won
    """

    tagged_name = "<td>{}</td>".format(name)

    things = []
    is_time = False

    hour = []
    mins = []

    for item in stats:
        if name == "Time Played":
            is_time = True

            if str(item) == tagged_name:
                time = item.next_sibling.getText().split()
                if time[1] == "minutes" or time[1] == "minute":
                    mins.append(int(time[0]))
                elif time[1] == "hours" or time[1] == "hour":  # needed instead of else as it can also be in seconds
                    hour.append(int(time[0]))

        elif str(item) == tagged_name:
            things.append(int(item.next_sibling.getText()))

    if is_time:
        if not hour:
            # meaning max play time is in minutes
            return "{} minutes".format(max(mins))
            # doesnt accommodate for 1 min playtime but seriously why would you even have that short a play time

        elif hour:
            max_time = max(hour)
            sfx = "hours"
            if max_time == 1:
                sfx = "hour"
            return "{} {}".format(max_time, sfx)

    return max(things)


def setup(bot):
    bot.add_cog(Overwatch(bot))
