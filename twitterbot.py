import botometer
from flask import Flask
from decouple import config


# app = Flask(__name__)


# @app.route('/')
# def hello():
#     return 'Hello, World!'

rapidapi_key = config('rapidapi_key', default='')
consumer_key = config('consumer_key', default='')
consumer_secret = config('consumer_secret', default='')
access_token = config('access_token', default='')
access_token_secret = config('access_token_secret', default='')

twitter_app_auth = {
    'consumer_key': consumer_key,
    'consumer_secret': consumer_secret,
    'access_token': access_token,
    'access_token_secret': access_token_secret
  }
bom = botometer.Botometer(wait_on_ratelimit=True,
                          rapidapi_key=rapidapi_key,
                          **twitter_app_auth)

# Check a single account by screen name
result = bom.check_account('@elonmusk')

print("Analyzing the language in this account's tweets gives this account a " + str(result['display_scores']['english']['overall']) + "/5.0 on our bot scale")
print(str(round(100*result['cap']['english'],2))+'% of accounts with this bot score or higher are known to be automated.')
print("Analyzing other features of this account gives this account a " + str(result['display_scores']['universal']['overall']) + "/5.0 on our bot scale")
print(str(round(100*result['cap']['universal'],2))+'% of accounts with this bot score or higher are known to be automated.')
