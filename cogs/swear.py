import asyncio
import simplify as s
import random


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
        watchlist.update({self.user: self})
        self.new()

    def new(self):
        self.points += 1
        self.point_check()
        loop.create_task(self.decay)

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
            loop.create_task(self.warn_user)
        elif self.points == 0:
            del watchlist[self.user]

    async def warn_user(self):
        s.whisper(self.user, "I'm warning you", self.bot)


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

    async def check_grey(self, message):
        for word in self.greylist:
            if word in message.content:
                self.trigger(message)
                return

    async def check_black(self, message):
        for word in self.blacklist:
            if word in message.content:
                self.trigger(message)
                return

    async def trigger(self, message):
        if message.author in watchlist:
            watchlist['message.author'].new()
        else:
            Warns(message.author, self.bot)


def setup(bot):
    bot.add_cog(Swear(bot))