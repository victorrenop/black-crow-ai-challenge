from unittest.mock import Mock

from pyspark.sql import SparkSession

from etl_builder.pipeline import Pipeline, run_pipeline


def test_run_pipeline(spark_session: SparkSession):
    """Testing if all steps are called"""
    # arrange
    source_step = Mock(id="source_id")
    transform_step_1 = Mock(id="transform_id1")
    transform_step_2 = Mock(id="transform_id2")
    sink_step_1 = Mock(id="sink_id1")
    sink_step_2 = Mock(id="sink_id2")
    pipeline = Pipeline(
        id="test_pipeline",
        source=source_step,
        transforms=[transform_step_1, transform_step_2],
        sinks=[sink_step_1, sink_step_2],
    )

    # act
    run_pipeline(pipeline)

    # Assertions based on the mock steps
    assert source_step.run_step_called
    assert transform_step_1.run_step_called
    assert transform_step_2.run_step_called
    assert sink_step_1.run_step_called
    assert sink_step_2.run_step_called
