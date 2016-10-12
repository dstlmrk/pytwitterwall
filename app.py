#!/usr/bin/env python3.4
# coding=utf-8

from flask import Flask, abort, url_for, render_template
import jinja2
from jinja2 import Markup

app = Flask("twitterwall")

@app.route('/')
def index():
    # return url_for('search', query='search')
    return 'Index Page'

# cesty psat s lomitkem
@app.route('/hello/')
def hello():
    return 'Hello, World'

@app.route('/template/')
@app.route('/template/<query>')
def template(query=None):
    return render_template('template.html', query=query)

@app.route('/search/<query>')
def search(query):
    return 'Search {}'.format(query)

@app.template_filter('capitalize')
def capitalize(text):
    return Markup('<i>{}</i>').format(text.capitalize())

if __name__ == '__main__':
    app.run(debug=True)