#!/usr/bin/env python3.4
# coding=utf-8

import click
import requests
import configparser
import base64
import time


def get_twitter_session(api_key, api_secret):

    def bearer_auth(req):
        req.headers['Authorization'] = 'Bearer ' + bearer_token
        return req

    session = requests.Session()
    secret = '{}:{}'.format(api_key, api_secret)
    secret64 = base64.b64encode(secret.encode('ascii')).decode('ascii')
    headers = {
        'Authorization': 'Basic {}'.format(secret64),
        'Host': 'api.twitter.com',
    }
    r = session.post(
        'https://api.twitter.com/oauth2/token',
        headers=headers,
        data={'grant_type': 'client_credentials'}
    )
    bearer_token = r.json()['access_token']
    session.auth = bearer_auth
    return session


def get_config(config_path):
    config = configparser.ConfigParser()
    config.read(config_path)
    return config


def print_line():
    print("-"*10)


def print_tweet(tweet):
    print(tweet)
    print_line()


def search_tweets(session, query, since_id, **params):
    params['q'] = query
    params['since_id'] = since_id
    return session.get(
        'https://api.twitter.com/1.1/search/tweets.json', params=params
    )


@click.command()
@click.option(
    '-q', '--query',
    default="#python",
    prompt="Your query string",
    help='Query string.'
)
@click.option(
    '--conf',
    default="./conf/auth.cfg",
    help='Configuration path. Defaults to ./conf/auth.cfg.'
)
@click.option(
    '--count',
    default=15,
    help='Count of first tweets, up to a maximum of 100. Defaults to 15.'
)
@click.option(
    '--loop',
    default=5,
    help='How often tweets will be reloaded in seconds. Defaults to 5.'
)
@click.option(
    '--retweets/--no-retweets',
    default=True,
    help='Flag that shows retweets. Defaults to true.'
)
def twitterwall(query, conf, count, loop, retweets):
    """
    Simple program which reads posts from Twitter via its API.
    """
    config = get_config(conf)
    session = get_twitter_session(
        config['twitter']['key'],
        config['twitter']['secret']
    )

    since_id = 0
    print_line()

    while 1:
        resp = search_tweets(session, query, since_id, count=count)
        for tweet in resp.json()['statuses']:
            if tweet.get('retweeted_status') and not retweets:
                continue
            else:
                print_tweet(tweet['text'])
        # offset
        since_id = resp.json()["search_metadata"]["max_id"]
        time.sleep(loop)

if __name__ == '__main__':
    twitterwall()
