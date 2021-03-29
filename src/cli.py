"""cli.py
Command line interface for the data processing tasks
"""
import os
from pathlib import Path
import click
from src import split_geolife


@click.command()
@click.argument("input_dir", type=click.Path(exists=True))
def split(input_dir):
    """Split Geolife user data into files per month."""
    input_dir = Path(input_dir)
    output_dir = input_dir / "user_by_month"
    split_geolife.split_user_months(input_dir, output_dir)


@click.group()
def cli():
    """Command Line Interface for processing GPS data into heatmaps."""


def main():
    # Step 1: split_geolife
    cli.add_command(split)
    cli()


if __name__ == "__main__":
    main()