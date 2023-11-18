import logging
from typing import List
from dataclasses import dataclass

from etl_builder.steps import Step

logger = logging.getLogger(__name__)


@dataclass
class Pipeline:
    """Pipeline class that holds the pipeline steps to be executed. The pipeline steps can be divded
    into three main steps: Source, Transform and Sink. Only one Source is allowed and the rest can have
    multiple definitions.
    """

    id: str
    source: Step
    transforms: List[Step]
    sinks: List[Step]


def run_pipeline(pipeline: Pipeline) -> None:
    """
    Runs the provided pipeline configuration.
    The execution follows the order: sources, transforms and then sinks.

    pipeline (Pipeline): Pipeline configurations to be ran.
    """
    try:
        logger.info("Starting '%s' execution" % (pipeline.id))
        logger.info(
            "Running step '%s'" % (pipeline.id),
            extra={"step_id": pipeline.source.step_name},
        )
        transform_df = pipeline.source.run_step()
        for transform in pipeline.transforms:
            logger.info("Running step '%s'" % (transform.step_name))
            transform_df = transform.run_step(transform_df)
        for sink in pipeline.sinks:
            logger.info("Running step '%s'" % (sink.step_name))
            transform_df = sink.run_step(transform_df)

    except Exception as ex:
        logger.error("Pipeline execution failed!")
        raise Exception(ex) from ex
