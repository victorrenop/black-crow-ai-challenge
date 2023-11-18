"""Great Expectations data quality basic configurations"""
import pathlib

from great_expectations.data_context.types.base import (
    DataContextConfig,
    DatasourceConfig,
)
from great_expectations.data_context.data_context import BaseDataContext

from etl_builder.steps import JsonFileSource

_DEFAULT_GE_CONFIGS = {
    "anonymous_usage_statistics": {"enabled": False},
    "datasources": {
        "pyspark_df_source": DatasourceConfig(
            class_name="Datasource",
            module_name="great_expectations.datasource",
            execution_engine={
                "class_name": "SparkDFExecutionEngine",
                "module_name": "great_expectations.execution_engine",
                "force_reuse_spark_context": True,
            },
            data_connectors={
                "default_runtime_data_connector_name": {
                    "class_name": "RuntimeDataConnector",
                    "batch_identifiers": ["batch_id"],
                    "module_name": "great_expectations.datasource.data_connector",
                },
            },
        )
    },
    "stores": {
        "expectations_store": {
            "class_name": "ExpectationsStore",
            "store_backend": {
                "class_name": "TupleFilesystemStoreBackend",
                "base_directory": "data/great_expectations_configs/expectations/",
                "root_directory": str(pathlib.Path.cwd()),
            },
        },
        "validations_store": {
            "class_name": "ValidationsStore",
            "store_backend": {
                "class_name": "TupleFilesystemStoreBackend",
                "base_directory": "data/great_expectations_configs/validations/",
                "root_directory": str(pathlib.Path.cwd()),
            },
        },
        "checkpoints_store": {
            "class_name": "CheckpointStore",
            "store_backend": {
                "class_name": "TupleFilesystemStoreBackend",
                "base_directory": "data/great_expectations_configs/checkpoints/",
                "root_directory": str(pathlib.Path.cwd()),
            },
        },
        "evaluation_parameter_store": {"class_name": "EvaluationParameterStore"},
    },
    "expectations_store_name": "expectations_store",
    "validations_store_name": "validations_store",
    "checkpoint_store_name": "checkpoints_store",
    "evaluation_parameter_store_name": "evaluation_parameter_store",
    "data_docs_sites": {
        "store_site": {
            "class_name": "SiteBuilder",
            "store_backend": {
                "class_name": "TupleFilesystemStoreBackend",
                "base_directory": "data/great_expectations_configs/data-docs/",
                "root_directory": str(pathlib.Path.cwd()),
            },
            "site_index_builder": {
                "class_name": "DefaultSiteIndexBuilder",
                "show_cta_footer": True,
            },
        }
    },
}


def run_data_quality(input_json_file_path: str, expectation_suite_name: str) -> None:
    context = BaseDataContext(project_config=DataContextConfig(**_DEFAULT_GE_CONFIGS))
    input_df = JsonFileSource(
        id="json_validation", file_paths=[input_json_file_path]
    ).run_step()

    checks_result = context.run_checkpoint(
        checkpoint_name="dq_general_checkpoint",
        batch_request={
            "runtime_parameters": {
                "batch_data": input_df,
            },
            "batch_identifiers": {
                "batch_id": "parsed_ua_output",
            },
            "data_asset_name": "parsed_ua_output",
        },
        expectation_suite_name=expectation_suite_name,
    )

    print(checks_result)
