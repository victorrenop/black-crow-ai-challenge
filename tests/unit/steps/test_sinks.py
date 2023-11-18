"""Test Sink classes"""

from pyspark.sql import SparkSession
from etl_builder.steps import StdoutSink, JsonFileSink, WriteModes


class TestStdoutSink:
    def test_run_step(self, spark_session: SparkSession):
        # arrange
        input_data = [("Foo", 1), ("Bar", 2)]
        input_df = spark_session.createDataFrame(input_data, ["Name", "Value"])
        stdout_sink = StdoutSink(id="test_stdout_sink", spark_session=spark_session)

        # act
        actual_result = stdout_sink.run_step(input_df)

        # assert
        assert input_df.collect() == actual_result.collect()


class TestJsonFileSink:
    def test_run_step(self, tmp_path, spark_session: SparkSession):
        # arrange
        input_data = [("Foo", 1), ("Bar", 2)]
        input_df = spark_session.createDataFrame(input_data, ["Name", "Value"])
        destination_file_path = str(tmp_path / "test_output")
        json_file_sink = JsonFileSink(
            id="test_json_file_sink",
            destination_file_path=destination_file_path,
            save_mode=WriteModes.OVERWRITE,
            spark_session=spark_session,
        )

        # act
        actual_result = json_file_sink.run_step(input_df)

        # assert
        assert actual_result.collect() == input_df.collect()
        assert (
            spark_session.read.json(destination_file_path).collect()
            == input_df.collect()
        )
