from discord.ext import commands
import simplify as s
import descriptions as desc
import aiohttp
from datetime import datetime
from pytz import timezone

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

    @commands.command(description=desc.rd, brief=desc.rd)
    async def rd(self):
        ow_rd = datetime(2016, 5, 24, 0, 0, 0)
        bf_rd = datetime(2016, 10, 21, 0, 0, 0)
        nms_rd = datetime(2016, 6, 21, 0, 0, 0)
        d2_rd = datetime(2016, 11, 11, 0, 0, 0)
        dx_rd = datetime(2016, 8, 23, 0, 0, 0)
        hi_rd = datetime(2016, 6, 6, 0, 0, 0)

        ow_days, ow_hrs, ow_mins = rd_calc(ow_rd) # OW and TW:W have the same release date
        bf_days, bf_hrs, bf_mins = rd_calc(bf_rd)  # BF1 and Civ6 have the same release date
        nms_days, nms_hrs, nms_mins = rd_calc(nms_rd)
        d2_days, d2_hrs, d2_mins = rd_calc(d2_rd)
        dx_days, dx_hrs, dx_mins = rd_calc(dx_rd)
        hi_days, hi_hrs, hi_mins = rd_calc(hi_rd)

        # template: "*** *** releases in {},{} hours and {} minutes.\n".format(_days, _hrs, _mins)

        title_msg = "__**Release Dates List** - *Times, Dates and Games are subject to change*__ \n \n"
        ow_msg = "***Overwatch*** and ***Total War: Warhammer*** release in {},{} hours and {} minutes.\n".format(ow_days, ow_hrs, ow_mins)
        nms_msg = "***No Man's Sky*** releases in {},{} hours and {} minutes.\n".format(nms_days, nms_hrs, nms_mins)
        bf_msg = "***Battlefield*** ***1*** and ***Civilization*** ***6*** release in {},{} hours and {} minu" \
                 "tes. \n".format(bf_days, bf_hrs, bf_mins)
        d2_msg = "***Dishonored*** ***2*** releases in {},{} hours and {} minutes.\n".format(d2_days, d2_hrs, d2_mins)
        dx_msg = "***Deus Ex: Mankind Divided*** releases in {},{} hours and {} minutes.\n".format(dx_days, dx_hrs,
                                                                                                   dx_mins)
        hi_msg = "***Hearts of Iron*** ***4*** releases in {},{} hours and {}minutes.\n".format(hi_days, hi_hrs, hi_mins)
        # having it like this should make changing them easier compared to how it was previously set up

        full_msg = title_msg + ow_msg + hi_msg + nms_msg + dx_msg + bf_msg + d2_msg

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
    fmt = '%H:%M'

    # http://www.saltycrane.com/blog/2009/05/converting-time-zones-datetime-objects-python/

    now_utc = datetime.now(timezone('UTC'))  # print(now_utc.strftime(fmt))

    now_pacific = now_utc.astimezone(timezone('US/Pacific'))
    sf = now_pacific.strftime(fmt)

    now_london = now_utc.astimezone(timezone('Europe/London'))
    london = now_london.strftime(fmt)

    now_sydney = now_utc.astimezone(timezone('Australia/Sydney'))
    sydney = now_sydney.strftime(fmt)

    now_ny = now_utc.astimezone(timezone('US/Eastern'))
    ny = now_ny.strftime(fmt)

    return {"sydney": sydney, "london": london, "ny": ny, "sf": sf}


def setup(bot):
    bot.add_cog(General(bot))
