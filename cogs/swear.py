import asyncio
import simplify as s
import random
import channels as chan
from discord.ext import commands
import checks

"""
DRAFT VERSION
"""

watchlist = {}
loop = asyncio.get_event_loop()


class Warns:
    def __init__(self, user, bot):
        self.user = user
        self.bot = bot
        self.points = 0
        self.warnings = ["Please don't swear!", "Don't swear, thanks!", 'Is there a need for suo much bad language?',
                         "That's it, I'm reporting you to the authorities!", "I'm a child, watch your language.",
                         "Did you know you already have at least 3 penalty points for swearing? Please stop",
                         "I'm no GLaDOS, but I like science too. Your swears are not science.",
                         "You know that you can express things without swears?", "Was that word necessary?"]
        watchlist.update({self.user: self})
        self.new()

    def new(self):
        self.points += 1
        if self.point_check():
            loop.create_task(self.warn_user())
        loop.create_task(self.decay())

    async def decay(self):
        time = 120
        while True:
            if time > 0:
                time -= 1
                await asyncio.sleep(1)

            else:
                break

        self.points -= 1
        self.point_check()

    def point_check(self):
        if self.points >= 3:
            return True

        if self.points == 0:
            del watchlist[self.user]

    async def warn_user(self):
        await s.whisper(self.user, random.choice(self.warnings), self.bot)
        await self.bot.send_message(
            self.bot.get_channel(chan.channels['admin']),
            "User {} seems to be swearing a lot. He now has {} penalty points".format(
                self.user.mention, self.points))


class Swear:
    def __init__(self, bot):
        self.bot = bot
        self.greylist = ["fuck", "shit", "cunt"]
        self.blacklist = ["nigga", "nigger", "kys", "fuck you", "fuck u"]
        self.ignore = "180842549873737728"

    async def message(self, message):
        if message.author.id is not self.ignore:
            self.check_grey(message)
            self.check_black(message)

    def check_grey(self, message):
        for word in self.greylist:
            if word in message.content:
                self.trigger(message)
                break

    def check_black(self, message):
        for word in self.blacklist:
            if word in message.content:
                self.trigger(message)
                break

    def trigger(self, message):
        if message.author in watchlist:
            watchlist[message.author].new()

        else:
            Warns(message.author, self.bot)

    @commands.command(hidden=True)
    @checks.mod_or_permissions(manage_messages=True)
    async def points(self, *, who: str):
        for user, instance in watchlist.items():
            if who.lower() in user.name.lower():
                print("found")
                await self.bot.say("{} has {} warning points.".format(instance.user.mention, instance.points))
                return
            else:
                await self.bot.say("User {} not found in watchlist".format(who))


def setup(bot):
    bot.add_cog(Swear(bot))
