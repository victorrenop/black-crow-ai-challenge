"""Test Transform classes"""

from pyspark.sql import SparkSession
from etl_builder.steps import (
    FillNullTransform,
    FlattenNestedTransform,
    UserAgentParserTransform,
)


class TestFillNullTransform:
    def test_fill_null_transform(self, spark_session: SparkSession):
        # arrange
        column_name = "example_column"
        value_to_fill = "default_value"
        fill_null_transform = FillNullTransform(
            id="test_id",
            column_name=column_name,
            value=value_to_fill,
            spark_session=spark_session,
        )
        input_data = [
            {"id": 1, column_name: None},
            {"id": 2, column_name: "some_value"},
            {"id": 3, column_name: None},
        ]
        input_df = spark_session.createDataFrame(input_data)
        expected_result = [
            {"id": 1, column_name: value_to_fill},
            {"id": 2, column_name: "some_value"},
            {"id": 3, column_name: value_to_fill},
        ]

        # act
        actual_result = fill_null_transform.run_step(input_df)

        # assert
        assert actual_result.filter(actual_result[column_name].isNull()).count() == 0
        assert [row.asDict() for row in actual_result.collect()] == expected_result


class TestFlattenNestedTransform:
    def test_flatten_nested_transform(self, spark_session: SparkSession):
        # act
        column_name = "nested_column"
        subset = ["field1"]
        drop_original_column = True
        flatten_transform = FlattenNestedTransform(
            id="test_id",
            column_name=column_name,
            subset=subset,
            drop_original_column=drop_original_column,
            spark_session=spark_session,
        )
        input_data = [
            {"id": 1, column_name: {"field1": "value1", "field2": "value2"}},
            {"id": 2, column_name: {"field1": "value3", "field2": "value4"}},
        ]
        input_df = spark_session.createDataFrame(input_data)
        expected_result = [{"id": 1, "field1": "value1"}, {"id": 2, "field1": "value3"}]

        # act
        actual_result = flatten_transform.run_step(input_df)

        # assert
        assert [row.asDict() for row in actual_result.collect()] == expected_result


class TestUserAgentParserTransform:
    def test_user_agent_parser_transform(self, spark_session: SparkSession):
        # arrange
        ua_string_column = "user_agent"
        output_column = "parsed_user_agent"
        ua_parser_transform = UserAgentParserTransform(
            id="test_id",
            ua_string_column=ua_string_column,
            output_column=output_column,
            spark_session=spark_session,
        )
        input_data = [
            {
                "id": 1,
                ua_string_column: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",  # noqa: E501
            },
            {
                "id": 2,
                ua_string_column: "Mozilla/5.0 (Linux; Android 10; SM-G960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36",  # noqa: E501
            },
            {
                "id": 3,
                ua_string_column: "Mozilla/5.0 (iPad; CPU OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1",  # noqa: E501
            },
            {
                "id": 4,
                ua_string_column: "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
            },
            {"id": 5, ua_string_column: ""},
        ]
        input_df = spark_session.createDataFrame(input_data)
        expected_result = [
            {
                "id": 1,
                ua_string_column: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",  # noqa: E501
                "parsed_user_agent": {
                    "device_type": "Desktop",
                    "browser_type": "Chrome",
                    "browser_version": "91.0.4472",
                },
            },
            {
                "id": 2,
                ua_string_column: "Mozilla/5.0 (Linux; Android 10; SM-G960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36",  # noqa: E501
                "parsed_user_agent": {
                    "device_type": "Mobile",
                    "browser_type": "Chrome Mobile",
                    "browser_version": "91.0.4472",
                },
            },
            {
                "id": 3,
                ua_string_column: "Mozilla/5.0 (iPad; CPU OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1",  # noqa: E501
                "parsed_user_agent": {
                    "device_type": "Tablet",
                    "browser_type": "Mobile Safari",
                    "browser_version": "14.1.1",
                },
            },
            {
                "id": 4,
                ua_string_column: "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
                "parsed_user_agent": {
                    "device_type": "Bot",
                    "browser_type": "Googlebot",
                    "browser_version": "2.1",
                },
            },
            {
                "id": 5,
                ua_string_column: "",
                "parsed_user_agent": {
                    "device_type": "Other",
                    "browser_type": "Other",
                    "browser_version": "Other",
                },
            },
        ]

        # act
        actual_result = ua_parser_transform.run_step(input_df)

        # assert
        actual_result_to_dict_list = [row.asDict() for row in actual_result.collect()]
        actual_result_to_dict_list = [
            {**row, **{"parsed_user_agent": row["parsed_user_agent"].asDict()}}
            for row in actual_result_to_dict_list
        ]

        assert actual_result_to_dict_list == expected_result
