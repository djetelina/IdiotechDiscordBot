import asyncio
import random
import time
import logging

import helpers.simplify as s
from helpers import descriptions as desc, settings

import calendar
from datetime import datetime

import aiohttp
from discord.ext import commands

import helpers.time_calculations as tc

# List with running game instances
games_list = []
loop = asyncio.get_event_loop()
log = logging.getLogger(__name__)


class Games:
    def __init__(self, bot):

        self.bot = bot

        # Dates have to be in relation to UTC (so if release is 5am BST, it would be 4am UTC)
        # Preferably use the latest release time for a game with different release times for different regions
        self.dates = {
            "No Man''s Sky": datetime(2016, 8, 12, 0, 0, 0),
            "Deus Ex: Mankind Divided": datetime(2016, 8, 23, 0, 0, 0),
            "Battlefield 1": datetime(2016, 10, 21, 0, 0, 0),
            "Civilization 6": datetime(2016, 10, 21, 0, 0, 0),
            "Dishonored 2": datetime(2016, 11, 11, 0, 0, 0),
            "Mirror''s Edge: Catalyst": datetime(2016, 6, 9, 0, 0, 0),
            "Mafia III": datetime(2016, 10, 7, 0, 0, 0),
            "Pokemon Sun and Moon": datetime(2016, 11, 23, 0, 0, 0),
            "World of Warcraft: Legion": datetime(2016, 8, 30, 0, 0, 0),
            "Mighty No. 9": datetime(2016, 6, 21, 0, 0, 0),
        }

    @commands.command(description=desc.steam_status, brief=desc.steam_status)
    async def steam(self):
        steam_api = 'http://is.steam.rip/api/v1/?request=SteamStatus'
        with aiohttp.ClientSession() as session:
            async with session.get(steam_api)as resp:
                data = await resp.json()
                if str(data["result"]["success"]) == "True":
                    login = (data["result"]["SteamStatus"]["services"]["SessionsLogon"]).capitalize()
                    community = (data["result"]["SteamStatus"]["services"]["SteamCommunity"]).capitalize()
                    economy = (data["result"]["SteamStatus"]["services"]["IEconItems"]).capitalize()
                    # leaderboards = (data["result"]["SteamStatus"]["services"]["LeaderBoards"]).capitalize()

                    reply = """**Steam Server Status**

```xl
Login          {}
Community      {}
Economy        {}```""".format(login, community, economy)

                else:
                    reply = "Failed connecting to API - Error: {}".format(data["result"]["error"])

        await self.bot.say(reply)

    @commands.command(pass_context=True, description=desc.release_dates, brief=desc.release_datesb)
    async def release(self, ctx):
            # We are using manual argument detection instead of @commands.group,
            # because we want sub-commands to be dynamic based on our self.dates dictionary
            for game in self.dates:
                maxlen = len(game)
            else:
                maxlen = 0
            arg = " ".join(ctx.message.content.split()[1:])

            if len(arg) > 0:
                found = False
                msg = "Found games starting with `{}`:\n\n```Ruby\n".format(arg.capitalize())
                for game in self.dates:
                    if game.lower().startswith(arg.lower()) or game.lower() is arg.lower():
                        days, hrs, mins = tc.calc_until(self.dates[game])
                        msg += "{}\n".format(tc.create_msg(game, days, hrs, mins, maxlen))
                        found = True

                if not found:
                    msg += ("No game in our release list found, that starts with {}".format(arg))

                msg += "```"

            else:
                msg = "**Release Dates List**\n\n```Ruby\n"
                for game, time in sorted(self.dates.items(), key=lambda x: x[1]):
                    days, hrs, mins = tc.calc_until(self.dates[game])
                    msg += "{}\n".format(tc.create_msg(game, days, hrs, mins, maxlen))
                msg += "```"

            await self.bot.say(msg)


def setup(bot):
    bot.add_cog(Games(bot))
