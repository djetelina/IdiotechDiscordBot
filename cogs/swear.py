import asyncio
import simplify as s
import random
import channels as chan
from discord.ext import commands
import checks
import os
import id_settings as id

"""
DRAFT VERSION
"""

watchlist = {}
loop = asyncio.get_event_loop()


class Warns:
    warnings = []
    
    def __init__(self, user, bot, points):
        self.user = user
        self.bot = bot
        self.points = 0
        
        if len(Warns.warnings) == 0:
            file = open(os.path.join(os.getcwd(), "cogs/swears/warnings.txt"),'r')
            Warns.warnings = file.readlines()

        watchlist.update({self.user: self})
        self.new(points)

    def new(self, points):
        self.points += points
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
    confusables = []
    swears = []
    
    def __init__(self, bot):
        self.bot = bot
        if len(Swear.confusables) == 0:
            file = open(os.path.join(os.getcwd(), "cogs/swears/confusables.txt"), encoding="utf-8-sig")
            Swear.confusables = file.readlines()
            file.close()
            Swear.confusables[:] = [confusable_line.strip() for confusable_line in Swear.confusables]
        if len(Swear.swears) == 0:
            file = open(os.path.join(os.getcwd(), "cogs/swears/swears.txt"), encoding="utf-8-sig")
            Swear.swears = file.readlines()
            file.close()
            Swear.swears[:] = [self.stomp_confusables(bad_word.strip()) for bad_word in Swear.swears]
        self.ignore = id.bot_id

    async def message(self, message):
        if message.author.id is not self.ignore:
            message.content = self.stomp_confusables(message.content.strip())
            self.check_swears(message)

    def stomp_confusables(self, input_string):
        output_string = ""
        for char in input_string:
            for confusable_line in Swear.confusables:
                if char in confusable_line:
                    char = confusable_line[:1]
                    break
            output_string += char
        return output_string

    def check_swears(self, message):
        swear_count = 0
        message_words = message.content.split()
        for bad_word in Swear.swears:
            bad_word = bad_word.strip()
            if bad_word[:1] == '*':
                for message_word in message_words:
                    partial_match = bad_word[1:]
                    if partial_match in message_word.strip():
                        swear_count += 1
            else:
                if bad_word in message_words:
                    swear_count += 1
        if swear_count > 0:
            self.trigger(message, swear_count)

    def trigger(self, message, points):
        if message.author in watchlist:
            watchlist[message.author].new(points)
        else:
            Warns(message.author, self.bot, points)

    @commands.command(hidden=True)
    @checks.mod_or_permissions(manage_messages=True)
    async def points(self, *, who: str):
        for user, instance in watchlist.items():
            if who.lower() in user.name.lower():
                await self.bot.say("{} has {} warning points.".format(instance.user.mention, instance.points))
                return
            else:
                await self.bot.say("User {} not found in watchlist".format(who))


def setup(bot):
    bot.add_cog(Swear(bot))
