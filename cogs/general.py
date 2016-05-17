from discord.ext import commands
import simplify as s
import descriptions as desc
import pytz
import aiohttp
from datetime import datetime


class General:
    def __init__(self, bot):
        self.bot = bot

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
                    reply = "Idiotech is live streaming {}! https://www.twitch.tv/idiotechgaming".format(game)
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
            "**Sydney**: {} (GMT+10) | **London**: {} (GMT+1) "
            " | **New York**: {} (GMT-4) | **San Francisco** {} (GMT-7)".format(
                time["sydney"], time["london"], time["ny"], time["sf"]), 30, self.bot)

    @time.command(name='sydney', description=desc.time_sydney, brief=desc.time_sydney)
    async def _sydney(self):
        time = get_time()
        await s.destructmsg("**Sydney**: {} (GMT+10)".format(time["sydney"]), 30, self.bot)

    @time.command(name='london', description=desc.time_london, brief=desc.time_london)
    async def _london(self):
        time = get_time()
        await s.destructmsg("**London**: {} (GMT+1)".format(time["london"]), 30, self.bot)

    @time.command(name='ny', description=desc.time_ny, brief=desc.time_ny)
    async def _ny(self):
        time = get_time()
        await s.destructmsg("**New York**: {} (GMT-4)".format(time["ny"]), 30, self.bot)

    @time.command(name='sf', description=desc.time_sf, brief=desc.time_sf)
    async def _sf(self):
        time = get_time()
        await s.destructmsg("**San Francisco**: {} (GMT-7)".format(time["sf"]), 30, self.bot)

    @commands.command(description=desc.rd, brief=desc.rd)
    async def rd(self):
        ow_rd = datetime(2016, 5, 24, 0, 0, 0)
        bf_rd = datetime(2016, 10, 21, 0, 0, 0)
        nms_rd = datetime(2016, 6, 21, 0, 0, 0)
        d2_rd = datetime(2016, 11, 11, 0, 0, 0)

        ow_days, ow_hrs, ow_mins = rd_calc(ow_rd)
        bf_days, bf_hrs, bf_mins = rd_calc(bf_rd)  # BF1 and Civ6 have the same release date
        nms_days, nms_hrs, nms_mins = rd_calc(nms_rd)
        d2_days, d2_hrs, d2_mins = rd_calc(d2_rd)

        full_msg = "__**Release Dates List** - *Times, Dates and Games are subject to change*__ \n \n" \
                   "***Overwatch*** releases in {},{} hours and {} minutes.\n" \
                   "***Battlefield*** ***1*** and ***Civilization*** ***6*** release in {},{} hours and {} minu" \
                   "tes. \n" \
                   "***No Man's Sky*** releases in {},{} hours and {} minutes.\n" \
                   "***Dishonored*** ***2*** releases in {},{} hours and {} minutes.\n" \
                   "".format(ow_days, ow_hrs, ow_mins, bf_days, bf_hrs, bf_mins, nms_days, nms_hrs, nms_mins,
                             d2_days, d2_hrs, d2_mins)

        await s.destructmsg(full_msg, 60, self.bot)


def rd_calc(rd):

    tdelta = rd - datetime.utcnow()
    tstr = str(tdelta)

    days, notdays = tstr.split(",")
    hrs, mins, secs = notdays.split(":")

    return days, hrs, mins


def get_time() -> dict:
    """
    Function to get local time in cities

    :return: Dictionary with {"city":"%H:%M"}
    """
    prague = pytz.timezone('Europe/Prague')
    now = prague.localize(datetime.now())
    fmt = '%H:%M'
    au_tz = pytz.timezone('Australia/Sydney')
    sydney = now.astimezone(au_tz).strftime(fmt)
    lon_tz = pytz.timezone('Europe/London')
    london = now.astimezone(lon_tz).strftime(fmt)
    ny_tz = pytz.timezone('US/Eastern')
    ny = now.astimezone(ny_tz).strftime(fmt)
    sf_tz = pytz.timezone('US/Pacific')
    sf = now.astimezone(sf_tz).strftime(fmt)
    return {"sydney": sydney, "london": london, "ny": ny, "sf": sf}


def setup(bot):
    bot.add_cog(General(bot))
