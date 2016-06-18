import os


"""
Found here: https://discordapp.com/developers/applications/me
The token for the Discord Bot, Will require creating an Application.
The token is found under "APP BOT USER" and then "Token: "
"""
token = os.environ.get("DISCORD")

"""
First go here: https://developers.facebook.com/
Make an new App (basic set-up is fine, use communication as category)
Then go here: https://developers.facebook.com/tools/explorer/
To the top right you should see "Graph API Explorer", click that and select the app you just made.
After that click the "Get Token" button and then "Get App Token"
The string in the text box labeled "Access token" is your key
"""
fb_key = os.environ.get("FACEBOOK")

"""
Found here: https://console.developers.google.com/apis/library
Create a new project, then on the API overviews go to YouTube Data API and enable it.
Then go to Credentials and create an API Key there.
"""
yt_key = os.environ.get("YOUTUBE")

"""
Found here: https://home.openweathermap.org/api_keys
Sign up then go to profile and then 'API keys'
"""
weather_key = os.environ.get("WEATHER")