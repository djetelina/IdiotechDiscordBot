from discord.ext import commands
import simplify as s
import descriptions as desc
import aiohttp
from datetime import datetime
from pytz import timezone


class General:
    def __init__(self, bot):
        """
        Edit self.dates with releases we want to track
        """
        self.bot = bot
        self.dates = {
            "Overwatch": datetime(2016, 5, 24, 0, 0, 0),
            "Total War: Warhammer": datetime(2016, 5, 24, 0, 0, 0),
            "Hearts of Iron 4": datetime(2016, 6, 6, 0, 0, 0),
            "No Man's Sky": datetime(2016, 6, 21, 0, 0, 0),
            "Deus Ex: Mankind Divided": datetime(2016, 8, 23, 0, 0, 0),
            "Battlefield 1": datetime(2016, 10, 21, 0, 0, 0),
            "Civilization 6": datetime(2016, 10, 21, 0, 0, 0),
            "Dishonored 2": datetime(2016, 11, 11, 0, 0, 0),
            }

    @commands.command(description=desc.reddit, brief=desc.reddit)
    async def reddit(self):
        await s.destructmsg("https://www.reddit.com/r/idiotechgaming/", 20, self.bot)

    @commands.command(description=desc.github, brief=desc.github)
    async def github(self):
        await s.destructmsg("https://github.com/iScrE4m/IdiotechDiscordBot", 20, self.bot)

    @commands.command(description=desc.twitch, brief=desc.twitch)
    async def twitch(self):
        with aiohttp.ClientSession() as session:
            async with session.get('https://api.twitch.tv/kraken/streams?channel=idiotechgaming')as resp:
                data = await resp.json()
                if len(data["streams"]) > 0:
                    game = data["streams"][0]["game"]
                    views = data["streams"][0]["viewers"]

                    fmt = "%Y-%m-%dT%H:%M:%SZ"
                    hrs, mins, secs = dur_calc(datetime.strptime(data["streams"][0]["created_at"], fmt))

                    if views == 1:
                        peep = "person"
                    else:
                        peep = "people"

                    reply = "**Idiotech** is live streaming **{}** with **{}** {} watching! " \
                            "\nCurrent Uptime: {} hours, {} minutes and {} seconds." \
                            "\nhttps://www.twitch.tv/idiotechgaming".format(game, views, peep, hrs, mins, secs)
                else:
                    reply = "https://www.twitch.tv/idiotechgaming (OFFLINE)"
        await s.destructmsg(reply, 20, self.bot)

    @commands.command(description=desc.twitter, brief=desc.twitter)
    async def twitter(self):
        await s.destructmsg('https://twitter.com/idiotechgaming', 20, self.bot)

    @commands.command(description=desc.youtube, brief=desc.youtube)
    async def youtube(self):
        await s.destructmsg('https://www.youtube.com/c/idiotechgaming', 20, self.bot)

    @commands.command(description=desc.rules, brief=desc.rules)
    async def rules(self):
        await self.bot.say('Please read <#179965419728273408>')

    @commands.group(pass_context=True, description=desc.time, brief=desc.time)
    async def time(self, ctx):
        """
        Group for !time command, set subcommands by wrapping them in @time.command(name='subcommand_name)
        We use function get_time() to get all the times over the world.
        To add a city, edit get_time() and add it into dictionary
        """
        if ctx.invoked_subcommand is None:
            time = get_time()
            await s.destructmsg("**Sydney**: {} | **London**: {} | **New York**: {} | **San Francisco** {}".format(
                    time["sydney"], time["london"], time["ny"], time["sf"]), 30, self.bot)

    @time.command(name='advanced', description=desc.time_advanced, brief=desc.time_advanced)
    async def _advanced(self):
        time = get_time()
        # Sorry for readability, string too long
        await s.destructmsg(
            "**Sydney**: {} (UTC+10) | **London**: {} (UTC+1) "
            " | **New York**: {} (UTC-4) | **San Francisco** {} (UTC-7)".format(
                time["sydney"], time["london"], time["ny"], time["sf"]), 30, self.bot)

    @time.command(name='sydney', description=desc.time_sydney, brief=desc.time_sydney)
    async def _sydney(self):
        time = get_time()
        await s.destructmsg("**Sydney**: {} (UTC+10)".format(time["sydney"]), 30, self.bot)

    @time.command(name='london', description=desc.time_london, brief=desc.time_london)
    async def _london(self):
        time = get_time()
        await s.destructmsg("**London**: {} (UTC+1)".format(time["london"]), 30, self.bot)

    @time.command(name='ny', description=desc.time_ny, brief=desc.time_ny)
    async def _ny(self):
        time = get_time()
        await s.destructmsg("**New York**: {} (UTC-4)".format(time["ny"]), 30, self.bot)

    @time.command(name='sf', description=desc.time_sf, brief=desc.time_sf)
    async def _sf(self):
        time = get_time()
        await s.destructmsg("**San Francisco**: {} (UTC-7)".format(time["sf"]), 30, self.bot)

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
                    leaderboards = (data["result"]["SteamStatus"]["services"]["LeaderBoards"]).capitalize()

                    reply = """__**Steam Status**__

                    **Login servers:** {}
                    **Community servers:** {}
                    **Economy servers:** {}""".format(login, community, economy)

                else:
                    reply = "Failed connecting to API - Error: {}".format(data["result"]["error"])

        await s.destructmsg(reply, 30, self.bot)

    @commands.command(pass_context=True, description=desc.release_dates, brief=desc.release_datesb)
    async def release(self, ctx):
        """
        We are using manual argument detection instead of @commands.group,
        because we want subcommands to be dynamic based on our self.dates dictionary
        """
        arg = " ".join(ctx.message.content.split()[1:])
        if len(arg) > 0:
            for game in self.dates:
                if game.lower().startswith(arg):
                    days, hrs, mins = rd_calc(self.dates[game])
                    msg = "{} releases in {},{} hours and {} minutes.".format(game, days, hrs, mins)
                    await s.destructmsg(msg, 30, self.bot)
                    break
            else:
                await s.destructmsg("No game in our release list found, that starts with {}".format(arg), 30, self.bot)
        else:
            msg = "Release Dates List - Times, Dates and Games are subject to change\n"

            for game, time in sorted(self.dates.items(), key=lambda x: x[1]):
                days, hrs, mins = rd_calc(self.dates[game])
                msg += "\n{} releases in {},{} hours and {} minutes.".format(game, days, hrs, mins)

            await s.destructmsg("```{}```".format(msg), 30, self.bot)


