"""Data sources definitions"""

from typing import Any, Dict, List, Optional
from pyspark.sql import DataFrame, SparkSession
from etl_builder.steps import Step

class JsonFileSource(Step):
    """Reads the content from one or more json files.

    Attributes:
        file_paths (List[str]): List of file paths representing the json files.
        json_read_options (Dict[str, Any], optional): Json read options to be used by spark. Defaults to {}.
        schema (Optional[Dict[str, Any]], optional): Schema to be used at read time. Defaults to None.
    """

    def __init__(self, id: str, file_paths: List[str], schema: Optional[Dict[str, Any]] = None, json_read_options: Optional[Dict[str, Any]] = None, spark_session: Optional[SparkSession] = None) -> None:
        super().__init__(id=id, spark_session=spark_session)
        self._file_paths = file_paths
        self._schema = schema
        self._json_read_options = json_read_options or {}
    
    def _run_step(self, input_df: Optional[DataFrame] = None) -> DataFrame:

        write_expression = self.spark_session.read.options(**self._json_read_options)
        if self._schema:
            write_expression = write_expression.schema(self._schema)
        return write_expression.json(self._file_paths)
