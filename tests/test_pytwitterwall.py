#!/usr/bin/env python3.4
# coding=utf-8

import pytest
import flexmock
from pytwitterwall import Twitterwall
from io import StringIO
import builtins
import betamax
import os
import sys

from betamax.cassette import cassette


def sanitize_token(interaction, current_cassette):
    # Exit early if the request did not return 200 OK because that's the
    # only time we want to look for Authorization-Token headers
    if interaction.data['response']['status']['code'] != 200:
        return

    headers = interaction.data['request']['headers']
    token = headers.get('Authorization')
    # If there was no token header in the response, exit
    if token is None:
        return

    # Otherwise, create a new placeholder so that when cassette is saved,
    # Betamax will replace the token with our placeholder.
    if isinstance(token, list):
        for item in token:
            current_cassette.placeholders.append(
                cassette.Placeholder(placeholder='<AUTH_TOKEN>', replace=item)
            )
    else:
        current_cassette.placeholders.append(
            cassette.Placeholder(placeholder='<AUTH_TOKEN>', replace=token)
        )

with betamax.Betamax.configure() as config:

    dir_path = os.path.dirname(os.path.realpath(__file__))
    # tell Betamax where to find the cassettes
    # make sure to create the directory
    config.cassette_library_dir = dir_path + '/fixtures/cassettes'

    # AUTH_FILE se nastavuje pomoci
    # $ export AUTH_FILE="./conf/auth.cfg"
    if 'AUTH_FILE' in os.environ:
        # If the tests are invoked with an AUTH_FILE environ variable
        API_KEY, API_SECRET = Twitterwall.get_credentials(
            os.environ['AUTH_FILE']
        )
        # Always re-record the cassetes
        # https://betamax.readthedocs.io/en/latest/record_modes.html
        config.default_cassette_options['record_mode'] = 'all'
    else:
        if os.listdir(config.cassette_library_dir) == []:
            raise Exception(
                "Your AUTH_FILE is missing and you haven't any cassettes"
            )
        API_KEY, API_SECRET = ("api-key", "api-secret")
        # Do not attempt to record sessions with bad fake token
        config.default_cassette_options['record_mode'] = 'none'

    # Filtering Sensitive Data
    config.before_record(callback=sanitize_token)


def test_get_credentials_invalid():
    with pytest.raises(SystemExit):
        api_key, api_secret = Twitterwall.get_credentials(".")


def test_get_credentials():
    expected_api_key = "#key"
    expected_api_secret = "#secret"
    flexmock(builtins, open=StringIO(
        ('[twitter]\nkey={}\nsecret={}\n').format(
            expected_api_key, expected_api_secret
        )
    ))
    api_key, api_secret = Twitterwall.get_credentials(".")
    assert api_key == expected_api_key
    assert api_secret == expected_api_secret


def test__create_session_invalid(betamax_session):
    with pytest.raises(SystemExit):
        twitterwall = Twitterwall(
            api_key="#", api_secret="#", session=betamax_session
        )


def test_search_tweets(betamax_session):
    twitterwall = Twitterwall(
        session=betamax_session,
        api_key=API_KEY,
        api_secret=API_SECRET
    )
    response = twitterwall.search_tweets("python")
    assert response.status_code == 200
    assert isinstance(response.json()['statuses'], list)


def test_get_indices():
    expected_first_index = 8
    expected_second_index = 12
    entity = {
        "user_id": 1,
        "indices": [expected_first_index, expected_second_index],
        "index": 5
    }
    first_index, second_index = Twitterwall.get_indices(entity)
    assert expected_first_index == first_index
    assert expected_second_index == second_index


@pytest.mark.parametrize(
    ['text', 'entity', 'expected_tweet'],
    [
        (
            "my test #tweet #python",
            {"indices": [8, 14]},
            "my test <a href=\"/search/tweet\">#tweet</a> #python"
        ),
        (
            "#python",
            {"indices": [0, 7]},
            "<a href=\"/search/python\">#python</a>"
        )
    ],
)
def test_add_hashtag(text, entity, expected_tweet):
    tweet = Twitterwall.add_hashtag(text, entity)
    assert expected_tweet == tweet


@pytest.mark.parametrize(
    ['text', 'entity', 'expected_tweet'],
    [
        (
            "my test @user #python",
            {"indices": [8, 13]},
            "my test <a href=\"/search/user\">@user</a> #python"
        ),
        (
            "@python",
            {"indices": [0, 7]},
            "<a href=\"/search/python\">@python</a>"
        )
    ],
)
def test_add_user_mention(text, entity, expected_tweet):
    tweet = Twitterwall.add_hashtag(text, entity)
    assert expected_tweet == tweet


def test_add_url():
    tweet = "my test with url python.cz #python"
    entity = {
        "indices": [17, 26],
        "expanded_url": "http://www.python.cz",
        "display_url": "python.cz"
    }
    expected_tweet = (
        "my test with url"
        " <a href=\"http://www.python.cz\">python.cz</a> #python"
    )
    edited_tweet = Twitterwall.add_url(tweet, entity)
    assert expected_tweet == edited_tweet


def test_add_media():
    tweet = "my media test"
    entity = {
        "indices": [13, 13],
        "expanded_url": "http://www.python.cz",
        "media_url": "http://youtube.com/23mg4"
    }
    expected_tweet = (
        "my media test"
        "<br><br><a href=\"http://www.python.cz\">"
        "<img src=\"http://youtube.com/23mg4\"></a>"
    )
    edited_tweet = Twitterwall.add_media(tweet, entity)
    assert expected_tweet == edited_tweet


@pytest.fixture
def testapp(betamax_session):
    from pytwitterwall import app
    app.config['TESTING'] = True
    app.config['session'] = betamax_session
    return app.test_client()


def test_title(testapp):
    response = testapp.get('/')
    assert 200 == response.status_code
    assert '<h1>TwitterWall</h1>' in response.data.decode('utf-8')


def test_wall(testapp):
    response = testapp.get('/search/hroncok/')
    assert 200 == response.status_code
    assert '<h1>twitterwall</h1>' in response.data.decode('utf-8')
