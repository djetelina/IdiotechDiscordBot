from discord.ext import commands
from datetime import datetime
import pytz
import discord
import asyncio
import aiohttp
import json

description = "Bot for Idiotech's Discord by iScrE4m"
bot = commands.Bot(command_prefix='!', description=description)


def has_permissions(author: discord.Member, roles: set):
    U_roles = set([r.name for r in author.roles])
    if roles.intersection(U_roles):
        return True
    else:
        return False
        # if has_permissions(ctx.message.author, {"Admin", "Moderator"}):


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
    with open("log.txt", "w", encoding='utf-8') as file:
        async for msg in bot.logs_from(public, limit=500):
            if msg.author.name in users:
                string = "[{}] {}: {}\n".format(msg.timestamp, msg.author.name, msg.clean_content)
                file.write(string)
    with open("log.txt", "rb") as file:
        await bot.send_file(admin, file, filename="log.txt",
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
    msg = await bot.say(reply)
    await asyncio.sleep(20)
    await bot.delete_message(msg)


@bot.command(description="Links to Idiotech's Twitter")
async def twitter():
    msg = await bot.say('https://twitter.com/idiotechgaming')
    await asyncio.sleep(20)
    await bot.delete_message(msg)


@bot.command(description="Links to Idiotech's YouTube")
async def youtube():
    msg = await bot.say('https://www.youtube.com/c/idiotechgaming')
    await asyncio.sleep(20)
    await bot.delete_message(msg)


@bot.command(description="Sends a person to rules channel (not by force, this is a peaceful bot)")
async def rules():
    await bot.say('Please read <#179965419728273408>')


@bot.command(pass_context=True, description="Shows local time of Sydney, London and New York")
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
    msg = await bot.say("Sydney: {} (GMT+10) | London: {} | New York: {}".format(australia, london, ny))
    await asyncio.sleep(20)
    await bot.delete_message(msg)

with open("token.txt", "rb") as file:
    token = file.readline()

bot.run(token)
