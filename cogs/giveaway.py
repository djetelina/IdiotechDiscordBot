from discord.ext import commands
import descriptions as desc
import simplify as s
import random
import asyncio
import time

giveawayslist = []
loop = asyncio.get_event_loop()


class Giveaway:
    """
    Object for giveaways, after creating call loop.create_event(self.countdown)
    """

    def __init__(self, game, countdown, channel, owner, bot):
        """
        Create a giveaway instance

        :param game:        Name of a game to giveaway
        :param countdown:   Number of minutes until conclusion
        :param channel:     Channel object where to open the giveaway
        :param owner:       User object of owner
        """
        self.game = game
        if countdown > 30:
            countdown = 30
        self.time = countdown * 60
        self.enrolled = []
        self.channel = channel
        self.owner = owner
        self.status = 1
        self.bot = bot
        giveawayslist.append(self)

    async def countdown(self):
        while True:
            if self.time > 0:
                self.time -= 1
                await asyncio.sleep(1)
            else:
                break
        if self.status:
            try:
                winner = random.choice(self.enrolled)
                await self.bot.send_message(self.channel, "{}'s giveaway winner of {} is: {}".format(
                        self.owner.mention, self.game, winner.mention))
                await s.whisper(self.owner, "Winner of your giveaway for {}: {}".format(
                        self.game, winner.mention), self.bot)
                await s.whisper(winner, "You won a giveaway for **{}** by {}".format(
                        self.game, self.owner.mention), self.bot)
            except IndexError:
                await self.bot.send_message(self.channel,
                                            "Nobody enrolled for {} and the giveaway has concluded".format(self.game))
                await s.whisper(self.owner, "Nobody enrolled for your giveaway of {}".format(self.game), self.bot)
            giveawayslist.remove(self)

    def enroll(self, user):
        self.enrolled.append(user)

    def remove(self, user):
        self.enrolled.remove(user)

    async def cancel(self):
        await self.bot.send_message(self.channel,
                                    "{} canceled their giveaway for {}".format(self.owner.mention, self.game))
        self.status = 0
        giveawayslist.remove(self)


class Giveaways:
    """
    Giveaway category of commands
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True, description=desc.giveaways, brief=desc.giveawaysb)
    async def giveaway(self, ctx):
        if ctx.invoked_subcommand is None:
            if len(giveawayslist) > 0:
                reply = "\nCurrently opened giveaways:\n=========="
                for ga in giveawayslist:
                    reply += "\n**{}** in {} by {} ({}, {} people enrolled)".format(
                            ga.game, ga.channel.mention, ga.owner.mention, parsesecs(ga.time), len(ga.enrolled))
                reply += "\n==========\nEnter giveaway with !enroll **GameName**"
            else:
                reply = "No giveaways open"

            await self.bot.say(reply)

    @giveaway.command(name="open", pass_context=True, description=desc.giveaway, brief=desc.giveawayb)
    async def _open(self, ctx, countdown: int, *, games: str):
        games = games.split(';')
        for game in games:
            print(game)
            ga = Giveaway(game, countdown, ctx.message.channel, ctx.message.author, self.bot)
            await self.bot.say("{} just opened a giveaway for {}. Type '!enroll {}' to enroll".format(
                    ctx.message.author.mention, game, game))
            loop.create_task(ga.countdown())

    @giveaway.command(name="cancel", pass_context=True, description=desc.cancelga, brief=desc.cancelgab)
    async def _cancel(self, ctx, *, game: str):
        for ga in giveawayslist:
            if ga.game == game and ctx.message.author == ga.owner:
                await ga.cancel()

    @commands.command(pass_context=True, description=desc.enroll, brief=desc.enrollb)
    async def enroll(self, ctx, *, game: str):
        user = ctx.message.author
        found = 0
        if len(giveawayslist) == 0:
            await s.whisper(user, "There are no giveaways opened", self.bot)
            return
        for opened in giveawayslist:
            if opened.game.lower() == game.lower():
                if ctx.message.channel == opened.channel and user not in opened.enrolled:
                    opened.enroll(user)
                    found = 1
                    await s.whisper(user, "You enrolled for {}".format(game), self.bot)
                elif user in opened.enrolled:
                    found = 1
                    await s.whisper(user, "You are already enrolled for this game", self.bot)
                else:
                    found = 1
                    await s.whisper(user, "You tried to enter a giveaway from  wrong channel, sorry can't do that",
                                    self.bot)
        if not found:
            await s.whisper(user, "Giveaway for the game you mentioned not found", self.bot)
        await self.bot.delete_message(ctx.message)


def parsesecs(sec: int) -> str:
    """
    Parses seconds into time left format
    This is to be used only for giveaways which have limit of 30 minutes

    :param sec: number of seconds
    :return:    string with time left
    """
    if sec >= 60:
        tleft = time.strftime("%M minutes left", time.gmtime(sec)).lstrip('0')
    else:
        tleft = time.strftime("%S seconds left", time.gmtime(sec)).lstrip('0')
    return tleft


def setup(bot):
    bot.add_cog(Giveaways(bot))
