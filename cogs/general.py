import calendar
from datetime import datetime

import aiohttp
from discord.ext import commands
from pytz import timezone

import helpers.tokens as t
from helpers import descriptions as desc, time_calculations as tc


class General:
    def __init__(self, bot):
        """
        Edit self.dates with releases we want to track
        """
        self.bot = bot

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
                    hrs, mins, secs = tc.calc_duration(datetime.strptime(data["streams"][0]["created_at"], fmt))

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
                y, m, d, = tc.date_split(data["data"][0]["created_time"])  # y = year, m = month, d = day

                # TODO Make date ago
                msg = """**Latest Facebook Post**
```{4}```
{0}{1} of {2}, {3}

https://www.facebook.com/idiotechgaming/""".format(d, tc.get_date_suf(d), calendar.month_name[int(m)], y, fb_post)
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
                uploaded = "{0} the {1}{2}, {3}".format(month, day, tc.get_date_suf(day), year)
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


def get_time() -> dict:
    """
   Function to get local time in cities
   :return: Dictionary with {"city":"%H:%M"}
   """
    places = {'sf': 'US/Pacific', 'london': 'Europe/London', 'sydney': 'Australia/Sydney', 'perth': 'Australia/Perth', 'ny': 'US/Eastern'}
    output = {}
    now_utc = datetime.now(timezone('UTC'))
 
    for i in places:
        time = now_utc.astimezone(timezone(places[i]))
        fmttime = time.strftime('%H:%M')
        output[i] = fmttime
 
    return output


def setup(bot):
    bot.add_cog(General(bot))
