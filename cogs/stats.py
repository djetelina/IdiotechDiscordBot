import os
import logging
import psycopg2
from urllib import parse

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

from discord.ext import commands

from helpers import descriptions as desc

Base = declarative_base()

class CommandsDB(Base):
    __tablename__= "commands"
    id = Column(Integer, primary_key=True)
    command = Column(String(250), nullable=False)
    used = Column(Integer, default=1)

class GiveawaysDB(Base):
    __tablename__="giveaways"
    id = Column(Integer, primary_key=True)
    game = Column(String(250), nullable=False)
    given = Column(Integer, default=1)



class Stats:
    def __init__(self, bot):
        self.bot = bot
        logging.info(os.environ.get("DATABASE_URL"))
        self.engine = create_engine("postgres://", creator=self.connect, echo=True)
        if not database_exists(self.engine.url):
            logging.info("Database not found")
            create_database(self.engine.url)
            logging.info("Database created")
        Base.metadata.create_all(self.engine)
        Base.metadata.bind= self.engine
        self.Session = sessionmaker(bind=self.engine)
        self.db = self.Session()
        self.sessioncmd = 0
        self.sessionga = 0

    def connect(self):
        logging.info("connect called")
        parse.uses_netloc.append("postgres")
        url = parse.urlparse(os.environ["DATABASE_URL"])
        logging.info(url)
        logging.info(url.path)
        logging.info(url.username)
        logging.info(url.password)
        logging.info(url.hostname)
        logging.info(url.port)


        return psycopg2.connect(database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )

    async def on_command_p(self, command: str):
        self.sessioncmd += 1

        if self.db.query(CommandsDB).filter(CommandsDB.command == command).count():
            self.db.query(CommandsDB).filter(CommandsDB.command == command). \
                update({CommandsDB.used: CommandsDB.used + 1})
        else:
            self.db.add(CommandsDB(command=command))

        self.db.commit()

    async def on_giveaway(self, game: str):
        self.sessionga += 1

        if self.db.query(GiveawaysDB).filter(GiveawaysDB.game == game).count():
            self.db.query(GiveawaysDB).filter(GiveawaysDB.game == game).\
                    update({GiveawaysDB.given: GiveawaysDB.given + 1})
        else:
            self.db.add(GiveawaysDB(game=game))

        self.db.commit()

    @commands.group(pass_context=True, descirption=desc.stats, brief=desc.stats)
    async def stats(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.bot.say(
                "I have served you {} commands in my lifetime and {} since I was last restarted".format(
                    self.get_total("cmd"), self.sessioncmd))

    @stats.command(name="giveaways", description=desc.statsga, brief=desc.statsga)
    async def _giveaways(self):
        await self.bot.say("I have helped give out {} games and {} since I was last restarted".format(
            self.get_total("ga"), self.sessionga))


    def get_total(self, table):
        if table is "ga":
            all = self.db.query(GiveawaysDB).all()
            total = 0
            for one in all:
                total = total + one.used
            return total

        elif table is "cmd":
            all = self.db.query(CommandsDB).all()
            total = 0
            for one in all:
                total = total + one.used
            return total

        else:
            logging.warning("DB error get_total")
            return


def setup(bot):
    bot.add_cog(Stats(bot))
