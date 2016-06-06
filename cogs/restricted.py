import os
import logging

import discord
from discord.ext import commands

from helpers import descriptions as desc, checks, settings

log = logging.getLogger(__name__)


class Restricted:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True, description=desc.iscream)
    @checks.is_scream()
    async def develop(self):
        await self.bot.say('iScrE4m is streaming my development over at http://twitch.tv/iScrE4m - come watch!')

    @commands.command(hidden=True, description="not for you")
    @checks.is_scream()
    async def avatar(self, image: str):
        try:
            with open("cogs/avatar/" + image, "rb") as avatar:
                f = avatar.read()
                image_bytes = bytearray(f)
                await self.bot.edit_profile(avatar=image_bytes)
                await self.bot.say("New avatar uploaded, how do you like me now?")
                log.info("Avatar updated")

        except Exception as e:
            log.exception("Couldn't change avatar")

    @commands.command(hidden=True, description=desc.iscream)
    @checks.is_scream()
    async def play(self, *, playing: str):
        await self.bot.change_status(game=discord.Game(name=playing))
        await self.bot.say("I'm now playing {}".format(playing))
        log.info("Now playing updated")

    @commands.command(pass_context=True, hidden=True, description=desc.iscream)
    @checks.is_scream()
    async def nick(self, ctx, *, nick: str):
        try:
            await self.bot.change_nickname(ctx.message.server.me, nick)
            await self.bot.say("I might have an identity crysis. New name accepted")
            log.info("New name updated")
        except Exception as e:
            log.exception("Couldn't change display name")

    @commands.command(description=desc.iscream)
    @checks.is_scream()
    async def update(self):
        version = self.bot.get_cog('Versioning')
        if version is not None:
            msg = "I have been updated! New version: {}\n\n```md\n{}```".format(
                version.version, version.changelog.split("_____")[0])
            await self.bot.send_message(self.bot.get_channel(settings.channels['general']), msg)

    @commands.command(hidden=True, pass_context=True, description=desc.rtfh, brief=desc.rtfhb)
    @checks.mod_or_permissions(manage_messages=True)
    async def rtfh(self, ctx, target: str, cmd: str):
        # RTFH stands for read the F***ing help
        # Not using @commands.group because we want to have one command for both commands and subcommands
        # Known bug: '!rtfh help' doesn't send full 'help' properly

        ctx.message.author = ctx.message.mentions[0]
        msg = ctx.message.content.split()

        try:
            subcmd = msg[3]
            await commands.bot._default_help_command(ctx, cmd, subcmd)

        except IndexError:
            await commands.bot._default_help_command(ctx, cmd)

    @commands.command(hidden=True, description=desc.idiotech)
    @checks.is_idiotech()
    async def dance(self):
        await self.bot.say('Moves like Jagger I tell you')

    @commands.command(hidden=True, description=desc.idiotech)
    @checks.is_idiotech()
    async def log(self, users: str):
        # TODO Discuss what to do with this comand, it's not being used much
        users = users.split(';')
        public = self.bot.get_channel(settings.channels['general'])
        admin = self.bot.get_channel(settings.channels['admin'])
        with open("log.txt", "w", encoding='utf-8') as logfile:
            async for msg in self.bot.logs_from(public, limit=500):
                if msg.author.name in users:
                    string = "[{}] {}: {}\n".format(msg.timestamp, msg.author.name, msg.clean_content)
                    logfile.write(string)

        with open("log.txt", "rb") as logfile:
            await self.bot.send_file(admin, logfile, filename="log.txt",
                                     content="Log file for mentioned users from last 500 messages in public channel.")
        os.remove("log.txt")
        log.info("Log file sent to admins for review")


def setup(bot):
    bot.add_cog(Restricted(bot))
