"""cli.py
Command line interface for the data processing tasks
"""
import click


@click.group()
def cli():
    """Command Line Interface for processing GPS data into heatmaps."""


if __name__ == "__main__":
    cli()