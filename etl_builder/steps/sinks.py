"""Data sinks definitions"""

from typing import Any, Dict, List, Optional
from pyspark.sql import DataFrame, SparkSession
from etl_builder.steps import Step, WriteModes

class StdoutSink(Step):
    """Outputs the DataFrame in the Stdout of the system for debugging.

    Attributes:
        row_number (int, optional): Maximum number of rows to show. Defaults to 10.
        vertical (bool, optional): Displays the data in the vertical format. Defaults to True.
        truncated (bool, optional): Truncate the row results. Defaults to True.

    Returns:
        DataFrame: output DataFrame
    """

    def __init__(self, id: str, spark_session: Optional[SparkSession] = None, row_number: int = 10, vertical: bool = True, truncated: bool = True) -> None:
        super().__init__(id=id, spark_session=spark_session)
        self._row_number = row_number
        self._vertical = vertical
        self._truncated = truncated
    
    def _run_step(self, input_df: Optional[DataFrame] = None) -> DataFrame:

        input_df.show(n=self._row_number, truncate=self._truncated, vertical=self._vertical)
        return input_df


class JsonFileSink(Step):
    """Writes the DataFrame in a json file.

    Attributes:
        destination_file_path (str): Name of the destionation json file.
        save_mode (str): One of the modes defined by the WriteModes enumerator.
    """

    def __init__(self, id: str, destination_file_path: str, save_mode: str = WriteModes.OVERWRITE, write_options: Optional[Dict[str, Any]] = None, spark_session: Optional[SparkSession] = None) -> None:
        super().__init__(id=id, spark_session=spark_session)
        self._destination_file_path = destination_file_path
        self._save_mode = save_mode
        self._write_options = write_options or {}
    
    def _run_step(self, input_df: Optional[DataFrame] = None) -> DataFrame:
        input_df.coalesce(1).write \
            .format("json") \
            .mode(self._save_mode) \
            .options(**self._write_options) \
            .save(self._destination_file_path)

        return input_df
