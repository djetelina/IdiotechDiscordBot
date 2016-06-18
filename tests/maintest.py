import unittest
from main import bot
from helpers import settings

class CogsTest(unittest.TestCase):

    def test_load_cogs(self):
        for extension in settings.extensions:
            try:
                bot.load_extension(extension)
            except Exception as e:
                self.fail()

if __name__ == '__main__':
    unittest.main()