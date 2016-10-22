#!/usr/bin/env python3.4
# coding=utf-8

import click
import sys
from pytwitterwall.base import Twitterwall
from pytwitterwall.web import app


@click.group()
@click.option('--conf', default="./conf/auth.cfg",
              help='Configuration path [./conf/auth.cfg].')
@click.option('--initial-count', default=15,
              help='Count of first tweets [15]. Max 100.')
@click.option('--retweets-are-allowed/--no-retweets', default=True,
              help='Flag that shows retweets. Defaults to true.')
@click.pass_context
def cli(ctx, conf, initial_count, retweets_are_allowed):
    """
    Simple program which reads posts from Twitter via its API.
    """
    ctx.obj = Twitterwall(conf, initial_count, retweets_are_allowed)


@cli.command()
@click.option('--debug/--no-debug', default=False, help='Use debugger.')
@click.pass_obj
def web(twitterwall, debug):
    """Run the web app"""
    app.config['twitterwall'] = twitterwall
    app.run(debug=debug)


@cli.command()
@click.option('-q', '--query', default="#python",
              prompt="Your query string", help='Query string.')
@click.option('--loop', default=5,
              help='How often tweets will be reloaded in secs [5].')
@click.pass_obj
def console(twitterwall, query, loop):
    """Run the console app"""
    twitterwall.infinite_loop(query, loop)

cli(prog_name='pytwitterwall')

def main():
    cli()
