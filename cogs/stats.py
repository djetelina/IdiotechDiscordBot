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

    async def on_command_p(self, command: str):
        self.sessioncmd += 1
        if self.is_in_db(command):
            self.command_increase(command)
        else:
            self.new_entry(command)

    @commands.command(descirption=desc.stats, brief=desc.stats)
    async def stats(self):
        await s.destructmsg("I have served you {} commands in my lifetime and {} since I was last restarted".format(
            self.totalcmd(), self.sessioncmd
        ), 30, self.bot)

    def is_in_db(self, command):
        query = """
        SELECT 1
        FROM commands
        WHERE command = ?
        COLLATE NOCASE
        """
        self.db.execute(query, (command,))
        entry = self.db.fetchone()
        return entry is not None

    def new_entry(self, command):
        query = """
        INSERT INTO commands
        (command)
        VALUES (?)
        """
        command = command.lower()
        self.db.execute(query, (command,))
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

    def totalcmd(self):
        query = """
        SELECT SUM(used) AS TOTAL
        FROM commands
        """
        self.db.execute(query)
        return str(self.db.fetchone()[0])

def setup(bot):
    bot.add_cog(Stats(bot))
