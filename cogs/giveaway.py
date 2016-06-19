import asyncio
import random
import logging

from discord.ext import commands

import helpers.simplify as s
from helpers import descriptions as desc, settings
import helpers.time_calculations as tc

# List with running giveaway instances
giveawayslist = []
loop = asyncio.get_event_loop()
log = logging.getLogger(__name__)


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
        log.info("Giveaway for {} is being started by {}".format(self.game, self.owner.name))

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
                log.info("{1} won {0}".format(self.game, winner.name))

                await self.bot.send_message(self.channel, "{}'s giveaway of {} has been won by {}".format(
                    self.owner.mention, self.game, winner.mention))
                await s.whisper(self.owner, "Winner of your giveaway for {}: {}".format(
                    self.game, winner.mention), self.bot)
                await s.whisper(winner, "You won a giveaway for **{}**, don't forget to thank {}!".format(
                    self.game, self.owner.mention), self.bot)

                if self.code:
                    await s.whisper(winner, "Your game code: {}".format(self.code), self.bot)
                    await s.whisper(self.owner, "I have sent them the code you provided.", self.bot)
                    log.info("Code sent to the winner")

            except IndexError:
                await self.bot.send_message(
                    self.channel, "Nobody enrolled for {} and the giveaway has concluded".format(self.game))
                await s.whisper(self.owner, "Nobody enrolled for your giveaway for {}".format(self.game), self.bot)

            giveawayslist.remove(self)
            await changetopic(self.bot)

    def enroll(self, user):
        self.enrolled.append(user)

    def remove(self, user):
        """
        Right now not used
        Possible ways to implement:
            !enroll cancel
            Remove somebody from giveaway and permit them from entering
                Would need to add blacklist function
        """
        self.enrolled.remove(user)

    async def cancel(self):
        await self.bot.say("{} canceled their giveaway for {}".format(self.owner.mention, self.game))
        log.info("{} canceled their giveaway".format(self.owner.name))
        self.status = 0
        giveawayslist.remove(self)


class Giveaways:
    """
    Giveaway category of commands
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True, description=desc.giveaway, brief=desc.giveaway_brief)
    async def giveaway(self, ctx):
        if ctx.invoked_subcommand is None:
            if len(giveawayslist) > 0:
                reply = "Currently opened giveaways:\n"
                for ga in giveawayslist:
                    reply += "\n**{}** by {} ({}, {} people enrolled)".format(
                        ga.game, ga.owner.mention, tc.parsesecs(ga.time), len(ga.enrolled))
                reply += "\n\nEnter giveaway with !enroll **GameName**"

            else:
                reply = "No giveaway open"

            await self.bot.say(reply)

    @giveaway.command(name="open", pass_context=True, description=desc.openga, brief=desc.opengab)
    async def _open(self, ctx, countdown: int, *, game: str):
        has_opened = False
        for giveaway in giveawayslist:
            if ctx.message.author == giveaway.owner:
                has_opened = True

        if not has_opened:
            Giveaway(game, countdown, self.bot.get_channel(settings.channels['giveaways']), ctx.message.author,
                     self.bot)
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
            await s.whisper(ctx.message.author, "You already have a giveaway open", self.bot)

    @giveaway.command(name="link", pass_context=True, description=desc.link_ga, brief=desc.link_ga_brief)
    async def _link(self, ctx, url: str):
        for giveaway in giveawayslist:
            if ctx.message.author == giveaway.owner:
                giveaway.url = url
                await s.whisper(giveaway.owner, "Link accepted", self.bot)
                log.info("Link for giveaway by {} provided".format(giveaway.owner.name))

    @giveaway.command(name="code", pass_context=True, description=desc.code_ga, brief=desc.code_ga_brief)
    async def _code(self, ctx, *, code: str):
        """
        Example: !giveaway code 123-ABC-356 (STEAM)

        Will PM the winner with:
        Your game code: 123-ABC-356 (STEAM)
        """
        for giveaway in giveawayslist:
            if ctx.message.author == giveaway.owner:
                giveaway.code = code
                await s.whisper(giveaway.owner, "Code accepted", self.bot)
                log.info("Code for giveaway by {} provided".format(giveaway.owner.name))

    @giveaway.command(name="description", pass_context=True, description=desc.desc_ga, brief=desc.desc_ga_brief)
    async def _description(self, ctx, *, description: str):
        for giveaway in giveawayslist:
            if ctx.message.author == giveaway.owner:
                giveaway.description = description
                await s.whisper(giveaway.owner, "Description accepted", self.bot)
                log.info("Description for giveaway by {} provided".format(giveaway.owner.name))

    @giveaway.command(name="confirm", pass_context=True, description=desc.confirm_ga, brief=desc.confirm_ga)
    async def _confirm(self, ctx):
        for giveaway in giveawayslist:
            if ctx.message.author == giveaway.owner:
                await s.whisper(giveaway.owner, "Thank you, I'll open the giveaway now.", self.bot)
                loop.create_task(giveaway.countdown())
                await self.bot.send_message(
                    giveaway.channel, "@here {0} just opened a giveaway for {1}. Type '!enroll {1}' to enroll".format(
                        giveaway.owner.mention, giveaway.game))
                await changetopic(self.bot)

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
                await changetopic(self.bot)

    @commands.command(pass_context=True, description=desc.enroll, brief=desc.enroll_brief)
    async def enroll(self, ctx, *, game: str):
        user = ctx.message.author
        found = 0

        if len(giveawayslist) == 0:
            await s.whisper(user, "There are no giveaways open to enter!", self.bot)
            return

        for opened in giveawayslist:
            if opened.game.lower() == game.lower():
                if ctx.message.channel == opened.channel and user not in opened.enrolled:
                    opened.enroll(user)
                    found = 1
                    await s.whisper(user, "You enrolled for {}, good luck!".format(game), self.bot)
                    break

                elif user in opened.enrolled:
                    found = 1
                    await s.whisper(user, "You have already enrolled for this game", self.bot)
                    break

                else:
                    found = 1
                    await s.whisper(user, "You tried to enter a giveaway from  wrong channel.\n"
                                          "I'm sorry {}, I'm afraid I can't let you do that.".format(user.mention),
                                    self.bot)
                    break

        if not found:
            await s.whisper(user, "Giveaway for the game you gave does not exists, check your spelling.", self.bot)

        try:
            await self.bot.delete_message(ctx.message)
        except Exception as e:
            log.exception("Couldn't delete enroll message")

        await changetopic(self.bot)

# TODO eventually test if this indeed is broken in the class, for some reason ER says he thinks it was
async def changetopic(bot):
        new_topic = "Giveaways running: {0} | Total enrolled: {1}".format(
            len(giveawayslist), sum(len(giveaway.enrolled) for giveaway in giveawayslist))
        log.debug("New topic in giveaways: {}".format(new_topic))
        try:
            await bot.edit_channel(bot.get_channel(settings.channels['giveaways']), topic=new_topic)
            log.debug("Topic updated in giveaways")
        except Exception as e:
            log.exception("Couldn't change topic in giveaways")


def setup(bot):
    bot.add_cog(Giveaways(bot))