def rd_calc(rd):
    """
    Calculator for release dates

    :param rd:  datetime()
    :return:    three strings with time left
    """

    tdelta = rd - datetime.utcnow()
    tstr = str(tdelta)

    days, notdays = tstr.split(",")
    hrs, mins, secs = notdays.split(":")

    return days, hrs, mins


def dur_calc(rd):
    """
    Calculator for duration of time streaming

    :param rd:  Timestamp of stream start from twitch API
    :return:    three strings with time passed
    """

    tdelta = datetime.utcnow() - rd
    tstr = str(tdelta)

    hrs, mins, secs = tstr.split(":")
    secs = secs.split(".")[0]

    return hrs, mins, secs


def get_time() -> dict:
    """
    Function to get local time in cities

    :return: Dictionary with {"city":"%H:%M"}
    """
    fmt = '%H:%M'

    now_utc = datetime.now(timezone('UTC'))

    now_pacific = now_utc.astimezone(timezone('US/Pacific'))
    sf = now_pacific.strftime(fmt)

    now_london = now_utc.astimezone(timezone('Europe/London'))
    london = now_london.strftime(fmt)

    now_sydney = now_utc.astimezone(timezone('Australia/Sydney'))
    sydney = now_sydney.strftime(fmt)

    now_ny = now_utc.astimezone(timezone('US/Eastern'))
    ny = now_ny.strftime(fmt)

    return {
        "sydney": sydney,
        "london": london,
        "ny": ny,
        "sf": sf
    }


def setup(bot):
    bot.add_cog(General(bot))
