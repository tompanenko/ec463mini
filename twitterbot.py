import botometer
import requests
import json
from flask import Flask
from decouple import config
from google.cloud import language_v1

def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2RecentSearchPython"
    return r

def connect_to_endpoint(url, params):
    response = requests.get(url, auth=bearer_oauth, params=params)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()



# app = Flask(__name__)


# @app.route('/')
# def hello():
#     return 'Hello, World!'

# if __name__ == '__main__':
#   app.run(debug=True)

rapidapi_key = config('rapidapi_key', default='')
consumer_key = config('consumer_key', default='')
consumer_secret = config('consumer_secret', default='')
access_token = config('access_token', default='')
access_token_secret = config('access_token_secret', default='')
bearer_token = config('bearer_token',default='')



# Instantiates a client
client = language_v1.LanguageServiceClient()



twitter_app_auth = {
    'consumer_key': consumer_key,
    'consumer_secret': consumer_secret,
    'access_token': access_token,
    'access_token_secret': access_token_secret
  }
bom = botometer.Botometer(wait_on_ratelimit=True,
                          rapidapi_key=rapidapi_key,
                          **twitter_app_auth)

while(1):
    account = input("Enter a twitter account to analyze, or 'q' to quit (e.g. '@elonmusk' or 'elonmusk'): ")
    if account == 'q': break
    if account[0] == '@': account = account[1:]
    try:
        result = bom.check_account('@'+account)
    except:
        print("This account wasn't found\n")
        continue
    
    print("Analyzing the language in this account's tweets gives this account a " + str(result['display_scores']['english']['overall']) + "/5.0 on our bot scale")
    print(str(round(100*result['cap']['english'],2))+'% of accounts with this bot score or higher are known to be automated.')
    print("Analyzing other features of this account gives this account a " + str(result['display_scores']['universal']['overall']) + "/5.0 on our bot scale")
    print(str(round(100*result['cap']['universal'],2))+'% of accounts with this bot score or higher are known to be automated.')

    search_url = "https://api.twitter.com/2/tweets/search/recent"

    # Optional params: start_time,end_time,since_id,until_id,max_results,next_token,
    # expansions,tweet.fields,media.fields,poll.fields,place.fields,user.fields
    query_params = {'query': '(from:'+account+' -is:retweet -is:reply)','tweet.fields': 'author_id'}

    try:
        json_response = connect_to_endpoint(search_url, query_params)
        tweets = json_response["data"]
    except:
        print("This account has no recent tweets.\n")
        continue

    print("\nThe latest tweets by this account are:\n")
    for idx,tweet in enumerate(tweets):

        # The text to analyze
        text = tweet["text"]
        document = language_v1.Document(
            content=text, type_=language_v1.Document.Type.PLAIN_TEXT
        )

        # Detects the sentiment of the text
        sentiment = client.analyze_sentiment(
            request={"document": document}
        ).document_sentiment

        print(str(idx+1)+".\n"+tweet["text"])
        print("Sentiment score: {}\n".format(sentiment.score))

    
