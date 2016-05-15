import discord
from discord.ext import commands
import descriptions as desc
import checks
import random
import simplify as s

bot = commands.Bot(command_prefix='!', description=desc.main, pm_help=True)
extensions = ['cogs.giveaway', 'cogs.general', 'cogs.restricted', ]
"""
Don't forget to re-add swear.py ^^
"""


@bot.event
async def on_ready():
    """After logging in"""
    print(bot.user.name + ' logged in')
    await bot.change_status(game=discord.Game(name='!help'))


@bot.command(hidden=True)
@checks.is_scream()
async def load(*, module: str):
    """
    Loads a module.
    """
    module = module.strip()
    try:
        bot.load_extension(module)
    except Exception as e:
        await bot.say('\U0001f52b')
        await bot.say('{}: {}'.format(type(e).__name__, e))
    else:
        await bot.say('\U0001f44c')


@bot.command(hidden=True)
@checks.is_scream()
async def unload(*, module: str):
    """Unloads a module."""
    module = module.strip()
    try:
        bot.unload_extension(module)
    except Exception as e:
        await bot.say('\U0001f52b')
        await bot.say('{}: {}'.format(type(e).__name__, e))
    else:
        await bot.say('\U0001f44c')


if __name__ == '__main__':
    for extension in extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print('Failed to load extension {}\n{}: {}'.format(extension, type(e).__name__, e))
    with open("token.txt", "r") as file:
        token = file.readline()
    bot.run(token)
