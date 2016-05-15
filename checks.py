from discord.ext import commands


def is_idiotech():
    """
    Checks if user requesting a command is Idiotech, if not command will not execute

    Usage: wrapper of command
    """

    def predicate(ctx):
        return ctx.message.author.id == "176291669254209539"

    return commands.check(predicate)


def is_scream():
    """
    Checks if user requesting a command is iScrE4m, if not command will not execute

    Usage: wrapper of command
    """

    def predicate(ctx):
        return ctx.message.author.id == "132577770046750720"

    return commands.check(predicate)