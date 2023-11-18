"""Pipelines init module"""
from etl_builder.pipelines.black_crow_ai_pipeline import black_crow_ai_pipeline

# All pipelines definitions that can be run by the CLI
PIPELINES = {
    "black_crow_ai_pipeline": black_crow_ai_pipeline,
}

__all__ = ["PIPELINES"]
