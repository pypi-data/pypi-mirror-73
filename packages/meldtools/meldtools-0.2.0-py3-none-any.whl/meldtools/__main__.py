'''Main entry point for the command-line interface'''

# Standard library imports
from dataclasses import asdict
import json
from pathlib import Path
import sys

# Non-standard library imports
import click

# Local imports
from . import __version__
from meldtools import load
from meldtools.models import MeldJsonSchema


@click.group()
@click.version_option(version=__version__)
def main():
    '''The entry point for the meldtools CLI utilities'''
    pass


@main.command()
@click.option('directory',
              '-d',
              '--dir',
              type=click.Path(exists=True),
              help='Directory to traverse and find MELD text files.')
@click.option('register',
            '-r',
            '--reg',
            type=click.Path(exists=True),
            help='Register CSV with corpus metadata.')
@click.argument('output', type=click.File('w'))
def jsonify(directory, register, output) -> None:
    meld = load(directory, register)
    for d in meld:
        try:
            schema = MeldJsonSchema(d.meld_code, d.date,  # type: ignore
                                    d.period, d.latitude, # type: ignore
                                    d.longitude, d.format, # type: ignore
                                    d.function_primary, # type: ignore
                                    d.function_secondary, # type: ignore
                                    d.conc) # type: ignore
            out = json.dumps(asdict(schema))
            output.write(out + '\n')
        except AttributeError:
            sys.stderr.write(f'Could not parse {d=}')
