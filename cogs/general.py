from discord.ext import commands
import simplify as s
import descriptions as desc
import aiohttp
from datetime import datetime
from pytz import timezone
import tokens as t
import calendar


class General:
    def __init__(self, bot):
        """
        Edit self.dates with releases we want to track
        """
        self.bot = bot

        # Dates have to be in relation to UTC (so if release is 5am BST, it would be 4am UTC)
        self.dates = {
            "Overwatch": datetime(2016, 5, 23, 23, 0, 0),  # launches 12:00am bst, -1 because its in UTC time
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

    @commands.command(description=desc.fb, brief=desc.fb)
    async def facebook(self):
        with aiohttp.ClientSession() as session:
            async with session.get('https://graph.facebook.com/v2.6/idiotechgaming/posts'
                                   '?access_token={}'.format(t.fb_key)) as resp:
                data = await resp.json()

                msg1 = data["data"][0]["message"]
                y, m, d, = date_split(data["data"][0]["created_time"])  # y = year, m = month, d = day

                msg = "**Latest Facebook Post**\n" \
                    "**Posted:** {}{} of {}, {}.\n\n" \
                    "```{}```"  \
                    "https://www.facebook.com/idiotechgaming/" \
                    "".format(d, get_date_suf(d), calendar.month_name[int(m)], y, msg1)

                await s.destructmsg(msg, 30, self.bot)

    @commands.command(description=desc.youtube, brief=desc.youtube)
    async def youtube(self):
        connector = aiohttp.TCPConnector(verify_ssl=False)

        with aiohttp.ClientSession(connector=connector) as session:
            async with session.get('https://www.googleapis.com/youtube/v3/search?part=snippet&channelId=UC0YagOInbZx'
                                   'j10gaWwb1Nag&maxResults=1&order=date&key={}'.format(t.yt_key)) as resp:
                data = await resp.json()
                # channel = "https://www.youtube.com/c/idiotechgaming"

                mo = "**"  # Modifier (e.g. * for italic, ** for bold, __ for underline and so on)
                title = mo + "Latest Upload: " + mo\
                        + data["items"][0]["snippet"]["title"]  # [::-1]  # msg + vid title, [::-1] reverses str
                uploaded = data["items"][0]["snippet"]["publishedAt"]  # datetime video was uploaded
                date = str(uploaded).split('T')[0]  # just the date of upload

                year, month, day = date.split('-')
                month = calendar.month_name[int(month)]  # takes month number and returns word form (i.e. 05 = may)

                uploaded = mo + "Uploaded: " + mo + "{} the {}{}, {}.".format(month, day, get_date_suf(day), year)
                link = "https://youtu.be/" + data["items"][0]["id"]["videoId"]
                # uses ``` to stop video from being embed

                await s.destructmsg(title + "\n" + uploaded + "\n\n"+link, 30, self.bot)

    @commands.command(description=desc.rules, brief=desc.rules)
    async def rules(self):
        await self.bot.say('Please read <#179965419728273408>')

    @commands.group(pass_context=True, description=desc.time, brief=desc.time)
    async def time(self, ctx):
        # Group for !time command, set subcommands by wrapping them in @time.command(name='subcommand_name)
        # We use function get_time() to get all the times over the world.
        # To add a city, edit get_time() and add it into dictionary

        if ctx.invoked_subcommand is None:
            time = get_time()
            await s.destructmsg("**San Francisco**: {} | **New York**: {} | **London**: {} | **Sydney** {}".format(
                    time["sf"], time["ny"], time["london"], time["sydney"]), 30, self.bot)

    @time.command(name='advanced', description=desc.time_advanced, brief=desc.time_advanced)
    async def _advanced(self):
        time = get_time()
        await s.destructmsg(
            "**San Francisco** {} (UTC-7) "
            "| **New York**: {} (UTC-4) "
            "| **London**: {} (UTC+1) "
            "| **Sydney**: {} (UTC+10) "
            "".format(time["sf"], time["ny"], time["london"], time["sydney"]), 30, self.bot)

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

    @time.command(name='perth', description=desc.time_perth, brief=desc.time_perth)
    async def _perth(self):
        time = get_time()
        await s.destructmsg("**Perth**: {} (UTC+8)".format(time["perth"]), 30, self.bot)

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

                    reply = """__**Steam Status**__

                    **Login servers:** {}
                    **Community servers:** {}
                    **Economy servers:** {}""".format(login, community, economy)

                else:
                    reply = "Failed connecting to API - Error: {}".format(data["result"]["error"])

        await s.destructmsg(reply, 30, self.bot)

    @commands.command(pass_context=True, description=desc.release_dates, brief=desc.release_datesb)
    async def release(self, ctx):
        # We are using manual argument detection instead of @commands.group,
        # because we want subcommands to be dynamic based on our self.dates dictionary

        arg = " ".join(ctx.message.content.split()[1:])
        if len(arg) > 0:
            for game in self.dates:
                if game.lower().startswith(arg.lower()) or game.lower() is arg.lower():
                    days, hrs, mins = calc_until(self.dates[game])
                    msg = "{} releases in {},{} hours and {} minutes.".format(game, days, hrs, mins)
                    await s.destructmsg(msg, 30, self.bot)

                    break
            else:
                await s.destructmsg("No game in our release list found, that starts with {}".format(arg), 30, self.bot)
        else:
            msg = "Release Dates List - Times, Dates and Games are subject to change\n"

            for game, time in sorted(self.dates.items(), key=lambda x: x[1]):
                days, hrs, mins = calc_until(self.dates[game])
                msg += "\n{} releases in {},{} hours and {} minutes.".format(game, days, hrs, mins)

            await s.destructmsg("```{}```".format(msg), 30, self.bot)


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

    tdelta = rd - datetime.utcnow()
    tstr = str(tdelta)

    days, notdays = tstr.split(",")
    hrs, mins, secs = notdays.split(":")

    return days, hrs, mins


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
