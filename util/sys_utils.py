import logging
import sys

import click


def exit_with_message(msg):
    click.echo(msg)
    logging.error(msg)
    click.echo("Exiting")
    logging.error("Exiting")
    sys.exit(1)
