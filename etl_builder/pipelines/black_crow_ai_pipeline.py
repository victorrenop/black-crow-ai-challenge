"""Black Crow AI challenge pipeline definition"""

from etl_builder.pipeline import Pipeline
from etl_builder.steps import JsonFileSource, JsonFileSink, StdoutSink, FillNullTransform, FlattenNestedTransform, UserAgentParserTransform
from etl_builder.pipeline import run_pipeline

black_crow_ai_pipeline = Pipeline(
    id="black_crow_ai_pipeline",
    source=JsonFileSource(id="extract_input_json_file", file_paths=["data/sample_orders.json.gz"]),
    transforms=[
        FillNullTransform(id="fill_null_user_agent_string_with_empty_string", column_name="USER_AGENT", value=""),
        UserAgentParserTransform(id="parse_ua_string", ua_string_column="USER_AGENT", output_column="parsed_ua_agent"),
        FlattenNestedTransform(id="flatten_parsed_ua_field", column_name="parsed_ua_agent", subset=["device_type", "browser_type", "browser_version"], drop_original_column=True),
    ],
    sinks=[
        StdoutSink(id="debug_output", truncated=False),
        JsonFileSink(id="save_result_to_json_file", destination_file_path="data/processed_orders", write_options={"compression": "gzip"})
    ]
)

if __name__ == "__main__":
    run_pipeline(black_crow_ai_pipeline)
