import logging

from discord import errors

log = logging.getLogger(__name__)


class SpamFilter():
    def __init__(self, bot):
        self.bot = bot

    async def message(self, message):
        if not message.channel.is_private:
            if len(message.author.roles) == 1:
                if linkcheck(message.content):
                    log.info("Suspicious (spam) message from {0.author.name} indetified, deleting".format(message))
                    try:
                        await self.bot.delete_message(message)
                    except Exception as e:
                        log.exception("Can't delete the message")



def linkcheck(msg):
    no_space_msg = msg.replace(" ", "").lower()
    suspicious = ["http", "www", ".com", "://", "g2a"]
    for word in suspicious:
        if word in no_space_msg:
            return True


def setup(bot):
    bot.add_cog(SpamFilter(bot))