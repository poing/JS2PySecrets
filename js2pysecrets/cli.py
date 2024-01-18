# js2pysecrets/cli.py

import click
from .wrapper import wrapper

@click.command()
def main():
    wrapper()

if __name__ == "__main__":
    main()
