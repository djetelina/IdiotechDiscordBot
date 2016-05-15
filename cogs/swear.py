from discord.ext import commands
from datetime import datetime
import pytz
import discord
import asyncio
import aiohttp

import random
import simplify as s
from main import bot as b


class Swear:
    def __init__(self, bot):
        """
        Here is where I should probably explain what this stuff does
        """
        self.bot = bot
        self.greylist = ["fuck", "shit", "cunt"]
        self.blacklist = ["nigga", "nigger", "kys", "fuck you", "fuck u"]
        self.warnings = ["Please don't swear!", "Don't swear, thanks!"]
        self.ignore = 181177004085739520
    """
    @bot.event
    async def on_ready(self):
        print('Logged in as')
        print(bot.user.name)
        print(bot.user.id)
        print('------')
    """

    # loop = asyncio.get_event_loop()

    """
    TO DO
    -----
    Add counting system to black list, on third trigger send message to idiotech via #admin

    """

    # @b.event  # broken
    # async def on_message(self, message):
    async def msg(self, message):
        # if message.author.name != self.ignore:
            for i in self.greylist:
                if i in message.content:
                    await s.whisper(message.author, random.choice(self.warnings))
                    break

            for j in self.blacklist:
                if j in message.content:
                    # admin = message.server.get_channel("176304607172100097") # for idiotech server
                    admin = message.server.get_channel("181233418099490826")  # for test server
                    customWarn = str(message.author) + " sent a blacklisted phrase '" + j + "' in " \
                        + str(message.channel)

                    await b.send_message(admin, customWarn)

    """
    class Warns:
        def __init__(self):


        # self


        def init(self, user):
    """


def setup(bot):
    bot.add_cog(Swear(bot))

    Swear.msg = bot.event(Swear.msg)
