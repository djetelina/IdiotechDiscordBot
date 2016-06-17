import aiohttp
from discord.ext import commands
from helpers import descriptions as desc


class Currency:
    def __init__(self, bot):
        self.bot = bot
        # TODO Decide whether to use the full currency names somewhere or not
        self.currency = {"AUD": "A$",  # "Australian Dollar",
                         "BGN": "lev",  # "Bulgarian Lev",
                         "BRL": "R$",  # "Brazilian Real",
                         "CAD": "C$",  # "Canadian Dollar",
                         "CHF": "SFr",  # "Swiss Franc",
                         "CNY": "C¥",  # "Chinese Yuan",
                         "CZK": "Kč",  # "Czech Koruna",
                         "DKK": "Dkr",  # "Danish Krone",
                         "EUR": "€",  # "Euro",
                         "GBP": "£",  # "British Pound",
                         "HKD": "HK$",  # "Hong Kong Dollar",
                         "HRK": "kn",  # "Croatian Kuna",
                         "HUF": "Ft",  # "Hungarian Forint",
                         "IDR": "Rp",  # "Indonesian Rupiah",
                         "ILS": "₪",  # "Israeli New Sheqel",
                         "INR": "₹",  # "Indian Rupee",
                         "JPY": "J¥",  # "Japanese Yen",
                         "KRW": "S₩",  # "South Korean Won",
                         "MXN": "M$",  # "Mexican Peso",
                         "MYR": "RM",  # "Malaysian Ringgit",
                         "NOK": "Nkr",  # "Norwegian Krone",
                         "NZD": "NZ$",  # "New Zealand Dollar",
                         "PHP": "₱",  # "Philippine Peso",
                         "PLN": "zł",  # "Polish Zloty",
                         "RON": "lei",  # "Romanian Leu",
                         "RUB": "₽",  # "Russian Ruble",
                         "SEK": "Skr",  # "Swedish Krona",
                         "SGD": "S$",  # "Singapore Dollar",
                         "THB": "฿",  # "Thai Baht",
                         "TRY": "₺",  # "Turkish Lira",
                         "USD": "$",  # "US Dollar",
                         "ZAR": "R",  # "South African Rand"
                         }

    @commands.command(desc=desc.cc, brief=desc.cc)
    async def cc(self, amount: float, base: str, to: str):
        """
        example: `!cc 50 EUR USD`
        """
        base = base.upper()
        to = to.upper()
        amount = round(amount, 2)
        if base not in self.currency:
            await self.bot.say("Currency '{}' unavailable for conversion.".format(base))
            return

        if to not in self.currency:
            await self.bot.say("Currency '{}' unavailable for conversion.".format(to))
            return

        with aiohttp.ClientSession() as session:
            url = "http://api.fixer.io/latest?base={}".format(base)
            async with session.get(url) as resp:
                try:
                    data = await resp.json()
                    conversion = float(data["rates"][to])
                    converted = conversion * amount
                    result = round(converted, 2)
                    base_s = self.currency[base]
                    to_s = self.currency[to]

                    await self.bot.say("{}{} ({}) is {}{} ({})".format(amount, base_s, base, result, to_s, to))

                except Exception:
                    await self.bot.say("An error occurred whilst getting currencies. Check spellings.")
                    return


def setup(bot):
    bot.add_cog(Currency(bot))
