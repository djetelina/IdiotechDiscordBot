import asyncio

async def destructmsg(msg, seconds, bot):
    """
    Send autodestructive message to channel of original message

    :param msg:     String
    :param seconds: Integer of seconds after which to delete the message
    :param bot:     Bot instance
    """
    message = await bot.say(msg)
    await asyncio.sleep(seconds)
    await bot.delete_message(message)


async def whisper(user, msg, bot):
    """
    Send private message to a user

    :param user: User object
    :param msg:  String
    :param bot:  Bot Instance
    """
    await bot.start_private_message(user)
    await bot.send_message(user, msg)
