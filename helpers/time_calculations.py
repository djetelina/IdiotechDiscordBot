from datetime import datetime
import time


def create_msg(game, days, hrs, mins, maxlen):
    spaces = maxlen - len(game) + 30
    for _ in range(spaces):
        game += " "
    if int_day(days) < 0:  # if hours is a minus (i.e. game is released)
        msg = "{} is out now!".format(game)
    elif int_day(days) == 0 and int(hrs) == 0 and int(mins) == 0:
        msg = "{} releases within the next 60 seconds, HYPE!!!".format(game)
    else:
        msg = "{} {}, {} hours {} minutes".format(game, days, hrs, mins)

    return msg


def int_day(day):
    """
    Takes day as string ('3 days') and returns just the number as an integer
    :param day:
    :return:
    """
    day, word = day.split(" ")
    return int(day)


def get_date_suf(day):
    # Get the suffix to add to date ('st' for 1, 'nd' for 2 and so on) code from http://stackoverflow.com/a/5891598
    if 4 <= int(day) <= 20 or 24 <= int(day) <= 30:
        suffix = "th"
    else:
        suffix = ["st", "nd", "rd"][int(day) % 10 - 1]
    return suffix


def date_split(date):
    """
    Returns the given datetime as three strings: year, month and day

    :param date: The datetime to split into year, month and day
    :return: year, month, day
    """

    to_split = str(date).split('T')[0]
    year, month, day = to_split.split('-')

    return year, month, day


def date_now():
    """
    Returns the date now as three strings: year, month and day

    :return: year, month, day
    """

    now = datetime.utcnow()
    date, no_date = str(now).split(' ')
    year, month, day = date.split('-')

    return year, month, day


def calc_until(rd):
    """
    Calculates the amount of time between now and 'rd'

    :param rd:  release date as datetime()
    :return:    three strings with time left
    """

    t_delta = rd - datetime.utcnow()
    t_str = str(t_delta)

    test_var = t_str.split(".")[0]
    if len(test_var) == 7 or len(test_var) == 8:
        days = "0 days"
        hrs, minutes, secs = test_var.split(":")
    elif len(test_var) == 5 or len(test_var) == 4:
        days = "0 days"
        hrs = "0"
        minutes, secs = test_var.split(":")
    elif len(test_var) == 1 or len(test_var) == 2:
        days = "0 days"
        hrs = "0"
        minutes = "0"
    else:
        days, no_days = t_str.split(",")
        hrs, minutes, secs = no_days.split(":")

    hrs = hrs.strip()  # removes spaces in string

    return days, hrs, minutes


def calc_duration(start):
    """
    Calculates the amount of time between 'start' and now

    :param start:  Datetime
    :return:    three strings with time passed
    """

    tdelta = datetime.utcnow() - start
    tstr = str(tdelta)

    hrs, mins, secs = tstr.split(":")
    secs = secs.split(".")[0]

    return hrs, mins, secs


def parsesecs(sec: int) -> str:
    """
    Parses seconds into time left format
    This is to be used only for giveaway which have limit of 30 minutes

    :param sec: number of seconds
    :return:    string with time left
    """
    if sec >= 120:
        tleft = time.strftime("%M minutes left", time.gmtime(sec)).lstrip('0')
    elif sec >= 60:
        tleft = time.strftime("%M minute left", time.gmtime(sec)).lstrip('0')
    else:
        tleft = time.strftime("%S seconds left", time.gmtime(sec)).lstrip('0')

    return tleft
