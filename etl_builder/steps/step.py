"""Generic step definition that a pipeline can run"""

from abc import ABC, abstractmethod
from typing import Optional
from enum import StrEnum

from pyspark.sql import DataFrame, SparkSession


class WriteModes(StrEnum):
    """Definition of DataFrame write modes"""

    APPEND = "append"
    OVERWRITE = "overwrite"


class Step(ABC):
    """Generic step definition that a pipeline can run

    Attributes:
        id (str): ID of the step, used to identify the step execution in the logging porocess
    """

    def __init__(self, id: str, spark_session: Optional[SparkSession] = None) -> None:
        self._id = id
        self._spark_session = spark_session

    @property
    def step_name(self) -> str:
        return f"({self.__class__.__name__}) {self._id}"

    @property
    def spark_session(self) -> SparkSession:
        if not self._spark_session:
            self._spark_session = SparkSession.builder.getOrCreate()
        return self._spark_session

    def run_step(self, input_df: Optional[DataFrame] = None, **kwargs) -> DataFrame:
        """Runs the pipeline step using the input PySpark DataFrame if needed
        and outputing a new copy of the data as a new PySpark DataFrame.

        Args:
            input_df (DataFrame): The input PySpark DataFrame to be used in the
            step's execution. Can also be None if the step uses an external data source.

        Returns:
            DataFrame: The resulting DataFrame, always a new copy to avoid undesirable
            data mutation.
        """

        return self._run_step(input_df=input_df, **kwargs)

    @abstractmethod
    def _run_step(self, input_df: Optional[DataFrame] = None, **kwargs) -> DataFrame:
        pass
