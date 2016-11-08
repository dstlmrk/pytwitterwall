#!/usr/bin/env python3.4
# coding=utf-8

import requests
import base64
import sys
import time
import configparser
from jinja2 import Markup


class Twitterwall(object):
    ''''''

    def __init__(self, api_key=None, api_secret=None,
                 initial_count=15, retweets_are_allowed=True, session=None):
        self.session = session
        self._create_session(api_key, api_secret)
        self.initial_count = initial_count
        self.retweets_are_allowed = retweets_are_allowed

    @staticmethod
    def get_credentials(config_path):
        '''
        Parse api key and api secret from config file.
        '''
        config = configparser.ConfigParser()
        config.read(config_path)
        try:
            api_key = config['twitter']['key']
            api_secret = config['twitter']['secret']
        except Exception as e:
            print("Your config file is invalid, check README")
            sys.exit(1)
        return api_key, api_secret

    def _create_session(self, api_key, api_secret):
        '''
        Create session if it still doesn't exists.
        In all cases gets token for next requests.
        '''
        def bearer_auth(req):
            req.headers['Authorization'] = 'Bearer ' + bearer_token
            return req

        session = self.session or requests.Session()
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

        if 400 <= r.status_code < 600:
            for error in r.json()['errors']:
                print(error['message'])
            sys.exit(1)

        bearer_token = r.json()['access_token']
        session.auth = bearer_auth
        self.session = session

    def search_tweets(self, query, since_id=0, **params):
        params['q'] = query
        params['since_id'] = since_id
        return self.session.get(
            'https://api.twitter.com/1.1/search/tweets.json', params=params
        )

    def _print_tweets(self, statuses):
        for status in statuses:
            if status.get('retweeted_status')\
            and not self.retweets_are_allowed:
                continue
            else:
                print(status['text'] + "\n----------")

    def infinite_loop(self, query, loop):
        print("----------")
        resp = self.search_tweets(query, count=self.initial_count)
        self._print_tweets(resp.json()['statuses'])
        since_id = resp.json()["search_metadata"]["max_id"]

        while 1:
            resp = self.search_tweets(query, since_id)
            self._print_tweets(resp.json()['statuses'])
            # offset
            since_id = resp.json()["search_metadata"]["max_id"]
            time.sleep(loop)

    @staticmethod
    def get_indices(entity):
        return entity['indices'][0], entity['indices'][1]

    @staticmethod
    def add_hashtag(tweet, entity):
        first_c, last_c = Twitterwall.get_indices(entity)
        hashtag_text = tweet[first_c:last_c]
        hashtag = Markup('<a href=\"/search/{}\">{}</a>').format(
            hashtag_text[1:], hashtag_text
        )
        return Markup(tweet[0:first_c]) + hashtag + Markup(tweet[last_c:])

    @staticmethod
    def add_user_mention(tweet, entity):
        first_c, last_c = Twitterwall.get_indices(entity)
        user_mention_text = tweet[first_c:last_c]
        user_mention = Markup('<a href=\"/search/{}\">{}</a>').format(
            user_mention_text[1:], user_mention_text
        )
        return (
            Markup(tweet[0:first_c]) + user_mention + Markup(tweet[last_c:])
        )

    @staticmethod
    def add_url(tweet, entity):
        first_c, last_c = Twitterwall.get_indices(entity)
        url = Markup('<a href=\"{}\">{}</a>').format(
            entity['expanded_url'], entity['display_url']
        )
        return Markup(tweet[0:first_c]) + url + Markup(tweet[last_c:])

    @staticmethod
    def add_media(tweet, entity):
        first_c, last_c = Twitterwall.get_indices(entity)
        media = Markup('<br><br><a href="{}"><img src="{}"></a>').format(
            entity['expanded_url'], entity['media_url']
        )
        return Markup(tweet[0:first_c]) + media + Markup(tweet[last_c:])
