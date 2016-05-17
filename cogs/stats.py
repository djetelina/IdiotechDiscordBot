from discord.ext import commands
import simplify as s
import descriptions as desc
import sqlite3
import os

class Stats:
    def __init__(self, bot):
        self.bot = bot
        self.db_path = os.path.join(os.getcwd(), "cogs/db/stats.db")
        self.database = sqlite3.connect(self.db_path , timeout=1)
        self.database.row_factory = sqlite3.Row
        self.db = self.database.cursor()
        self.sessioncmd = 0
        self.sessionga = 0

    async def on_command_p(self, command: str):
        self.sessioncmd += 1
        if self.is_in_db("cmd", command):
            self.command_increase(command)
        else:
            self.new_entry("cmd", command)

    async def on_giveaway(self, game: str):
        self.sessionga += 1
        if self.is_in_db("ga", game):
            self.ga_increase(game)
        else:
            self.new_entry("ga", game)

    @commands.group(pass_context=True, descirption=desc.stats, brief=desc.stats)
    async def stats(self, ctx):
        if ctx.invoked_subcommand is None:
            await s.destructmsg(
                "I have served you {} commands in my lifetime and {} since I was last restarted".format(
                self.get_total("cmd"), self.sessioncmd), 30, self.bot)

    @stats.command(name="giveaways", description=desc.statsga, brief=desc.statsga)
    async def _giveaways(self):
        await s.destructmsg("I have helped give out {} games and {} since I was last restarted".format(
            self.get_total("ga"), self.sessionga), 30, self.bot)

    def is_in_db(self, table, check):
        if table is "ga":
            table_name = "giveaways"
            column = "game"
        elif table is "cmd":
            table_name = "commands"
            column = "command"
        else:
            print("DB error is_in_db")
            return
        query = """
        SELECT 1
        FROM {0}
        WHERE {1} = ?
        COLLATE NOCASE
        """.format(table_name, column)
        self.db.execute(query, (check,))
        entry = self.db.fetchone()
        return entry is not None

    def new_entry(self, table, entry):
        if table is "ga":
            table_name = "giveaways"
            column = "game"
        elif table is "cmd":
            table_name = "commands"
            column = "command"
        else:
            print("DB error new_entry")
            return
        query = """
        INSERT INTO {0}
        ({1})
        VALUES (?)
        """.format(table_name, column)
        entry = entry.lower()
        self.db.execute(query, (entry,))
        self.database.commit()

    def command_increase(self, command):
        query = """
        UPDATE commands
        SET
          used = used + 1
        WHERE command = ?
        """
        command = command.lower()
        self.db.execute(query, (command,))
        self.database.commit()

    def ga_increase(self, game):
        query = """
        UPDATE giveaways
        SET
          given = given +1
        WHERE game = ?
        """
        game = game.lower()
        self.db.execute(query, (game,))
        self.database.commit()

    def get_total(self, table):
        if table is "ga":
            table_name = "giveaways"
            column = "given"
        elif table is "cmd":
            table_name = "commands"
            column = "used"
        else:
            print("DB error get_total")
            return
        query = """
        SELECT SUM({0}) AS TOTAL
        FROM {1}
        """.format(column, table_name)
        self.db.execute(query)
        return str(self.db.fetchone()[0])

def setup(bot):
    bot.add_cog(Stats(bot))
