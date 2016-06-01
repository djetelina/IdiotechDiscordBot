"""
Description strings
"""

main = """Bot for Idiotech's Discord

Owner: iScrE4m
Contributors: Extra_Random, Otter
Source code: https://github.com/iScrE4m/IdiotechDiscordBot
Request a feature: https://github.com/iScrE4m/IdiotechDiscordBot/issues

Commands can have subcommands, you can type !help for those too
For example: !help giveaway open"""

"""
GIVEAWAY RELATED
"""

openga = """Open a giveaway for specified channel

Available channels:
    private

Example: !giveaway open private 30 Overwatch"""
opengab = "Open a giveaway"

cancelga = """Cancel your giveaway for a game

Arguments: Game name (only one)

Example: !giveaway cancel Doom
"""
cancelgab = "Cancel a giveaway"

enroll = """Enroll in a existing giveaway

Example: !enroll Audiosurf 2
"""
enrollb = "Enroll in a giveaway"

giveaway = """Check status of running giveaways

Example: !giveaway"""
giveawayb = "Check status of running giveaways"

linkga = "Provide a link for your prepared giveaway"

codega = """Provide a code for your prepared or running giveaway

It will be sent to the winner after the giveaway is over in this format:
`Your game code: <GAMECODE>`

You can also specify if your game code is Steam, origin, etc. or add any note.
Simply write anything before or after the code, your whole message after `!giveaway code` will be sent

Example: !giveaway code 123-ABC-356 (STEAM)
"""
codegab = "Provide a code for your prepared or running giveaway"

descga = "Provide a description for your prepared giveaway"

confirmga = "Start your prepared giveaway"

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
If Idiotech is live, viewer count and the
game he is playing will be shown."""
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

Example: !release over"""
release_datesb = "List of games and countdown until their releases"
steam_status = "Check Status of Steam Servers"

"""
STATS
"""

stats = "I'll show you how much you need me!"
statsga = "I'll show you how much giveaways I helped you organize"
