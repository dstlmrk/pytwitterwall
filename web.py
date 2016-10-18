#!/usr/bin/env python3.4
# coding=utf-8

from datetime import datetime
from flask import Flask, render_template
from jinja2 import Markup
from twitterwall import Twitterwall


app = Flask("twitterwall")


@app.route('/')
def index():
    name = "TwitterWall"
    info = (
        "If you want to search something, put your query string"
        " into url such as: /search/your-query-string"
    )
    return Markup('<h1>{}</h1><p>{}</p>').format(name, info)

def get_twitterwall():
    return app.config.get("twitterwall") or Twitterwall()

# TODO: pokud chci zpracovavat i hashtagy, musel bych
# vstup escapovat pres nejaky formular
@app.route('/search/<query>/')
def search(query=None):
    twitterwall = get_twitterwall()
    resp = twitterwall.search_tweets(
        query, count=twitterwall.initial_count
    )
    statuses = []
    for status in resp.json()['statuses']:
        if status.get('retweeted_status')\
        and not twitterwall.retweets_are_allowed:
            continue
        else:
            statuses.append(status)
    return render_template(
        'twitterwall.html', statuses=statuses, query=query
    )


@app.template_filter('img')
def img(src):
    return Markup('<img src="{}">').format(src)


@app.template_filter('convert_time')
def convert_time(text):
    """Convert the time format to a different one"""
    dt = datetime.strptime(text, '%a %b %d %H:%M:%S %z %Y')
    return dt.strftime('%H:%M - %d. %m. %Y')


@app.template_filter('get_tweet')
def get_tweet(status):
    """
    Projdu si vsechny znaky, najdu hashtagy, nahradim je
    a vratim cely tweet vcetne html.
    """
    retweeted_status = False
    if status.get("retweeted_status"):
        retweeted_status = True
        status = status["retweeted_status"]

    tweet = status['text']
    entities = []

    for hashtag in status['entities']['hashtags']:
        entities.append({
            "type": "hashtag",
            "indices": hashtag['indices']
        })

    for user_mention in status['entities']['user_mentions']:
        entities.append({
            "type": "user_mention",
            "indices": user_mention['indices']
        })

    for url in status['entities']['urls']:
        entities.append({
            "type": "url",
            "indices": url['indices'],
            "display_url": url['display_url'],
            "expanded_url": url['expanded_url']
        })

    for media in status['entities'].get('media') or []:
        entities.append({
            "type": "media",
            "indices": media['indices'],
            "media_url": media['media_url'],
            "expanded_url": media['expanded_url']
        })

    entities = sorted(
        entities, key=lambda entity: entity['indices'][0], reverse=True
    )

    for entity in entities:
        first_c = entity['indices'][0]
        last_c = entity['indices'][1]
        if entity['type'] == "hashtag":
            tweet = Twitterwall.add_hashtag(tweet, entity)
        elif entity['type'] == "user_mention":
            tweet = Twitterwall.add_user_mention(tweet, entity)
        elif entity['type'] == "url":
            tweet = Twitterwall.add_url(tweet, entity)
        elif entity['type'] == "media":
            tweet = Twitterwall.add_media(tweet, entity)

    rt = ""
    if retweeted_status:
        rt = Markup(
            '<span class="label label-default">RT @{}</span> '
        ).format(status['user']['screen_name'])
    return rt + Markup('{}').format(tweet)


if __name__ == '__main__':
    app.run()
