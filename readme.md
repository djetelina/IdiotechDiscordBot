# Idiotech's Discord Bot

[![Build Status](https://travis-ci.org/iScrE4m/IdiotechDiscordBot.svg?branch=master)](https://travis-ci.org/iScrE4m/IdiotechDiscordBot) [![MIT Licence](https://badges.frapsoft.com/os/mit/mit.svg?v=103)](https://opensource.org/licenses/mit-license.php) [![Code Climate](https://codeclimate.com/github/iScrE4m/IdiotechDiscordBot/badges/gpa.svg)](https://codeclimate.com/github/iScrE4m/IdiotechDiscordBot) [![Test Coverage](https://codeclimate.com/github/iScrE4m/IdiotechDiscordBot/badges/coverage.svg)](https://codeclimate.com/github/iScrE4m/IdiotechDiscordBot/coverage)  

Bot for [Idiotech's Discord Server](https://discord.gg/0z3KQXI6apyyeNOD)

## Rules for developing

* Don't collect any longterm user information (not even chat logs)
* Make your code readable by humans
* Document if you can

## Request a feature

To request a feature please use [issue tracker](https://github.com/iScrE4m/IdiotechDiscordBot/issues)

## Run your testing branch

* Create Discord app and bot user [here](https://discordapp.com/developers/applications/me)
* Setup [Heroku](https://www.heroku.com/)
* Create config variables based on helpers/tokens.py
* Run remote through Heroku (heroku ps:scale worker=1)

### Local
* Install Python 3.5+
* Run ```pip install -r requirements.txt```
* Create .env file (you can skip the next step if you are on linux using autoenv, just run python main.py then)
* Run using `heroku local` (if you have Heroku set up) or `foreman start` (https://github.com/vlucas/phpdotenv)
