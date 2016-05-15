from discord.ext import commands
import checks
import descriptions as desc


class Restricted:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True, description=desc.iscream)
    @checks.is_scream()
    async def develop(self):
        await self.bot.say('iScrE4m is streaming my development over at http://twitch.tv/iScrE4m - come watch!')

    @commands.command(hidden=True, description=desc.idiotech)
    @checks.is_idiotech()
    async def dance(self):
        await self.bot.say('Moves like Jagger I tell you')


    """
    @commands.command(pass_context=True, hidden=True, description=desc.findlast)
    async def findlast(self, ctx):
        user = ctx
        # this will search all channels for specified user's last message, and post it in channel it was called from
    """

    @commands.command(pass_context=True, hidden=True, description=desc.idiotech)
    @checks.is_idiotech()
    async def log(self, ctx):
        users = " ".join(ctx.message.content.split(' ')[1:]).split(';')
        public = ctx.message.server.get_channel("176293292865093632")
        admin = ctx.message.server.get_channel("176304607172100097")
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
