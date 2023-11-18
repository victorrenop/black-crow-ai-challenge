"""Data sources definitions"""

from typing import Any, Dict, List, Optional
from pyspark.sql import DataFrame, SparkSession
from etl_builder.steps import Step


class JsonFileSource(Step):
    """Reads the content from one or more json files.

    Attributes:
        file_paths (List[str]): List of file paths representing the json files.
        json_read_options (Dict[str, Any], optional): Json read options to be used by spark. Defaults to {}.
    """

    def __init__(
        self,
        id: str,
        file_paths: List[str],
        json_read_options: Optional[Dict[str, Any]] = None,
        spark_session: Optional[SparkSession] = None,
    ) -> None:
        super().__init__(id=id, spark_session=spark_session)
        self._file_paths = file_paths
        self._json_read_options = json_read_options or {}

    def _run_step(self, input_df: Optional[DataFrame] = None) -> DataFrame:
        return self.spark_session.read.options(**self._json_read_options).json(
            self._file_paths
        )
