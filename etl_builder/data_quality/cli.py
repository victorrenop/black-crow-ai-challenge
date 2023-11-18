"""CLI module with commands to run data quality checks"""
from typing import Any

import click
from click.exceptions import ClickException

from etl_builder.data_quality import run_data_quality


@click.group(context_settings=dict(max_content_width=250))
def data_quality() -> None:
    """All you need for running your data quality checks!"""


@data_quality.command()
@click.argument("input-data-path", type=click.STRING, required=True)
@click.argument("expectation-suite-name", type=click.STRING, required=True)
@click.pass_context
def execute(
    ctx: Any,
    input_data_path: str,
    expectation_suite_name: str,
) -> None:
    """Executes a defined data quality check using a Great Expectations expectation suite."""
    try:
        run_data_quality(input_data_path, expectation_suite_name)
    except Exception as exc:
        raise ClickException("Pipeline not found: %s" % (exc)) from exc

    click.echo(">>> [CLI] :white_check_mark:Pipeline execution finished!!!\n")
