from discord.ext import commands
import descriptions as desc
import simplify as s
import random
import asyncio

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
            except IndexError:
                await self.bot.send_message(self.channel,
                                            "Nobody enrolled for {} and the giveaway has concluded".format(self.game))
            giveawayslist.remove(self)

    def enroll(self, user):
        self.enrolled.append(user)

    def remove(self, user):
        self.enrolled.remove(user)

    async def cancel(self):
        await self.bot.send_message(self.channel,
                                    "{} canceled his giveaway for {}".format(self.owner.mention, self.game))
        self.status = 0
        giveawayslist.remove(self)


class Giveaways:
    """
    Giveaway category of commands
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, description=desc.giveaway, brief=desc.giveawayb)
    async def giveaway(self, ctx):
        try:
            countdown = int(ctx.message.content.split(' ')[1])
            games = " ".join(ctx.message.content.split(' ')[2:]).split(';')
            for game in games:
                ga = Giveaway(game, countdown, ctx.message.channel, ctx.message.author, self.bot)
                await self.bot.say("{} just opened a giveaway for {}. Type '!enroll {}' to enroll".format(
                        ctx.message.author.mention, game, game))
                loop.create_task(ga.countdown())
        except ValueError:
            await s.whisper(ctx.message.author, "You must enter minutes as whole number (no decimal point)!", self.bot)
        except IndexError:
            await s.whisper(ctx.message.author, "Error trying to open a giveaway, don't forget number of minutes!",
                            self.bot)

    @commands.command(pass_context=True, description=desc.cancelga, brief=desc.cancelgab)
    async def cancelga(self, ctx):
        game = ctx.message.content.split(' ')[1:]
        for ga in giveawayslist:
            if ga.game == game and ctx.message.author == ga.owner:
                await ga.cancel()

    @commands.command(pass_context=True, description=desc.enroll, brief=desc.enrollb)
    async def enroll(self, ctx):
        user = ctx.message.author
        found = 0
        try:
            game = ' '.join(ctx.message.content.split(' ')[1:])
        except TypeError:
            await s.whisper(user, "You have to choose a game when enrolling", self.bot)
            return
        if len(giveawayslist) == 0:
            await s.whisper(user, "There are no giveaways opened", self.bot)
            return
        for opened in giveawayslist:
            if opened.game == game:
                if ctx.message.channel == opened.channel:
                    opened.enroll(user)
                    found = 1
                    await s.whisper(user, "You enrolled for {}".format(game), self.bot)
                else:
                    found = 1
                    await s.whisper(user, "You tried to enter a giveaway from  wrong channel, sorry can't do that",
                                    self.bot)
        if not found:
            await s.whisper(user, "Giveaway for your game not found", self.bot)

    @commands.command(description=desc.giveaways, brief=desc.giveawaysb)
    async def giveaways(self):
        if len(giveawayslist) > 0:
            reply = "Currently opened giveaways:"
            for ga in giveawayslist:
                reply += " {} in {} ({} seconds left, {} people enrolled)".format(
                        ga.game, ga.channel.mention, ga.time, len(ga.enrolled))
        else:
            reply = "No giveaways open"
        await self.bot.say(reply)


def setup(bot):
    bot.add_cog(Giveaways(bot))
