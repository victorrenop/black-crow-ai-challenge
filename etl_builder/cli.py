"""CLI module with all the commands implementations."""
import click

from etl_builder.pipelines.cli import pipelines
from etl_builder.data_quality.cli import data_quality


@click.group()
def cli() -> None:
    """Black Crow AI challenge CLI to run pipelines and data quality reports"""


cli.add_command(pipelines)
cli.add_command(data_quality)


if __name__ == "__main__":
    cli()  # pragma: no cover
