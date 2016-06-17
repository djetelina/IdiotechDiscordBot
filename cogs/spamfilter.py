import logging

log = logging.getLogger(__name__)


class SpamFilter:
    def __init__(self, bot):
        self.bot = bot

    async def message(self, message):
        if not message.channel.is_private:
            if len(message.author.roles) == 1:
                if linkcheck(message.content):
                    log.warning("Suspicious message from {0.author.name} identified, deleting."
                                "Message: {0.content}".format(message))
                    try:
                        await self.bot.delete_message(message)
                    except Exception as e:
                        log.exception("Can't delete the message")


def linkcheck(msg):
    no_space_msg = msg.replace(" ", "").lower()
    suspicious = ["http", "www", ".com", "://", "g2a", "dotcom", "kinguin", "youtu.be", "/channel/"]
    for word in suspicious:
        if word in no_space_msg:
            return True


def setup(bot):
    bot.add_cog(SpamFilter(bot))
