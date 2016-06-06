import logging

from discord.ext import commands

from helpers import descriptions as desc, simplify as s

log = logging.getLogger(__name__)


class Versioning:
    """
    This versioning system probably isn't perfect, but since this is not a pip package,
    I didn't find any good practices online. I'm open to discussion
    """
    version = ""
    changelog = ""

    def __init__(self, bot):
        self.bot = bot

        with open('cogs/versioning/changelog.md', 'r') as changes:
            Versioning.changelog = changes.read()
            log.debug("Changelog loaded from file")

        with open('cogs/versioning/version.txt', 'r') as v:
            Versioning.version = v.readline()
            log.debug("version loaded from file")

    @commands.command(name='version', description=desc.v_command, brief=desc.v_command)
    async def v(self):
        await self.bot.say("Current version: {}".format(Versioning.version))

    @commands.command(name='changelog', pass_context=True, description=desc.changelog, brief=desc.changelog)
    async def chlog(self, ctx):
        # Test that your markdown looks pretty in ```md``` tag in Discord
        # Split minor versions (major.minor.patch.bugfixes) with '** **'
        # Always split the latest changes with '_____' (and remove it from previous position
        chlog = "```md\n{0}```".format(Versioning.changelog.split("** **")[0])
        await s.whisper(ctx.message.author, chlog, self.bot)


def setup(bot):
    bot.add_cog(Versioning(bot))
