import calendar
from datetime import datetime

import aiohttp
from discord.ext import commands
from pytz import timezone

import helpers.tokens as t
from helpers import descriptions as desc


class General:
    def __init__(self, bot):
        """
        Edit self.dates with releases we want to track
        """
        self.bot = bot

        # Dates have to be in relation to UTC (so if release is 5am BST, it would be 4am UTC)
        self.dates = {
            "Hearts of Iron 4": datetime(2016, 6, 6, 0, 0, 0),
            "No Man''s Sky": datetime(2016, 8, 12, 0, 0, 0),
            "Deus Ex: Mankind Divided": datetime(2016, 8, 23, 0, 0, 0),
            "Battlefield 1": datetime(2016, 10, 21, 0, 0, 0),
            "Civilization 6": datetime(2016, 10, 21, 0, 0, 0),
            "Dishonored 2": datetime(2016, 11, 11, 0, 0, 0),
            "Mirror''s Edge: Catalyst": datetime(2016, 6, 9, 0, 0, 0),
            "Mafia III": datetime(2016, 10, 7, 0, 0, 0),
            "Pokemon Sun and Moon": datetime(2016, 11, 23, 0, 0, 0),
        }

    @commands.command(description=desc.reddit, brief=desc.reddit)
    async def reddit(self):  # returns link to sub-reddit
        await self.bot.say("https://www.reddit.com/r/idiotechgaming/")

    @commands.command(description=desc.github, brief=desc.github)
    async def github(self):  # returns link to github for this bot
        await self.bot.say("You can request features, contribute and report issues with the bot here:"
                           "\nhttps://github.com/iScrE4m/IdiotechDiscordBot")

    @commands.command(description=desc.twitch, brief=desc.twitchb)
    async def twitch(self):
        with aiohttp.ClientSession() as session:
            async with session.get('https://api.twitch.tv/kraken/streams?channel=idiotechgaming')as resp:
                data = await resp.json()
                if len(data["streams"]) > 0:
                    game = data["streams"][0]["game"]
                    views = data["streams"][0]["viewers"]

                    fmt = "%Y-%m-%dT%H:%M:%SZ"
                    hrs, mins, secs = calc_duration(datetime.strptime(data["streams"][0]["created_at"], fmt))

                    # if one person is watching return 'person' instead of people
                    if views == 1:
                        peep = "person"
                    else:
                        peep = "people"

                    reply = "**Idiotech** is live streaming **{}** with **{}** {} watching! " \
                            "\nCurrent Uptime: {} hours, {} minutes and {} seconds." \
                            "\nhttps://www.twitch.tv/idiotechgaming".format(game, views, peep, hrs, mins, secs)
                else:
                    reply = "https://www.twitch.tv/idiotechgaming (OFFLINE)"
        await self.bot.say(reply)

    @commands.command(description=desc.twitter, brief=desc.twitter)
    async def twitter(self):  # returns link to Idiotech's twitter
        await self.bot.say('https://twitter.com/idiotechgaming')

    @commands.command(description=desc.fb, brief=desc.fb)
    async def facebook(self):  # finds latest facebbok post and returns it, along with link to page
        with aiohttp.ClientSession() as session:
            async with session.get('https://graph.facebook.com/v2.6/idiotechgaming/posts'
                                   '?access_token={}'.format(t.fb_key)) as resp:
                data = await resp.json()

                fb_post = data["data"][0]["message"]
                y, m, d, = date_split(data["data"][0]["created_time"])  # y = year, m = month, d = day

                # TODO Make date ago
                msg = """**Latest Facebook Post**
```{4}```
{0}{1} of {2}, {3}

https://www.facebook.com/idiotechgaming/""".format(d, get_date_suf(d), calendar.month_name[int(m)], y, fb_post)
                await self.bot.say(msg)

    @commands.command(description=desc.youtube, brief=desc.youtube)
    async def youtube(self):
        connector = aiohttp.TCPConnector(verify_ssl=False)

        with aiohttp.ClientSession(connector=connector) as session:
            async with session.get('https://www.googleapis.com/youtube/v3/search?part=snippet&channelId=UC0YagOInbZx'
                                   'j10gaWwb1Nag&maxResults=1&order=date&key={}'.format(t.yt_key)) as resp:
                data = await resp.json()

                mo = "**"
                title = "{0}Latest Upload:{0} {1}".format(mo, data["items"][0]["snippet"]["title"])

                uploaded = data["items"][0]["snippet"]["publishedAt"]
                date = str(uploaded).split('T')[0]

                year, month, day = date.split('-')
                month = calendar.month_name[int(month)]

                # TODO Make Uploaded in ago format
                uploaded = "{0} the {1}{2}, {3}".format(month, day, get_date_suf(day), year)
                link = "https://youtu.be/{}".format(data["items"][0]["id"]["videoId"])

                await self.bot.say("{}\n{}\n\n{}".format(title, uploaded, link))

    @commands.command(description=desc.rules, brief=desc.rules)
    async def rules(self):
        # TODO Get from settings
        await self.bot.say('Please read <#179965419728273408>')

    @commands.group(pass_context=True, description=desc.time, brief=desc.time)
    async def time(self, ctx):
        # Group for !time command, set subcommands by wrapping them in @time.command(name='subcommand_name)
        # We use function get_time() to get all the times over the world.
        # To add a city, edit get_time() and add it into dictionary

        if ctx.invoked_subcommand is None:
            time = get_time()
            await self.bot.say("**San Francisco**: {} | **New York**: {} | **London**: {} | **Sydney** {}".format(
                time["sf"], time["ny"], time["london"], time["sydney"]))

        # TODO Squish timezones into one command (here)

    @time.command(name='advanced', description=desc.time_advanced, brief=desc.time_advanced)
    async def _advanced(self):
        time = get_time()
        await self.bot.say(
            "**San Francisco** {} (UTC-7) "
            "| **New York**: {} (UTC-4) "
            "| **London**: {} (UTC+1) "
            "| **Sydney**: {} (UTC+10) "
            "".format(time["sf"], time["ny"], time["london"], time["sydney"]))

    @time.command(name='sydney', description=desc.time_sydney, brief=desc.time_sydney)
    async def _sydney(self):
        time = get_time()
        await self.bot.say("**Sydney**: {} (UTC+10)".format(time["sydney"]))

    @time.command(name='london', description=desc.time_london, brief=desc.time_london)
    async def _london(self):
        time = get_time()
        await self.bot.say("**London**: {} (UTC+1)".format(time["london"]))

    @time.command(name='ny', description=desc.time_ny, brief=desc.time_ny)
    async def _ny(self):
        time = get_time()
        await self.bot.say("**New York**: {} (UTC-4)".format(time["ny"]))

    @time.command(name='sf', description=desc.time_sf, brief=desc.time_sf)
    async def _sf(self):
        time = get_time()
        await self.bot.say("**San Francisco**: {} (UTC-7)".format(time["sf"]))

    @time.command(name='perth', description=desc.time_perth, brief=desc.time_perth)
    async def _perth(self):
        time = get_time()
        await self.bot.say("**Perth**: {} (UTC+8)".format(time["perth"]))

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

