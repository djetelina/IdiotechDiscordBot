import logging

import discord
from discord.ext import commands

import helpers.tokens as t
from helpers import descriptions as desc, checks, settings

bot = commands.Bot(command_prefix='!', description=desc.main, pm_help=True)


@bot.event
async def on_ready():
    log.info(bot.user.name + ' logged in')
    await bot.change_status(game=discord.Game(name=settings.now_playing))


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
    try:
        log.info("#{2}: {1} called {0}".format(command.name, ctx.message.author.name, ctx.message.channel.name))
    except AttributeError:
        log.info("PM: {1} called {0}".format(command.name, ctx.message.author.name))

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
    log = logging.getLogger()
    log.setLevel(logging.INFO)
    console = logging.StreamHandler()
    log_file = logging.FileHandler('log.log', 'w', 'utf-8')

    console.setLevel(logging.INFO)
    log_file.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', "%d.%m.%Y %H:%M:%S")
    console.setFormatter(formatter)
    log_file.setFormatter(formatter)

    log.addHandler(log_file)
    log.addHandler(console)

    for extension in settings.extensions:
        try:
            bot.load_extension(extension)
            log.info('{} loaded'.format(extension))

        except Exception as e:
            log.warning('Failed to load extension {}\n{}: {}'.format(extension, type(e).__name__, e))

    bot.run(t.token)
