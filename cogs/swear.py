from discord.ext import commands
from datetime import datetime
import pytz
import discord
import asyncio
import aiohttp


import random
import simplify as s
# from main import bot as b


class Swear:
    def __init__(self, bot):
        """
        Here is where I should probably explain what this stuff does
        """
        self.bot = bot
        self.greylist = ["fuck", "shit", "cunt"]
        self.blacklist = ["nigga", "nigger", "kys", "fuck you", "fuck u"]
        self.warnings = ["Please don't swear!", "Don't swear, thanks!"]
        self.ignore = "<@181177004085739520>"

    """
    TO DO
    -----
    Add counting system to black list, on third trigger send message to idiotech via #admin
    ^^ potentially scrap that idea
    """

    async def on_message(self, message):
        print("message recieved")
        print(message.content)
        if message.author.id is not self.ignore:
            print("author id is not bots")
            for i in self.greylist:
                print("greylist checking: "+i)
                if i in message.content:
                    print("checked and found "+i+" from greylist")
                    await s.whisper(message.author, random.choice(self.warnings), self.bot)
                    break

            for j in self.blacklist:
                print("blacklist checking: "+j)
                if j in message.content:
                    print("blacklist triggered")
                    # admin = message.server.get_channel("176304607172100097") # for idiotech server
                    admin = message.server.get_channel("181233418099490826")  # for test server
                    customWarn = message.author.name + " sent a blacklisted phrase '" + j + "' in " \
                        + message.channel.name

                    await self.bot.send_message(admin, customWarn)


def setup(bot):
    bot.add_cog(Swear(bot))
    Swear.on_message = bot.event(Swear.on_message)