```Login          {}
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
                    days, hrs, mins = calc_until(self.dates[game])
                    msg += "{}\n".format(create_msg(game, days, hrs, mins, maxlen))
                    found = True

            if not found:
                msg += ("No game in our release list found, that starts with {}".format(arg))

            msg += "```"

        else:
            msg = "**Release Dates List**\n\n```Ruby\n"
            for game, time in sorted(self.dates.items(), key=lambda x: x[1]):
                days, hrs, mins = calc_until(self.dates[game])
                msg += "{}\n".format(create_msg(game, days, hrs, mins, maxlen))
            msg += "```"

        await self.bot.say(msg)


def create_msg(game, days, hrs, mins, maxlen):
    spaces = maxlen - len(game) + 30
    for _ in range(spaces):
        game = game + " "
    if int_day(days) < 0:  # if hours is a minus (i.e. game is released)
        msg = "{} is out now!".format(game)
    elif int_day(days) == 0 and int(hrs) == 0 and int(mins) == 0:
        msg = "{} releases within the next 60 seconds, HYPE!!!".format(game)
    else:
        msg = "{} {}, {} hours {} minutes".format(game, days, hrs, mins)

    return msg


def int_day(day):
    """
    Takes day as string ('3 days') and returns just the number as an integer
    :param day:
    :return:
    """
    day, word = day.split(" ")
    return int(day)


def get_date_suf(day):
    # Get the suffix to add to date ('st' for 1, 'nd' for 2 and so on) code from http://stackoverflow.com/a/5891598
    if 4 <= int(day) <= 20 or 24 <= int(day) <= 30:
        suffix = "th"
    else:
        suffix = ["st", "nd", "rd"][int(day) % 10 - 1]
    return suffix


def date_split(date):
    """
    Returns the given datetime as three strings: year, month and day

    :param date: The datetime to split into year, month and day
    :return: year, month, day
    """

    to_split = str(date).split('T')[0]
    year, month, day = to_split.split('-')

    return year, month, day


def date_now():
    """
    Returns the date now as three strings: year, month and day

    :return: year, month, day
    """

    now = datetime.utcnow()
    date, time = str(now).split(' ')
    year, month, day = date.split('-')

    return year, month, day


def calc_until(rd):
    """
    Calculates the amount of time between now and 'rd'

    :param rd:  release date as datetime()
    :return:    three strings with time left
    """

    t_delta = rd - datetime.utcnow()
    t_str = str(t_delta)

    test_var = t_str.split(".")[0]
    if len(test_var) == 7 or len(test_var) == 8:
        days = "0 days"
        hrs, minutes, secs = test_var.split(":")
    elif len(test_var) == 5 or len(test_var) == 4:
        days = "0 days"
        hrs = "0"
        minutes, secs = test_var.split(":")
    elif len(test_var) == 1 or len(test_var) == 2:
        days = "0 days"
        hrs = "0"
        minutes = "0"
    else:
        days, time = t_str.split(",")
        hrs, minutes, secs = time.split(":")

    hrs = hrs.strip()  # removes spaces in string

    return days, hrs, minutes


def calc_duration(start):
    """
    Calculates the amount of time between 'start' and now

    :param start:  Datetime
    :return:    three strings with time passed
    """

    tdelta = datetime.utcnow() - start
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

    now_perth = now_utc.astimezone(timezone('Australia/Perth'))
    perth = now_perth.strftime(fmt)

    now_ny = now_utc.astimezone(timezone('US/Eastern'))
    ny = now_ny.strftime(fmt)

    return {
        "sydney": sydney,
        "london": london,
        "ny": ny,
        "sf": sf,
        "perth": perth
    }


def setup(bot):
    bot.add_cog(General(bot))
