import discord
from discord.ext import commands
import descriptions as desc
import checks
import tokens as t
from datetime import datetime

bot = commands.Bot(command_prefix='!', description=desc.main, pm_help=True)
extensions = [
    'cogs.giveaway',
    'cogs.general',
    'cogs.restricted',
    'cogs.stats',
    'cogs.weather',
    'cogs.swear',
    'cogs.overwatch',
]


@bot.event
async def on_ready():
    """After logging in"""
    print(bot.user.name + ' logged in at ' + str(datetime.now()))
    await bot.change_status(game=discord.Game(name='!help'))


@bot.event
async def on_message(message):
    if message.author is bot.user:
        return

    swear = bot.get_cog('Swear')

    if swear is not None:
        await swear.message(message)

    await bot.process_commands(message)


@bot.event
async def on_command(command, ctx):
    stats = bot.get_cog('Stats')

    if stats is not None:
        await stats.on_command_p(command.name)


@bot.command(hidden=True)
@checks.is_scream()
async def reload(*, module: str):
    """
    Reloads a module.

    :param module: Module to be reloaded, cogs.general -> from cogs folder general module
    """
    module = module.strip()

    try:
        bot.unload_extension(module)
        bot.load_extension(module)

    except Exception as e:
        await bot.say('\U0001f52b')
        await bot.say('{}: {}'.format(type(e).__name__, e))

    else:
        await bot.say('\U0001f44c')


@bot.command(hidden=True)
@checks.is_scream()
async def load(*, module: str):
    """
    Loads a module.

    :param module: Module to be loaded, cogs.general -> from cogs folder general module
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

    bot.run(t.token)
