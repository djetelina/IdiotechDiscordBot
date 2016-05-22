from discord.ext import commands
import checks
import descriptions as desc
import channels as chan
import discord


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

        except Exception as e:
            await self.bot.say("Error: {}".format(e))

    @commands.command(hidden=True, description="not for you")
    @checks.is_scream()
    async def play(self, *, playing: str):
        await self.bot.change_status(game=discord.Game(name=playing))

    @commands.command(pass_context=True, hidden=True, description="not for you")
    @checks.is_scream()
    async def nick(self, ctx, *, nick: str):
        await self.bot.change_nickname(ctx.message.server.me, nick)

    @commands.command(hidden=True, pass_context=True, description=desc.rtfh, brief=desc.rtfhb)
    @checks.mod_or_permissions(manage_messages=True)
    async def rtfh(self, ctx, target: str, cmd: str):
        """
        RTFH stands for read the F***ing help

        Not using @commands.group because we want to have one command for both commands and subcommands

        Known bug: '!rtfh help' doesn't send full 'help' properly
        """
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
        users = users.split(';')
        public = self.bot.get_channel(chan.channels['public'])
        admin = self.bot.get_channel(chan.channels['admin'])
        with open("log.txt", "w", encoding='utf-8') as logfile:
            async for msg in self.bot.logs_from(public, limit=500):
                if msg.author.name in users:
                    string = "[{}] {}: {}\n".format(msg.timestamp, msg.author.name, msg.clean_content)
                    logfile.write(string)

        with open("log.txt", "rb") as logfile:
            await self.bot.send_file(admin, logfile, filename="log.txt",
                                     content="Log file for mentioned users from last 500 messages in public channel.")


def setup(bot):
    bot.add_cog(Restricted(bot))
