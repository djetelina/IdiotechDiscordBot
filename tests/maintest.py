import unittest
from main import bot
from helpers import settings

class CogsTest(unittest.TestCase):

    def test_general(self):
        try:
            bot.load_extension('cogs.general')
        except Exception:
            self.fail()

    def test_giveaway(self):
        try:
            bot.load_extension('cogs.giveaway')
        except Exception:
            self.fail()

    def test_restricted(self):
        try:
            bot.load_extension('cogs.restricted')
        except Exception:
            self.fail()

    def test_versioning(self):
        try:
            bot.load_extension('cogs.versioning')
        except Exception:
            self.fail()

    def test_games(self):
        try:
            bot.load_extension('cogs.games')
        except Exception:
            self.fail()

    def test_spamfilter(self):
        try:
            bot.load_extension('cogs.spamfilter')
        except Exception:
            self.fail()

    def test_currency(self):
        try:
            bot.load_extension('cogs.currency')
        except Exception:
            self.fail()

    def test_stats(self):
        try:
            bot.load_extension('cogs.stats')
        except Exception:
            self.fail()

if __name__ == '__main__':
    unittest.main()