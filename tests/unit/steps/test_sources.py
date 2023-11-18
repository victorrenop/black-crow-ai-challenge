"""Test Source classes"""

from pyspark.sql import SparkSession
from etl_builder.steps import JsonFileSource


class TestJsonFileSource:
    def test_run_step(self, spark_session: SparkSession):
        # arrange
        test_path = "tests/unit/steps/data/"
        file_paths = [
            f"{test_path}/input_file_1.json",
            f"{test_path}/input_file_2.json",
        ]
        expected_result = [
            {"Name": "Foo", "Value": 1},
            {"Name": "Bar", "Value": 2},
            {"Name": "Baz", "Value": 3},
        ]
        json_source = JsonFileSource(
            id="test_id",
            file_paths=file_paths,
            spark_session=spark_session,
        )

        # act
        actual_result = json_source.run_step()

        # assert
        assert [row.asDict() for row in actual_result.collect()] == expected_result
