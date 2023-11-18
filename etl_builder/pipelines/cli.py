"""CLI module with commands to run pipelines"""
from typing import Any

import click
from click.exceptions import ClickException

from etl_builder.pipeline import Pipeline, run_pipeline
from etl_builder.pipelines import PIPELINES


def _list_pipelines() -> str:
    return "\n".join("  - " + name for name in PIPELINES.keys())


def _get_pipeline(pipeline_name: str) -> Pipeline:
    pipeline = PIPELINES.get(pipeline_name)
    if not pipeline:
        raise Exception("Pipeline doesn't exist")
    return pipeline


@click.group(context_settings=dict(max_content_width=250))
def pipelines() -> None:
    """All you need for running your pipelines!"""


@pipelines.command()
@click.argument("pipeline-name", type=click.STRING, required=True)
@click.pass_context
def execute(
    ctx: Any,
    pipeline_name: str,
) -> None:
    """Executes a defined pipeline."""
    try:
        pipeline = _get_pipeline(pipeline_name)
        run_pipeline(pipeline)
    except Exception as exc:
        raise ClickException("Pipeline not found: %s" % (exc)) from exc

    click.echo(">>> [CLI] Pipeline execution finished!\n")


@pipelines.command()
def list_pipelines() -> None:
    """List all available pipelines to execute."""

    try:
        pipelines_list = _list_pipelines()
    except Exception as exc:
        raise ClickException("Pipelines definition not found.") from exc
    click.echo(pipelines_list)
