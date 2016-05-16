import asyncio
import simplify as s


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


async def message(bot, message):
    """
    after you decide he used something for which you want to give him a point:

    if message.author in watchlist:
        watchlist['message.author'].new()
    else:
        Warns(message.author, bot)

    Only create the logic for detecting the bad words

    If you want grey words to have different weight than black words
    we can have new_grey and new_black methods instead of new, add different amount of points
    Then for every point loop.create_task(self.decay)
    """
    pass

