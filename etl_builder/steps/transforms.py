"""Data transformations definitions"""

from typing import Any, Dict, List, Optional

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.types import StructField, StructType, StringType
from pyspark.sql.functions import col, udf

from etl_builder.steps import Step

from user_agents import parse


class FillNullTransform(Step):
    """Fills nulls with the desired values

    Attributes:
        column_name (str): name of the column to fill null values
        value: (str | int | float): value to fill the nulls
    """

    def __init__(self, id: str, column_name: str, value: str | int | float, spark_session: Optional[SparkSession] = None) -> None:
        super().__init__(id=id, spark_session=spark_session)
        self._column_name = column_name
        self._value = value

    def _run_step(self, input_df: Optional[DataFrame] = None) -> DataFrame:
        return input_df.na.fill(value=self._value, subset=[self._column_name])


class FlattenNestedTransform(Step):
    """Flattens a nested field into columns

    Attributes:
        column_name (str): name of the column to flatten
        subset (List[str]): List of fields to flatten.
        drop_original_column (bool): Drops the nested column if True. Defaults to False.
    """

    def __init__(self, id: str, column_name: str, subset: List[str], drop_original_column: bool = False, spark_session: Optional[SparkSession] = None) -> None:
        super().__init__(id=id, spark_session=spark_session)
        self._column_name = column_name
        self._subset = subset
        self._drop_original_column = drop_original_column

    def _run_step(self, input_df: Optional[DataFrame] = None) -> DataFrame:
        result_df = input_df
        for subset_field in self._subset:
            result_df = result_df.withColumn(subset_field, col(f"{self._column_name}.{subset_field}"))
        if self._drop_original_column:
            result_df = result_df.drop(self._column_name)

        return result_df


class UserAgentParserTransform(Step):
    """Parses the desired User Agent column into 3 fields: device_type, browser_type and browser_version.

    Attributes:
        ua_string_column (str): Name of the column containing the User Agent string
        output_column (str): Name of the output column
    """
    def __init__(self, id: str, ua_string_column: str, output_column: str, spark_session: Optional[SparkSession] = None) -> None:
        super().__init__(id=id, spark_session=spark_session)
        self._ua_string_column = ua_string_column
        self._output_column = output_column
    
    def _parse_ua_string(self, ua_string: str) -> Dict[str, Any]:
        """Parses a User Agent string, returning the Device Type, Browser Type and Browser Version.

        Args:
            ua_string (str): User Agent string to be parsed.

        Returns:
            List[str]: Dict containing device_type, browser_type and browser_version.
        """

        parsed_string = parse(ua_string)

        device_type = "Other"
        if parsed_string.is_tablet:
            device_type = "Tablet"
        elif parsed_string.is_mobile:
            device_type = "Mobile"
        elif parsed_string.is_pc:
            device_type = "Desktop"
        elif parsed_string.is_bot:
            device_type = "Bot"

        return [
            device_type,
            parsed_string.browser.family,
            parsed_string.browser.version_string if parsed_string.browser.version_string != "" else "Other",
        ]
    
    def _run_step(self, input_df: Optional[DataFrame] = None) -> DataFrame:

        parse_ua_string_udf = udf(
            lambda ua_string: self._parse_ua_string(ua_string),
            StructType(
                [
                    StructField("device_type", StringType(), False),
                    StructField("browser_type", StringType(), False),
                    StructField("browser_version", StringType(), False),
                ]
            )
        )

        return input_df.withColumn(self._output_column, parse_ua_string_udf(self._ua_string_column))
