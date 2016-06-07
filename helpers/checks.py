from discord.ext import commands
import discord.utils
from helpers import settings


def is_server_owner():
    """
    Checks if user requesting a command is Idiotech, if not command will not execute

    Usage: wrapper of command
    """

    def predicate(ctx):
        return ctx.message.author.id == settings.owner_id

    return commands.check(predicate)


def is_dev():
    """
    Checks if user requesting a command is iScrE4m, if not command will not execute

    Usage: wrapper of command
    """

    def predicate(ctx):
        return ctx.message.author.id == settings.dev_id

    return commands.check(predicate)


"""
DANNY'S PERMS
"""


def is_owner_check(message):
    return message.author.id == settings.owner_id


def is_owner():
    return commands.check(lambda ctx: is_owner_check(ctx.message))


def check_permissions(ctx, perms):
    msg = ctx.message
    if is_owner_check(msg):
        return True

    ch = msg.channel
    author = msg.author
    resolved = ch.permissions_for(author)
    return all(getattr(resolved, name, None) == value for name, value in perms.items())


def role_or_permissions(ctx, check, **perms):
    if check_permissions(ctx, perms):
        return True

    ch = ctx.message.channel
    author = ctx.message.author
    if ch.is_private:
        return False  # can't have roles in PMs

    role = discord.utils.find(check, author.roles)
    return role is not None


def mod_or_permissions(**perms):
    def predicate(ctx):
        return role_or_permissions(ctx, lambda r: r.name in ('Epic', 'Legendary'), **perms)

    return commands.check(predicate)


def admin_or_permissions(**perms):
    def predicate(ctx):
        return role_or_permissions(ctx, lambda r: r.name == 'Bot Admin', **perms)

    return commands.check(predicate)
