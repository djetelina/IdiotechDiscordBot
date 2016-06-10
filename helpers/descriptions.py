"""
Description strings
"""

try:
    with open('cogs/versioning/version.txt', 'r') as v:
        version = " (v{})".format(v.readline())
except:
    version = ""

main = """Bot for Idiotech's Discord{}

Owner: iScrE4m
Contributors: Extra_Random, Otter
Source code: https://github.com/iScrE4m/IdiotechDiscordBot
Request a feature: https://github.com/iScrE4m/IdiotechDiscordBot/issues

Commands can have subcommands, you can type !help for those too
For example: !help giveaway open""".format(version)

"""
GIVEAWAY RELATED
"""

openga = """Open a giveaway

Maximum is 30 minutes (if you provide higher countdown, it will launch with 30 minutes.

Example: !giveaway open 30 Overwatch"""
opengab = "Open a giveaway"

cancelga = "Cancel your giveaway for a game"
cancelgab = "Cancel a giveaway"

enroll = """Enroll in a existing giveaway

Example: !enroll Audiosurf 2
"""
enroll_brief = "Enroll in a giveaway"

giveaway = """Check status of running giveaways

Example: !giveaway"""
giveaway_brief = "Check status of running giveaways"

link_ga = """If you want to add a link to the game's page (like steam url) please use:
This message will show once after you open the giveaway:"""
link_ga_brief = "Provide a link for your prepared giveaway. This is NOT "

code_ga = """Provide a code for your prepared or running giveaway

It will be sent to the winner after the giveaway is over in this format:
`Your game code: <GAMECODE>`

You can also specify if your game code is Steam, origin, etc. or add any note.
Simply write anything before or after the code, your whole message after `!giveaway code` will be sent
"""
code_ga_brief = "Provide a code for your prepared or running giveaway"

desc_ga_brief = "Provide a description for your prepared giveaway"
# noinspection PyPep8
desc_ga = """If you want to say more about the game or a giveaway, like where is it redeemable, if you are also giving away DLC with it etc.
You can also include url here instead of using the previous command
This message will show once after you open the giveaway:"""

confirm_ga = "Start your prepared giveaway"

"""
HIDDEN COMMANDS (only used by some)
"""

iscream = "Only available for iScrE4m"
idiotech = "Only available for Idiotech"
rtfh = """Force a person to read !help for a command
It will PM them the result of !help
Mention the person, or the bot will not know who's your target
Also available for subcommands

Example: !rtfh @Idiotech giveaway open
"""
rtfhb = "Force a person to read !help for a command"

"""
SIMPLE LINKS
"""

reddit = "Link to Idiotech's subreddit"
github = "Link to this bot's source code"
twitch = """Status of Idiotech's Twitch

If Idiotech is live, viewer count and the game he is playing will be shown."""
twitchb = "Status of Idiotech's Twitch"
twitter = "Link to Idiotech's Twitter"
youtube = "Link to Idiotech's Channel and Details of most recent upload"
fb = "Link to Idiotech's Facebook, also shows latest post"
rules = "READ THE RULES!"

"""
Utility commands
"""

time = "Check local times over the world"
time_advanced = "Checks local time over the world and their UTC positions"
time_sydney = "Checks local time in Sydney and it's UTC position"
time_london = "Checks local time in London and it's UTC position"
time_ny = "Checks local time in New York and it's UTC position"
time_sf = "Checks local time in San Francisco and it's UTC position"
time_perth = "Checks local time in Perth and its UTC position"
release_dates = """List of games and countdown until their releases

If you provide additional argument, it will look through list of games and find those starting with provided argument
"""

"""
GAMES
"""

release_datesb = "List of games and countdown until their releases"
steam = "Commands related to steam"
steam_status = "Check Status of Steam Servers"
steam_bs = "List of Top 5 Best selling steam games"
steam_sales = "PM's you a list of games currently on sale on Steam"

ow = """Find Overwatch Stats of a given battle tag in a given region

Example: !overwatch eu ExtraRandom#2501
"""
owb = "Find Overwatch Stats for a battle tag"

game = "Lists people currently plying games within the community"
open_game = "Open a game for community to play with you"
game_desc = """Provide a description for your community game

This is useful for telling people how to join you, where are you playing, who to add on steam/battle.net etc.
"""
game_desc_b = "Provide a description for your community game"
game_close = "Close your community game"
game_join = "Join a community game"
game_leave = "Leave a community game"

"""
STATS
"""

stats = "I'll show you how much you need me!"
statsga = "I'll show you how much giveaways I helped you organize"

"""
VERSIONING
"""

v_command = "My version number"
changelog = "My latest changes"
