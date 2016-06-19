# Idiotech's Discord Bot

[![Build Status](https://travis-ci.org/iScrE4m/IdiotechDiscordBot.svg?branch=master)](https://travis-ci.org/iScrE4m/IdiotechDiscordBot) [![MIT Licence](https://badges.frapsoft.com/os/mit/mit.svg?v=103)](https://opensource.org/licenses/mit-license.php) [![Code Climate](https://codeclimate.com/github/iScrE4m/IdiotechDiscordBot/badges/gpa.svg)](https://codeclimate.com/github/iScrE4m/IdiotechDiscordBot) [![Test Coverage](https://codeclimate.com/github/iScrE4m/IdiotechDiscordBot/badges/coverage.svg)](https://codeclimate.com/github/iScrE4m/IdiotechDiscordBot/coverage)  

Bot for [Idiotech's Discord Server](https://discord.gg/0z3KQXI6apyyeNOD)

## Rules for developing

* Don't collect any longterm user information (not even chat logs)
* Make your code readable by humans
* Document if you can
* Use pep8 with 120 max-length (PyCharm recommended)

## Request a feature

To request a feature please use [issue tracker](https://github.com/iScrE4m/IdiotechDiscordBot/issues)

## Run your testing branch

* Create Discord app and bot user [here](https://discordapp.com/developers/applications/me)
* Setup [Heroku](https://www.heroku.com/)
* Run heroku addons:create heroku-postgresql:hobby-dev
* Create config variables based on helpers/tokens.py
* Run remote through Heroku (heroku ps:scale worker=1)

### Local
* Install Python 3.5+
* Run ```pip install -r requirements.txt```
* Create .env file with local variables
* Create local Postgresql db and add it to .env as DATABASE_URL
* Run using `heroku local` (if you have Heroku set up) or `foreman start` (https://github.com/vlucas/phpdotenv)
    * If you are on linux using autoenv, you can `python main.py` from your env
