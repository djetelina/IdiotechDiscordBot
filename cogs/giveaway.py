from discord.ext import commands
import descriptions as desc
import simplify as s
import channels as chan
import random
import asyncio
import time

# List with running giveaway instances
giveawayslist = []
# Channels where we are allowed to host giveaways
whitechannels = ['private', 'code', 'test']
loop = asyncio.get_event_loop()


class Giveaway:
    """
    Giveaway object

    To start counting down the giveaway timer we call loop.create_event(self.countdown())
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
        self.url = 0
        self.code = 0
        self.desc = 0
        self.status = 1
        self.bot = bot
        giveawayslist.append(self)

    async def countdown(self):
        """
        Start counting down the giveaway
        """
        while True:
            if self.time > 0:
                self.time -= 1
                await asyncio.sleep(1)
            else:
                break
        # After the countdown is complete, check if the givaway hasn't been cancelled
        if self.status:
            try:
                stats = self.bot.get_cog('Stats')
                if stats is not None:
                    await stats.on_giveaway(self.game)

                random.seed()
                winner = random.choice(self.enrolled)

                await self.bot.send_message(self.channel, "{}'s giveaway winner of {} is: {}".format(
                    self.owner.mention, self.game, winner.mention))
                await s.whisper(self.owner, "Winner of your giveaway for {}: {}".format(
                    self.game, winner.mention), self.bot)
                await s.whisper(winner, "You won a giveaway for **{}** by {}".format(
                    self.game, self.owner.mention), self.bot)

                if self.code:
                    await s.whisper(winner, "Your game code: {}".format(self.code), self.bot)
                    await s.whisper(self.owner, "I have sent them the code you provided.", self.bot)

            except IndexError:
                await self.bot.send_message(
                    self.channel, "Nobody enrolled for {} and the giveaway has concluded".format(self.game))
                await s.whisper(self.owner, "Nobody enrolled for your giveaway of {}".format(self.game), self.bot)

            giveawayslist.remove(self)

    def enroll(self, user):
        self.enrolled.append(user)

    def remove(self, user):
        """
        Right now not used
        Possible ways to implement:
            !enroll cancel
            Remove somebody from giveaway and permit them from entering
                Would need to add blacklist function
                    This is okay with #public not being whitelisted
        """
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

    @commands.group(pass_context=True, description=desc.giveaway, brief=desc.giveawayb)
    async def giveaway(self, ctx):
        if ctx.invoked_subcommand is None:
            if len(giveawayslist) > 0:
                reply = "\nCurrently opened giveaways:\n=========="
                for ga in giveawayslist:
                    reply += "\n**{}** in {} by {} ({}, {} people enrolled)".format(
                        ga.game, ga.channel.mention, ga.owner.mention, parsesecs(ga.time), len(ga.enrolled))
                reply += "\n==========\nEnter giveaway with !enroll **GameName**"

            else:
                reply = "No giveaway open"

            await self.bot.delete_message(ctx.message)
            await s.destructmsg(reply, 10, self.bot)  # left in just in case i break something

    @giveaway.command(name="open", pass_context=True, description=desc.openga, brief=desc.opengab)
    async def _open(self, ctx, channel: str, countdown: int, *, game: str):
        has_opened = False
        for giveaway in giveawayslist:
            if ctx.message.author == giveaway.owner:
                has_opened = True

        if not has_opened:
            try:
                destination = self.bot.get_channel(chan.channels[channel])
                if channel in whitechannels:
                    Giveaway(game, countdown, destination, ctx.message.author, self.bot)
                    await s.whisper(ctx.message.author, """I have prepared the giveaway.

                    If you want me to automatically PM the winner the code please use:
                    `!giveaway code <CODE>`

                    If you want to add a link to the game's page (like steam url) please use:
                    This message will show once after you open the giveaway:
                    `!giveaway link <URL>`

                    If you want to say more about the game or a giveaway, like where is it redeemable,
                    if you are also giving away DLC with it etc.
                    You can also include url here instead of using the previous command
                    This message will show once after you open the giveaway:
                    `!giveaway description <DESCRIPTION>`

                    I will open the enrollments to your giveaway after you send me `!giveaway confirm`
                    """, self.bot)

                else:
                    await s.whisper(
                        ctx.message.author, "I'm sorry, but you can't open a giveaway in this channel.", self.bot)

            except KeyError:
                await s.whisper(ctx.message.author, "I don't know channel *{}*".format(channel), self.bot)

        else:
            await s.whisper(ctx.message.author, "You already have one giveaway open", self.bot)

    @giveaway.command(name="link", pass_context=True, description=desc.linkga, brief=desc.linkga)
    async def _link(self, ctx, url: str):
        for giveaway in giveawayslist:
            if ctx.message.author == giveaway.owner:
                giveaway.url = url
                await s.whisper(giveaway.owner, "Link accepted", self.bot)

    @giveaway.command(name="code", pass_context=True, description=desc.codega, brief=desc.codegab)
    async def _code(self, ctx, *, code: str):
        for giveaway in giveawayslist:
            if ctx.message.author == giveaway.owner:
                giveaway.code = code
                await s.whisper(giveaway.owner, "Code accepted", self.bot)

    @giveaway.command(name="description", pass_context=True, description=desc.descga, brief=desc.descga)
    async def _description(self, ctx, *, description: str):
        for giveaway in giveawayslist:
            if ctx.message.author == giveaway.owner:
                giveaway.description = description
                await s.whisper(giveaway.owner, "Description accepted", self.bot)

    @giveaway.command(name="confirm", pass_context=True, description=desc.confirmga, brief=desc.confirmga)
    async def _confirm(self, ctx):
        for giveaway in giveawayslist:
            if ctx.message.author == giveaway.owner:
                await s.whisper(giveaway.owner, "Thank you, I'll open the giveaway now.", self.bot)
                loop.create_task(giveaway.countdown())
                await self.bot.send_message(
                    giveaway.channel, "@here {0} just opened a giveaway for {1}. Type '!enroll {1}' to enroll".format(
                        giveaway.owner.mention, giveaway.game))

                if giveaway.desc:
                    await self.bot.send_message(giveaway.channel, "Description: {}".format(giveaway.description))

                if giveaway.url:
                    await self.bot.send_message(giveaway.channel, giveaway.url)

    @giveaway.command(name="cancel", pass_context=True, description=desc.cancelga, brief=desc.cancelgab)
    async def _cancel(self, ctx):
        for ga in giveawayslist:
            if ctx.message.author == ga.owner:
                await ga.cancel()
                await s.whisper(ga.owner, "Giveaway canceled", self.bot)

    @commands.command(pass_context=True, description=desc.enroll, brief=desc.enrollb)
    async def enroll(self, ctx, *, game: str):
        user = ctx.message.author
        found = 0

        if len(giveawayslist) == 0:
            await s.whisper(user, "There are no giveaway opened", self.bot)
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
    This is to be used only for giveaway which have limit of 30 minutes

    :param sec: number of seconds
    :return:    string with time left
    """
    if sec >= 120:
        tleft = time.strftime("%M minutes left", time.gmtime(sec)).lstrip('0')
    elif sec >= 60:
        tleft = time.strftime("%M minute left", time.gmtime(sec)).lstrip('0')
    else:
        tleft = time.strftime("%S seconds left", time.gmtime(sec)).lstrip('0')

    return tleft


def setup(bot):
    bot.add_cog(Giveaways(bot))
