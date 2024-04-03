import dlt
from dlt.common.pipeline import LoadInfo
from dlt.pipeline.pipeline import Pipeline
from dlt.destinations.impl.bigquery.bigquery_adapter import bigquery_adapter
from .helpers import add_etl_timestamp

try:
    from .mongodb import mongodb_collection  # type: ignore
except ImportError:
    from mongodb import mongodb_collection


def get_dlt_pipeline_instance(dataset_name: str) -> Pipeline:
    pipeline = dlt.pipeline(
        pipeline_name="local_mongo",
        destination="bigquery",
        progress="log",
        dataset_name=dataset_name,
        full_refresh=True,
    )
    return pipeline


def full_load_collection(
    pipeline: Pipeline, collection_name: str, database_name: str = None
) -> LoadInfo:
    extracted_data = mongodb_collection(
        database=database_name,
        collection=collection_name,
        parallel=True,
    )

    extracted_data = extracted_data.mongodb.add_map(add_etl_timestamp)

    extracted_data = bigquery_adapter(
        extracted_data,
        partition="_etl_timestamp",
        table_description="finance book",
    )

    @dlt.source(max_table_nesting=0)
    def wrapping_source():
        return extracted_data

    info = pipeline.run(
        wrapping_source(),
        write_disposition="append",
        loader_file_format="jsonl",
        staging="filesystem",
    )

    return info
