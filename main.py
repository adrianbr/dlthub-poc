from mongodb.pipeline import full_load_collection, get_dlt_pipeline_instance

dataset_name = "dlt_poc"

pipeline_instance = get_dlt_pipeline_instance(dataset_name)


pipeline = full_load_collection(
    pipeline=pipeline_instance, collection_name="financeBooks"
)
