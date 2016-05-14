from discord.ext import commands
from datetime import datetime
import pytz
import discord
import asyncio
import aiohttp
import random

description = "Bot for Idiotech's Discord by iScrE4m"
bot = commands.Bot(command_prefix='!', description=description, pm_help=True)

"""def has_permissions(author: discord.Member, roles: set):
    U_roles = set([r.name for r in author.roles])
    if roles.intersection(U_roles):
        return True
    else:
        return False
        # if has_permissions(ctx.message.author, {"Admin", "Moderator"}):
"""


def is_idiotech():
    def predicate(ctx):
        return ctx.message.author.id == "176291669254209539"

    return commands.check(predicate)


def is_scream():
    def predicate(ctx):
        return ctx.message.author.id == "132577770046750720"

    return commands.check(predicate)


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


giveawaydescription = """"Open a giveaway for current channel
Arguments: Time in minutes, names of games separated by ;
Example: !giveaway 60 Overwatch;Half-Life 3"""


loop = asyncio.get_event_loop()


@bot.command(pass_context=True, description=giveawaydescription)
async def giveaway(ctx):
    try:
        countdown = int(ctx.message.content.split(' ')[1])
        games = " ".join(ctx.message.content.split(' ')[2:]).split(';')
        for game in games:
            ga = Giveaway(game, countdown, ctx.message.channel)
            await bot.say("{} just opened a giveaway for {}. Type '!enroll {}' to enroll".format(
                    ctx.message.author.mention, game, game))
            loop.create_task(ga.countdown())
    except ValueError:
        pass


@bot.command(pass_context=True, description="Enroll in a giveaway for a certain game. Example !enroll Overwatch")
async def enroll(ctx):
    user = ctx.message.author
    game = ' '.join(ctx.message.content.split(' ')[1:])
    for opened in giveawayslist:
        if opened.game == game:
            if ctx.message.channel == opened.channel:
                opened.enroll(user)
                await bot.start_private_message(user)
                await bot.send_message(user, "You enrolled for {}".format(game))
            else:
                await bot.start_private_message(user)
                await bot.send_message(user, "You tried to enter a giveaway from  wrong channel, sorry can't do that")


@bot.command(description="Checks statuses of opened giveaways")
async def giveaways():
    if len(giveawayslist) > 0:
        reply = "Currently opened giveaways:"
        for ga in giveawayslist:
            reply += " {} in {} ({} seconds left, {} people enrolled)".format(
                    ga.game, ga.channel.mention, ga.time, len(ga.enrolled))
    else:
        reply = "No giveaways open"
    await bot.say(reply)


@bot.command(hidden=True, description="Are you going to code me? No, then don't touch this")
@is_scream()
async def develop():
    await bot.say('iScrE4m is streaming my development over at http://twitch.tv/iScrE4m - come watch!')


@bot.command(hidden=True, description="Not for plebs")
@is_idiotech()
async def dance():
    await bot.say('Moves like Jagger I tell you')


@bot.command(pass_context=True, hidden=True, description="Don't try this")
@is_idiotech()
async def log(ctx):
    users = " ".join(ctx.message.content.split(' ')[1:]).split(';')
    public = ctx.message.server.get_channel("176293292865093632")
    admin = ctx.message.server.get_channel("176304607172100097")
    with open("log.txt", "w", encoding='utf-8') as logfile:
        async for msg in bot.logs_from(public, limit=500):
            if msg.author.name in users:
                string = "[{}] {}: {}\n".format(msg.timestamp, msg.author.name, msg.clean_content)
                logfile.write(string)
    with open("log.txt", "rb") as logfile:
        await bot.send_file(admin, logfile, filename="log.txt",
                            content="Log file for mentioned users from last 500 messages in public channel.")


@bot.command(description="Links to Idiotech's Twitch")
async def twitch():
    with aiohttp.ClientSession() as session:
        async with session.get('https://api.twitch.tv/kraken/streams?channel=idiotechgaming')as resp:
            data = await resp.json()
            if len(data["streams"]) > 0:
                game = data["streams"][0]["game"]
                reply = "Idiotech is live streaming {}! https://www.twitch.tv/idiotechgaming".format(game)
            else:
                reply = "https://www.twitch.tv/idiotechgaming (OFFLINE)"
    await destructmsg(reply, 20)


@bot.command(description="Links to Idiotech's Twitter")
async def twitter():
    await destructmsg('https://twitter.com/idiotechgaming', 20)


@bot.command(description="Links to Idiotech's YouTube")
async def youtube():
    await destructmsg('https://www.youtube.com/c/idiotechgaming', 20)


@bot.command(description="Sends a person to rules channel (not by force, this is a peaceful bot)")
async def rules():
    await bot.say('Please read <#179965419728273408>')


@bot.command(description="Shows local time of Sydney, London and New York")
async def time():
    prague = pytz.timezone('Europe/Prague')
    now = prague.localize(datetime.now())
    fmt = '%H:%M'
    au_tz = pytz.timezone('Australia/Sydney')
    australia = now.astimezone(au_tz).strftime(fmt)
    lon_tz = pytz.timezone('Europe/London')
    london = now.astimezone(lon_tz).strftime(fmt)
    ny_tz = pytz.timezone('US/Eastern')
    ny = now.astimezone(ny_tz).strftime(fmt)
    await destructmsg("Sydney: {} (GMT+10) | London: {} | New York: {}".format(australia, london, ny), 20)


giveawayslist = []


class Giveaway:
    def __init__(self, game, countdown, channel):
        self.game = game
        self.time = countdown * 60
        self.enrolled = []
        self.channel = channel
        giveawayslist.append(self)

    async def countdown(self):
        while True:
            if self.time > 0:
                self.time -= 1
                await asyncio.sleep(1)
            else:
                break
        try:
            winner = random.choice(self.enrolled)
            await bot.send_message(self.channel, "The winner of {} is: {}".format(self.game, winner.mention))
        except IndexError:
            await bot.send_message(self.channel,
                                   "Nobody enrolled for {} and the giveaway has concluded".format(self.game))
        giveawayslist.remove(self)

    def enroll(self, user):
        self.enrolled.append(user)

    def remove(self, user):
        self.enrolled.remove(user)


async def destructmsg(msg, seconds):
    message = await bot.say(msg)
    await asyncio.sleep(seconds)
    await bot.delete_message(message)


with open("token.txt", "r") as file:
    token = file.readline()

bot.run(token)
