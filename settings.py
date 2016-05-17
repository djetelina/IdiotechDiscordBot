"""
DRAFT

Eventually we'll pull things from here. It is meant to easier change settings

Right now everything is still in it's place
"""

# Taken from main.py

# Which extensions to load on startup
extensions = ['cogs.giveaway', 'cogs.general', 'cogs.restricted', 'cogs.stats', ]
# Status message for bot
now_playing = "!help"


# Taken from giveaways.py

# Allow giveaways for these channels (don't forget to change descriptions.py
whitechannels = ['private', 'code']


# Not sure whether to have this in settings

# Used in giveaways and swear.py
import asyncio
loop = asyncio.get_event_loop()