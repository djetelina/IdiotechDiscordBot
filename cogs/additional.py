from discord.ext import commands
import simplify as s
import descriptions as desc
import aiohttp
from datetime import datetime
from pytz import timezone
import tokens as t
import calendar
import bs4
import requests

class Stuff:
    def __init__(self, bot):
        """
        Edit self.dates with releases we want to track
        """
        self.bot = bot

    @commands.command(pass_context=True, description=desc.ow, brief=desc.owb)
    async def overwatch(self, ctx):
        # https://automatetheboringstuff.com/chapter11/

        ok = True
        inp = ctx.message.content.split(" ")

        try:
            test = inp[2]  # If there is no second input this should cause an index error
        except IndexError:
            ok = False
            await self.bot.say("**Error:** Missing an argument. Make sure you specified the region "
                               "and user to check for. \nSyntax: !overwatch <region> <battletag>")
            return

        if inp[1] == "qt":
            inp = ["quick test", "eu", "ExtraRandom#2501"]

        msg = await self.bot.say("Fetching Stats for {}".format(inp[2]))

        reg_eu = {"eu", "euro", "europe"}
        reg_us = {"australia", "aussie", "aus", "us", "usa", "na", "america"}
        reg_kr = {"asia", "korea", "kr", "as", "china", "japan"}

        check = inp[1].lower()

        if check in reg_eu:
            reg = "eu"
        elif check in reg_us:
            reg = "us"
        elif check in reg_kr:
            reg = "kr"
        else:
            reg = "ERROR"
            ok = False
            # self.bot.edit_message(msg, "Wrong region")
            return

        user = inp[2].replace("#", "-")
        url = "https://playoverwatch.com/en-us/career/"
        plat = "pc"  # If there is a demand for other platforms we can add that later
        profile = url + plat + "/" + reg + "/" + user

        res = requests.get(profile)

        try:
            res.raise_for_status()
        except Exception as exc:
            await self.bot.edit_message(msg, "**Error with request. Please check for mistakes before trying again.**"
                                             ".\nError: "+str(exc))
            ok = False

        if ok:
            doc = bs4.BeautifulSoup(res.text, "html.parser")  # BeautifulSoup = Best name ever lol
            page = doc.select('div')

            # print(page[1109].select('div')[0].select('td'))
            mostplayed = page[82].select('div')[2].getText()
            mostgames = page[82].select('div')[3].getText()
            gameswon = int(page[1111].select('div')[0].select('td')[1].getText())
            gamesplayed = int(page[1111].select('div')[0].select('td')[3].getText())
            timeplayed = page[1111].select('div')[0].select('td')[11].getText()
            gameslost = gamesplayed - gameswon
            wonlost = "{}/{}".format(gameswon, gameslost)

            await self.bot.edit_message(msg, "**Overwatch Stats for {} - {}**\n\n"
                                             "Time Played:              *{}*\n"
                                             "Total Games:             *{}*\n"
                                             "Games Won/Lost:   *{}*\n"
                                             "Most Played Hero:   *{}, {} played*"
                                             "".format(inp[2], reg.upper(), timeplayed, gamesplayed,
                                                       wonlost, mostplayed, mostgames))


def setup(bot):
    bot.add_cog(Stuff(bot))

