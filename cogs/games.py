import asyncio
import logging
import bs4
import requests

from helpers import descriptions as desc, time_calculations as tc, simplify as s

from datetime import datetime

import aiohttp
from discord.ext import commands

# List with running game instances
games = {}
loop = asyncio.get_event_loop()
log = logging.getLogger(__name__)


class Game:
    def __init__(self, game, owner, bot):
        self.game = game
        self.owner = owner
        self.bot = bot
        self.players = [owner, ]
        self.description = 0
        games.update({self.game: self})

    def join(self, user):
        self.players.append(user)
        return "{0} joined {1}".format(user.name, self.game)

    def leave(self, user):
        if user in self.players:
            self.players.remove(user)
            response = "{0} left {1}".format(user.name, self.game)
            log.info(response)
        else:
            response = "{0} You can't leave a game you didn't join!".format(user.mention)
            log.info("{0} tried leaving a game he wasn't part of".format(user.name))
        return response

    def cancel(self):
        for k, v in games.items():
            if v == self:
                del games[k]
                log.info("{} canceled their game".format(self.owner.name))


class Games:
    def __init__(self, bot):

        self.bot = bot

        # Dates have to be in relation to UTC (so if release is 5am BST, it would be 4am UTC)
        # Preferably use the latest release time for a game with different release times for different regions
        self.dates = {
            "No Man''s Sky": datetime(2016, 8, 12, 0, 0, 0),
            "Deus Ex: Mankind Divided": datetime(2016, 8, 23, 0, 0, 0),
            "Battlefield 1": datetime(2016, 10, 21, 0, 0, 0),
            "Civilization 6": datetime(2016, 10, 21, 0, 0, 0),
            "Dishonored 2": datetime(2016, 11, 11, 0, 0, 0),
            "Mirror''s Edge: Catalyst": datetime(2016, 6, 9, 0, 0, 0),
            "Mafia III": datetime(2016, 10, 7, 0, 0, 0),
            "Pokemon Sun and Moon": datetime(2016, 11, 23, 0, 0, 0),
            "World of Warcraft: Legion": datetime(2016, 8, 30, 0, 0, 0),
            "Mighty No. 9": datetime(2016, 6, 21, 0, 0, 0),
        }

    @commands.command(pass_context=True, description=desc.release_dates, brief=desc.release_datesb)
    async def release(self, ctx):
        # We are using manual argument detection instead of @commands.group,
        # because we want sub-commands to be dynamic based on our self.dates dictionary
        for game in self.dates:
            maxlen = len(game)
        else:
            maxlen = 0
        arg = " ".join(ctx.message.content.split()[1:])

        if len(arg) > 0:
            found = False
            msg = "Found games starting with `{}`:\n\n```Ruby\n".format(arg.capitalize())
            for game in self.dates:
                if game.lower().startswith(arg.lower()) or game.lower() is arg.lower():
                    days, hrs, mins = tc.calc_until(self.dates[game])
                    msg += "{}\n".format(tc.create_msg(game, days, hrs, mins, maxlen))
                    found = True

            if not found:
                msg += ("No game in our release list found, that starts with {}".format(arg))

            msg += "```"

        else:
            msg = "**Release Dates List**\n\n```Ruby\n"
            for game, time in sorted(self.dates.items(), key=lambda x: x[1]):
                days, hrs, mins = tc.calc_until(self.dates[game])
                msg += "{}\n".format(tc.create_msg(game, days, hrs, mins, maxlen))
            msg += "```"

        await self.bot.say(msg)

    @commands.group(name="game", pass_context=True, description=desc.game, brief=desc.game)
    async def play(self, ctx):
        if ctx.invoked_subcommand is None:
            if len(games) > 0:
                reply = "People are playing:\n"
                for game_name, game in games.items():
                    reply += "\n**{}** ({} player/s, managed by {})".format(
                        game_name, len(game.players), game.owner.name)
                reply += "\n\nJoin them by typing !game join **Game**"

            else:
                reply = "No one is playing anything"

            await self.bot.say(reply)

    @play.command(name="open", pass_context=True, description=desc.open_game, brief=desc.open_game)
    async def _open(self, ctx, *, game: str):
        is_playing = False
        reply = ""
        for game_name, running_game in games.items():
            if ctx.message.author == running_game.owner:
                is_playing = True
                reply = "You are already maintiang one game, close that one first!"
                log.info("{} tried opening a game but he already owns one".format(
                    ctx.message.author.name))
                break
            for player in running_game.players:
                if ctx.message.author == player:
                    is_playing = True
                    reply = "You are already playing, leave the other game first by `!game leave`"
                    log.info("{} tried opening a game but he is playing a different one".format(
                        ctx.message.author.name))
                    break

        if not is_playing:
            Game(game, ctx.message.author, self.bot)
            reply = """Your game is now open!

            Why not telling people how to join you, where are you playing etc.?
            `!game description <ANYTHING>`

            Done with your playing session? Remember to clean up after yourself!
            `!game close`
            """
            await self.bot.say("{} just opened a community game, let's play {}!".format(
                ctx.message.author.name, game))
            log.info("Game {} by {} opened".format(game, ctx.message.author.name))

        await s.whisper(ctx.message.author, reply, self.bot)

    @play.command(name="description", pass_context=True, description=desc.game_desc, brief=desc.game_desc_b)
    async def _desc(self, ctx, *, description):
        for game_name, running_game in games.items():
            if ctx.message.author == running_game.owner:
                running_game.description = description
                await s.whisper(ctx.message.author, "Description for your community game accepted", self.bot)
                log.info("Description for game by {} provided".format(ctx.message.author.name))

    @play.command(name="close", pass_context=True, description=desc.game_close, brief=desc.game_close)
    async def _close(self, ctx):
        for game_name, running_game in games.items():
            if ctx.message.author == running_game.owner:
                running_game.cancel()
                await self.bot.say("Session for {0} is now closed!".format(running_game.game))

    @play.command(name="join", pass_context=True, description=desc.game_join, brief=desc.game_join)
    async def _join(self, ctx, *, game: str):
        user = ctx.message.author
        found = 0

        if len(games) == 0:
            await self.bot.say("Nobody is playing anything, why not `!game open` a new one?")
            log.info("{} tried to join a game but none were running".format(user.name))
            return

        is_playing = False
        for game_name, running_game in games.items():
            for player in running_game.players:
                if ctx.message.author == player:
                    is_playing = True
                    await s.whisper(user, "You are already playing {}".format(running_game.game), self.bot)
                    log.info("{} tried to join a game but he is playing a different one".format(user.name))
                    return

        if not is_playing:
            for game_name, running_game in games.items():
                if game_name.lower() == game.lower():
                    found = 1
                    reply = "{0} joined {1}".format(user.name, running_game.game)
                    running_game.players.append(user)
                    if running_game.description:
                        await s.whisper(user, "You joined {}, here's information by {}: {}".format(
                            game_name, running_game.owner.name, running_game.description), self.bot)
                        log.info("Messaged {} with description about game they joined".format(user.name))
                    await self.bot.say(reply)
                    log.info(reply)
                    break

            if not found:
                s.whisper(user, "Game {} not found".format(game), self.bot)

    @play.command(name="leave", pass_context=True, description=desc.game_leave, brief=desc.game_leave)
    async def _leave(self, ctx):
        for game_name, running_game in games.items():
            for player in running_game.players:
                if ctx.message.author == player:
                    running_game.players.remove(player)
                    self.bot.say("{0} is no longer playing {1}".format(player, running_game.game))
                    log.info("{0} left game {1}".format(player, running_game.game))

    @commands.command(description=desc.ow, brief=desc.owb)
    async def overwatch(self, region: str, battletag: str):
        msg = await self.bot.say("Fetching Stats for {}".format(battletag))

        user = battletag.replace("#", "-")

        reg_eu = ["eu", "euro", "europe"]
        reg_us = ["australia", "aussie", "aus", "us", "usa", "na", "america", "au"]
        reg_kr = ["asia", "korea", "kr", "as", "china", "japan"]

        if region.lower() in reg_eu:
            reg = "eu"
        elif region.lower() in reg_us:
            reg = "us"
        elif region.lower() in reg_kr:
            reg = "kr"
        else:
            self.bot.edit_message(msg, "Unknown region: {}".format(region))
            return

        future = loop.run_in_executor(
            None, requests.get, "https://playoverwatch.com/en-us/career/pc/{}/{}".format(reg, user))
        res = await future

        try:
            res.raise_for_status()
        except Exception as e:
            await self.bot.edit_message(msg, "**Error with request. Please check for mistakes before trying again.**"
                                             ".\nError: {}".format(str(e)))
            log.exception("Error with request")
            return

        doc = bs4.BeautifulSoup(res.text, "html.parser")
        page = doc.select('div')

        most_played = page[82].select('div')[2].getText()
        most_games = page[82].select('div')[3].getText()

        stats = doc.find_all('td')
        # print(stats)

        games_won = find_value(stats, "Games Won")
        games_played = find_value(stats, "Games Played")
        time_played = find_value(stats, "Time Played")

        games_lost = int(games_played) - int(games_won)
        won_lost = "{}/{}".format(games_won, games_lost)

        try:
            win_percent = round(((float(games_won) / float(games_played)) * 100), 1)
        except ZeroDivisionError:
            win_percent = "N/A"

        await self.bot.edit_message(msg, "**Overwatch Stats for {0} - {1}**\n\n"
                                         "Time Played:              *{2}*\n"
                                         "Total Games:             *{3}*\n"
                                         "Games Won/Lost:   *{4}* ({7}% win rate)\n"
                                         "Most Played Hero:   *{5}, {6} played*"
                                         "".format(battletag, reg.upper(), time_played, games_played,
                                                   won_lost, most_played, most_games, win_percent))

    # TODO http://csgo-stats.com/extrarandom/
        # Look into adding a !csgo command for get csgo profile stats
        # Looks like it should be pretty to do

    @commands.group(pass_context=True, description=desc.steam, brief=desc.steam)
    async def steam(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.bot.say("Available Subcommands: bestsellers, status\n"
                               "Usage: !steam <subcommand>")

    @steam.command(name="bestsellers", description=desc.steam_bs, brief=desc.steam_bs)
    async def _bs(self):
        future = loop.run_in_executor(
            None, requests.get, "http://store.steampowered.com/search/?filter=topsellers&os=win")
        res = await future

        try:
            res.raise_for_status()
        except Exception as e:
            await self.bot.say("**Error with request.\nError: {}".format(str(e)))
            log.exception("Error with request (games.py)")
            return

        doc = bs4.BeautifulSoup(res.text, "html.parser")
        title = doc.select('span[class="title"]')

        msg = """**Best Selling Steam Games**

 1) {}
2) {}
3) {}
4) {}
5) {}
""".format(title[0].getText(), title[1].getText(), title[2].getText(), title[3].getText(), title[4].getText())
        await self.bot.say(msg)

    @steam.command(name="status", description=desc.steam_status, brief=desc.steam_status)
    async def _status(self):
        steam_api = 'http://is.steam.rip/api/v1/?request=SteamStatus'
        with aiohttp.ClientSession() as session:
            async with session.get(steam_api)as resp:
                data = await resp.json()
                if str(data["result"]["success"]) == "True":
                    login = (data["result"]["SteamStatus"]["services"]["SessionsLogon"]).capitalize()
                    community = (data["result"]["SteamStatus"]["services"]["SteamCommunity"]).capitalize()
                    economy = (data["result"]["SteamStatus"]["services"]["IEconItems"]).capitalize()
                    # leaderboards = (data["result"]["SteamStatus"]["services"]["LeaderBoards"]).capitalize()

                    reply = """**Steam Server Status**

```xl
Login          {}
Community      {}
Economy        {}```""".format(login, community, economy)

                else:
                    reply = "Failed connecting to API - Error: {}".format(data["result"]["error"])

        await self.bot.say(reply)


def find_value(stats, name):
    """
    :param stats: stats list
    :param name: name of value to find (i.e. Games Won)
    :return: largest value for name (there are multiple game won's but the biggest will be the overall games won
    rather than a character specific games won
    """

    tagged_name = "<td>{}</td>".format(name)

    things = []
    is_time = False

    hour = []
    mins = []

    for item in stats:
        if name == "Time Played":
            is_time = True

            if str(item) == tagged_name:
                time = item.next_sibling.getText().split()
                if time[1] == "minutes" or time[1] == "minute":
                    mins.append(int(time[0]))
                elif time[1] == "hours" or time[1] == "hour":  # needed instead of else as it can also be in seconds
                    hour.append(int(time[0]))

        elif str(item) == tagged_name:
            things.append(int(item.next_sibling.getText()))

    if is_time:
        if not hour:
            # meaning max play time is in minutes
            return "{} minutes".format(max(mins))
            # doesnt accommodate for 1 min playtime but seriously why would you even have that short a play time

        elif hour:
            max_time = max(hour)
            sfx = "hours"
            if max_time == 1:
                sfx = "hour"
            return "{} {}".format(max_time, sfx)

    return max(things)


def setup(bot):
    bot.add_cog(Games(bot))
