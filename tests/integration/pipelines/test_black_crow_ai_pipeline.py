"""Test if the pipeline is behaving as expected"""

from copy import deepcopy

from pytest_spark import spark_session
from etl_builder.pipelines.black_crow_ai_pipeline import black_crow_ai_pipeline
from etl_builder.pipeline import run_pipeline


def test_black_crow_ai_pipeline_output(tmp_path, spark_session: spark_session):
    # arrange
    test_input_path = "tests/integration/pipelines/data/"
    test_temp_output_path = str(tmp_path / "output_file")
    file_paths = [f"{test_input_path}/input_file.json.gz"]
    testing_pipeline = deepcopy(black_crow_ai_pipeline)
    testing_pipeline.source._file_paths = file_paths
    testing_pipeline.sinks[1]._destination_file_path = test_temp_output_path
    expected_result = spark_session.read.json(
        f"{test_input_path}/expected_result.json"
    ).collect()

    # act
    run_pipeline(testing_pipeline)
    actual_result = spark_session.read.json(test_temp_output_path).collect()

    # assert
    assert actual_result == expected_result
